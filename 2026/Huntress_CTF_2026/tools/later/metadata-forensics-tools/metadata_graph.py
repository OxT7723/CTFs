"""Extract execution and delivery references from mixed metadata evidence."""
from __future__ import annotations

from email import policy
from email.parser import BytesParser
from io import BytesIO
import json
import re
import sqlite3
import struct
import zlib
from zipfile import ZipFile


def _png_text(data: bytes) -> list[str]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return []
    values: list[str] = []
    offset = 8
    while offset + 12 <= len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        chunk_type = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            break
        payload = data[offset + 8:offset + 8 + length]
        checksum = struct.unpack_from(">I", data, offset + 8 + length)[0]
        if zlib.crc32(chunk_type + payload) & 0xFFFFFFFF == checksum:
            if chunk_type == b"tEXt" and b"\x00" in payload:
                _, text = payload.split(b"\x00", 1)
                values.append(text.decode("latin-1", "replace"))
        offset = end
        if chunk_type == b"IEND":
            break
    return values


def _references(name: str, data: bytes) -> list[str]:
    """Return artifact IDs explicitly named by a file's primary contents."""
    references: list[str] = []

    if data.startswith(b"PK\x03\x04"):
        try:
            with ZipFile(BytesIO(data)) as archive:
                for member in archive.infolist():
                    if member.is_dir() or member.filename.rsplit("/", 1)[-1].casefold() != "run.txt":
                        continue
                    text = archive.read(member).decode("utf-8-sig", "replace")
                    references.extend(
                        re.findall(r"(?im)^\s*execute\s+([A-Za-z0-9][A-Za-z0-9_-]*)\s*$", text)
                    )
        except (OSError, ValueError):
            pass
        return references

    if data.startswith(b"SQLite format 3\x00"):
        connection = sqlite3.connect(":memory:")
        try:
            connection.deserialize(data)
            exists = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='launch_queue'"
            ).fetchone()
            if exists:
                references.extend(
                    str(row[0]) for row in connection.execute(
                        "SELECT target FROM launch_queue WHERE target IS NOT NULL"
                    )
                )
        except sqlite3.Error:
            pass
        finally:
            connection.close()
        return references

    if data.lstrip().startswith(b"{"):
        try:
            value = json.loads(data)
        except (json.JSONDecodeError, UnicodeDecodeError):
            value = None
        if isinstance(value, dict) and isinstance(value.get("next"), str):
            return [value["next"]]

    references.extend(
        re.findall(r"(?m)^next=([A-Za-z0-9][A-Za-z0-9_-]*)\s*$", "\n".join(_png_text(data)))
    )
    if references:
        return references

    # Preserve literal target references from command lines even when quoting
    # is malformed; the referenced file is still part of the evidence graph.
    text = data.decode("utf-8-sig", "replace")
    references.extend(
        match.group(2)
        for match in re.finditer(
            r"""(?im)^\s*(?:Start-Process|Invoke-Item|&)\s+(['"])\.?[\\/]+([A-Za-z0-9][A-Za-z0-9_-]*)['"]""",
            text,
        )
    )
    if references:
        return references

    if b"\n" in data and (data.startswith(b"From: ") or b"\nMessage-ID:" in data):
        message = BytesParser(policy=policy.default).parsebytes(data)
        for part in message.walk():
            if part.get_filename() and part.get_payload(decode=True):
                attachment = part.get_payload(decode=True).decode("utf-8-sig", "replace")
                references.extend(
                    re.findall(
                        r"(?im)^\s*(?:open|next|forwarded\s+to|continue\s+with)\s*:\s*([A-Za-z0-9][A-Za-z0-9_-]*)\s*$",
                        attachment,
                    )
                )
    return references


def _json_done(data: bytes) -> bool:
    if not data.lstrip().startswith(b"{"):
        return False
    try:
        value = json.loads(data)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False
    return isinstance(value, dict) and value.get("done") is True


def _cyclic_nodes(graph: dict[str, list[str]]) -> set[str]:
    """Return nodes that belong to a directed cycle."""
    index = 0
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    cyclic: set[str] = set()

    def connect(node: str) -> None:
        nonlocal index
        indices[node] = lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for child in graph[node]:
            if child not in indices:
                connect(child)
                lowlinks[node] = min(lowlinks[node], lowlinks[child])
            elif child in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[child])

        if lowlinks[node] != indices[node]:
            return
        component: list[str] = []
        while True:
            child = stack.pop()
            on_stack.remove(child)
            component.append(child)
            if child == node:
                break
        if len(component) > 1 or node in graph[node]:
            cyclic.update(component)

    for node in graph:
        if node not in indices:
            connect(node)
    return cyclic


def execution_chain_artifact_ids(target, files) -> list[str]:
    """Return the longest evidence-backed execution/delivery path in a case ZIP."""
    by_id = {}
    for item in files:
        if (
            len(item.chain) != len(target.chain) + 1
            or item.chain[:len(target.chain)] != target.chain
        ):
            continue
        member_path = item.chain[-1].replace("\\", "/").split("/")
        if len(member_path) == 2 and member_path[0].casefold() == "artifacts":
            by_id[member_path[1]] = item
    graph: dict[str, list[str]] = {artifact_id: [] for artifact_id in by_id}
    terminal_nodes = {
        artifact_id for artifact_id, item in by_id.items()
        if any(re.match(r"\s*done\b", value, re.IGNORECASE) for value in _png_text(item.data))
        or bool(re.search(
            r"(?im)^\s*#.*\bterminal\b",
            item.data.decode("utf-8-sig", "replace"),
        ))
        or _json_done(item.data)
    }
    for artifact_id, item in by_id.items():
        for reference in _references(item.name, item.data):
            if reference in by_id and reference not in graph[artifact_id]:
                graph[artifact_id].append(reference)
        graph[artifact_id].sort()

    paths: list[tuple[str, ...]] = []

    def visit(node: str, path: tuple[str, ...], seen: frozenset[str]) -> None:
        next_nodes = [child for child in graph[node] if child not in seen]
        if not next_nodes:
            paths.append(path)
            return
        for child in next_nodes:
            visit(child, path + (child,), seen | {child})

    for node in sorted(graph):
        visit(node, (node,), frozenset({node}))
    if not paths:
        return []
    completed = [path for path in paths if path[-1] in terminal_nodes]
    if completed:
        paths = completed
    else:
        # Randomized corpora can contain a large, self-referential decoy
        # component beside the actual source-to-delivery route. Ignore cyclic
        # components when a clean acyclic path is available.
        cyclic = _cyclic_nodes(graph)
        acyclic_graph = {
            node: [child for child in children if child not in cyclic]
            for node, children in graph.items()
            if node not in cyclic
        }
        acyclic_paths: list[tuple[str, ...]] = []

        def visit_acyclic(node: str, path: tuple[str, ...]) -> None:
            children = acyclic_graph[node]
            if not children:
                acyclic_paths.append(path)
                return
            for child in children:
                visit_acyclic(child, path + (child,))

        incoming = {child for children in acyclic_graph.values() for child in children}
        for node in sorted(set(acyclic_graph) - incoming):
            visit_acyclic(node, (node,))
        if acyclic_paths:
            paths = acyclic_paths
    longest = max(map(len, paths))
    return list(min(path for path in paths if len(path) == longest))
