#!/usr/bin/env python3
"""Build metadata answers from a live Game Master assignment and submit them."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from email import policy
from email.parser import BytesParser
from datetime import datetime, timezone
import hashlib
import http.client
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.parse
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from zipfile import BadZipFile, ZipFile, is_zipfile

try:
    import pyzipper
except ImportError:  # Standard, unencrypted ZIP files remain supported.
    pyzipper = None


def load_helper(filename: str, module_name: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


PE_METADATA = load_helper("pe_metadata.py", "pe_metadata")
ZIP_METADATA = load_helper("zip_metadata.py", "zip_metadata")
SHORTCUT_METADATA = load_helper("shortcut_metadata.py", "shortcut_metadata")
OOXML_METADATA = load_helper("ooxml_metadata.py", "ooxml_metadata")
MEDIA_METADATA = load_helper("audio_metadata.py", "audio_metadata")
VIDEO_METADATA = load_helper("video_metadata.py", "video_metadata")
ELF_METADATA = load_helper("elf_metadata.py", "elf_metadata")
MACHO_METADATA = load_helper("macho_metadata.py", "macho_metadata")
JAR_METADATA = load_helper("jar_metadata.py", "jar_metadata")
APK_METADATA = load_helper("apk_metadata.py", "apk_metadata")
SQLITE_METADATA = load_helper("sqlite_metadata.py", "sqlite_metadata")
EVTX_METADATA = load_helper("evtx_metadata.py", "evtx_metadata")
REGISTRY_METADATA = load_helper("registry_metadata.py", "registry_metadata")
PREFETCH_METADATA = load_helper("prefetch_metadata.py", "prefetch_metadata")
PCAP_METADATA = load_helper("pcap_metadata.py", "pcap_metadata")
DISK_METADATA = load_helper("disk_metadata.py", "disk_metadata")
X509_METADATA = load_helper("x509_metadata.py", "x509_metadata")
METADATA_GRAPH = load_helper("metadata_graph.py", "metadata_graph")


@dataclass
class ArtifactFile:
    chain: tuple[str, ...]
    data: bytes

    @property
    def name(self) -> str:
        return self.chain[-1].replace("\\", "/").rsplit("/", 1)[-1]

    @property
    def display_path(self) -> str:
        return " -> ".join(self.chain)


@dataclass
class ArtifactIndex:
    by_name: dict[str, list[ArtifactFile]]
    descendants_by_chain: dict[tuple[str, ...], list[ArtifactFile]]


class GameMasterSession:
    """Reuse one HTTP connection for the timed request sequence."""

    def __init__(self, base_url: str):
        parsed = urllib.parse.urlsplit(base_url)
        if parsed.scheme != "http" or not parsed.hostname:
            raise ValueError("GAME_MASTER_PROXY_URL must be an HTTP proxy URL")
        self.base_path = parsed.path
        self.host = parsed.hostname
        self.port = parsed.port or 80
        self.connection: http.client.HTTPConnection | None = None
        self.last_connection_reused = False

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def request(
        self, params: dict[str, str] | None = None, payload: dict | None = None
    ):
        query = urllib.parse.urlencode(params) if params else ""
        path = self.base_path + (f"?{query}" if query else "")
        body = json.dumps(payload).encode() if payload is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        method = "POST" if body is not None else "GET"
        url = f"http://{self.host}:{self.port}{path}"

        self.last_connection_reused = self.connection is not None
        if self.connection is None:
            self.connection = http.client.HTTPConnection(
                self.host, self.port, timeout=30
            )
        try:
            self.connection.request(method, path, body=body, headers=headers)
            response = self.connection.getresponse()
            response_body = response.read()
            response_headers = response.headers
            status = response.status
            reason = response.reason
            will_close = response.will_close
        except Exception:
            self.close()
            raise

        if will_close:
            self.close()
        if not 200 <= status < 300:
            raise urllib.error.HTTPError(
                url,
                status,
                reason,
                response_headers,
                io.BytesIO(response_body),
            )
        return response_body, response_headers


REQUEST_SESSION: GameMasterSession | None = None
PROFILE_REQUESTS = False
REQUEST_TIMINGS: list[dict[str, object]] = []


def request(params: dict[str, str] | None = None, payload: dict | None = None):
    if REQUEST_SESSION is None:
        raise RuntimeError("Game Master session has not been initialized")
    started = time.perf_counter() if PROFILE_REQUESTS else 0.0
    result = REQUEST_SESSION.request(params=params, payload=payload)
    if PROFILE_REQUESTS:
        operation = (
            params.get("op") if params
            else payload.get(
                "op", "submit" if "answers" in payload else "start"
            ) if payload
            else "unknown"
        )
        REQUEST_TIMINGS.append({
            "op": operation,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
            "connection_reused": REQUEST_SESSION.last_connection_reused,
        })
    return result


def collect_files(data: bytes, filename: str, parent: tuple[str, ...] = ()) -> list[ArtifactFile]:
    """Collect files and nested archives in memory, preserving each archive chain."""
    current = ArtifactFile(parent + (filename,), data)
    files = [current]
    if not is_zipfile(io.BytesIO(data)):
        return files
    try:
        archive_type = pyzipper.AESZipFile if pyzipper else ZipFile
        with archive_type(io.BytesIO(data)) as archive:
            if pyzipper:
                archive.setpassword(b"infected")
            for item in archive.infolist():
                if item.is_dir():
                    continue
                # The event's documented archive password is used for encrypted members.
                member = archive.read(
                    item, pwd=b"infected" if item.flag_bits & 0x1 else None
                )
                child = collect_files(member, item.filename, current.chain)
                files.extend(child)
    except (
        BadZipFile,
        RuntimeError,
        pyzipper.BadZipFile if pyzipper else BadZipFile,
    ):
        # Keep malformed archives as targetable byte sequences; raw ZIP fields
        # can still be read even when the central directory cannot be extracted.
        pass
    return files


def index_artifacts(files: list[ArtifactFile]) -> ArtifactIndex:
    """Index names and archive descendants for repeated question lookups."""
    by_name: dict[str, list[ArtifactFile]] = {}
    descendants_by_chain: dict[tuple[str, ...], list[ArtifactFile]] = {}
    for artifact in files:
        by_name.setdefault(artifact.name, []).append(artifact)
        for depth in range(len(artifact.chain)):
            descendants_by_chain.setdefault(
                artifact.chain[:depth], []
            ).append(artifact)
    return ArtifactIndex(by_name, descendants_by_chain)


def descriptor_chain(question: dict) -> tuple[str, ...]:
    descriptor = question.get("artifact", "")
    return tuple(
        segment.strip().replace("\\", "/").rsplit("/", 1)[-1]
        for segment in re.split(r"\s*->\s*", descriptor)
        if segment.strip()
    )


def select_target(
    question: dict,
    files: list[ArtifactFile],
    artifact_index: ArtifactIndex | None = None,
) -> ArtifactFile:
    chain = descriptor_chain(question)
    if not chain:
        raise ValueError(f"Question has no artifact descriptor: {question.get('id')}")
    wanted = chain[-1]
    candidates_by_name = (
        artifact_index.by_name.get(wanted, [])
        if artifact_index is not None
        else [artifact for artifact in files if artifact.name == wanted]
    )
    candidates = [
        artifact for artifact in candidates_by_name
        if artifact.chain[-len(chain):] == chain
    ]
    if not candidates:
        # A descriptor may name the assigned outer file while the requested
        # evidence is a member within it.
        candidates = candidates_by_name
    if not candidates:
        raise ValueError(f"Could not find {wanted!r} for {question.get('id')}")
    if len(candidates) > 1:
        paths = ", ".join(item.display_path for item in candidates)
        raise ValueError(f"Ambiguous artifact {wanted!r}: {paths}")
    return candidates[0]


def evidence_note(
    question: dict,
    target: ArtifactFile,
    files: list[ArtifactFile],
    artifact_index: ArtifactIndex | None = None,
) -> ArtifactFile:
    if not is_zipfile(io.BytesIO(target.data)):
        return target
    descendants = (
        artifact_index.descendants_by_chain.get(target.chain, [])
        if artifact_index is not None
        else [
            artifact for artifact in files
            if len(artifact.chain) > len(target.chain)
            and artifact.chain[:len(target.chain)] == target.chain
        ]
    )
    descendants = [
        artifact for artifact in descendants
        if "note" in artifact.name.lower()
        and not is_zipfile(io.BytesIO(artifact.data))
    ]
    preferred = [item for item in descendants if "evidence" in item.name.lower()]
    matches = preferred or descendants
    if not matches:
        raise ValueError("No evidence-note file found inside the described archive")
    return matches[0]


def named_file(
    question: dict,
    target: ArtifactFile,
    files: list[ArtifactFile],
    artifact_index: ArtifactIndex | None = None,
) -> ArtifactFile:
    """Resolve a file named or described by the question within its archive."""
    descendants = (
        artifact_index.descendants_by_chain.get(target.chain, [])
        if artifact_index is not None
        else [
            artifact for artifact in files
            if len(artifact.chain) > len(target.chain)
            and artifact.chain[:len(target.chain)] == target.chain
        ]
    )
    descendants = [
        artifact for artifact in descendants
        if not is_zipfile(io.BytesIO(artifact.data))
    ]
    text = question.get("question", "")
    explicit_names = re.findall(r"[\w.-]+\.[A-Za-z0-9]{1,8}", text)
    for name in explicit_names:
        matches = [item for item in descendants if item.name == name]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ValueError(f"Ambiguous file name in question: {name}")

    field = requested_field(question)
    if "copy" in field or "copy" in text.lower():
        matches = [
            item for item in descendants
            if "note" in item.name.lower() and "copy" in item.name.lower()
        ]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ValueError("Ambiguous evidence-note copy file")
    if "roster" in field or "roster" in text.lower():
        matches = [item for item in descendants if "roster" in item.name.lower()]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ValueError("Ambiguous roster file")

    return evidence_note(question, target, files, artifact_index)


def synthesis_sha256_order(
    question: dict,
    target: ArtifactFile,
    files: list[ArtifactFile],
    artifact_index: ArtifactIndex | None = None,
) -> str:
    match = re.search(r"\bFiles:\s*(\[[^\]]*\])", question.get("question", ""), re.S)
    if not match:
        raise ValueError("Synthesis question does not list its files")
    names = json.loads(match.group(1))
    package_chain = target.chain[:-1]
    ranked: list[tuple[str, str]] = []
    for name in names:
        candidates_by_name = (
            artifact_index.by_name.get(name, [])
            if artifact_index is not None
            else files
        )
        matches = [
            artifact for artifact in candidates_by_name
            if artifact.name == name
            and artifact.chain[:len(package_chain)] == package_chain
        ]
        if len(matches) != 1:
            raise ValueError(f"Expected one artifact named {name!r}, found {len(matches)}")
        ranked.append((hashlib.sha256(matches[0].data).hexdigest(), name))
    ranked.sort()
    return json.dumps([name for _, name in ranked], ensure_ascii=False, separators=(",", ":"))


def identical_sha256_groups(data: bytes) -> str:
    """Group artifact IDs or member names whose bytes have equal SHA-256."""
    with ZipFile(io.BytesIO(data)) as archive:
        manifests = [
            name for name in archive.namelist()
            if name.rsplit("/", 1)[-1].casefold() == "delivery-manifest.json"
        ]
        groups: dict[str, list[str]] = {}
        if manifests:
            if len(manifests) != 1:
                raise ValueError(
                    f"Expected at most one delivery-manifest.json, found {len(manifests)}"
                )
            manifest = json.loads(archive.read(manifests[0]))
            for artifact in manifest.get("artifacts", []):
                artifact_id = artifact.get("id")
                member_path = artifact.get("path")
                if not artifact_id or not member_path:
                    raise ValueError("Manifest artifact is missing its id or path")
                try:
                    member_data = archive.read(member_path)
                except KeyError as error:
                    raise ValueError(
                        f"Manifest member is missing from archive: {member_path}"
                    ) from error
                digest = hashlib.sha256(member_data).hexdigest()
                groups.setdefault(digest, []).append(artifact_id)
        else:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                member_data = archive.read(member)
                artifact_name = member.filename.rsplit("/", 1)[-1]
                digest = hashlib.sha256(member_data).hexdigest()
                groups.setdefault(digest, []).append(artifact_name)

    result = [sorted(ids) for ids in groups.values() if len(ids) > 1]
    result.sort()
    return json.dumps(result, ensure_ascii=False, separators=(",", ":"))


def jpeg_dimensions(data: bytes) -> str:
    sof_markers = {
        0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    }
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("Input does not start with a JPEG SOI marker")
    position = 2
    while position < len(data):
        if data[position] != 0xFF:
            position += 1
            continue
        while position < len(data) and data[position] == 0xFF:
            position += 1
        if position >= len(data):
            break
        marker = data[position]
        position += 1
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if position + 2 > len(data):
            break
        segment_size = int.from_bytes(data[position:position + 2], "big")
        if segment_size < 2 or position + segment_size > len(data):
            raise ValueError("JPEG segment is truncated")
        if marker in sof_markers:
            height = int.from_bytes(data[position + 3:position + 5], "big")
            width = int.from_bytes(data[position + 5:position + 7], "big")
            return f"{width}x{height}"
        position += segment_size
    raise ValueError("JPEG has no start-of-frame dimensions")


def msi_information(data: bytes) -> dict[str, object]:
    """Read common Windows Installer fields with the system msitools reader."""
    with tempfile.NamedTemporaryFile(suffix=".msi") as package:
        package.write(data)
        package.flush()

        def read_msiinfo(*args: str) -> str:
            completed = subprocess.run(
                ["msiinfo", args[0], package.name, *args[1:]],
                capture_output=True,
                text=True,
            )
            if completed.returncode:
                return ""
            return completed.stdout

        properties: dict[str, str] = {}
        for row in read_msiinfo("export", "Property").splitlines()[3:]:
            columns = row.split("\t", 1)
            if len(columns) == 2:
                properties[columns[0]] = columns[1]

        upgrades: list[str] = []
        for row in read_msiinfo("export", "Upgrade").splitlines()[3:]:
            columns = row.split("\t")
            if columns and columns[0] and columns[0] not in {"UpgradeCode"}:
                upgrades.append(columns[0])

        summary = {}
        for row in read_msiinfo("suminfo").splitlines():
            if ": " in row:
                key, value = row.split(": ", 1)
                summary[key.casefold()] = value
        revision = summary.get("revision number (uuid)", "")
        return {
            "properties": properties,
            "upgrade_codes": sorted(set(upgrades), key=str.casefold),
            "package_code_guid": revision,
            "template": summary.get("template", ""),
        }


def apk_package_name(data: bytes) -> str:
    """Read the application ID from an APK's binary Android manifest."""
    executable = shutil.which("aapt")
    if executable is None:
        raise RuntimeError("APK package-name parsing requires Android build-tools (aapt)")
    with tempfile.NamedTemporaryFile(suffix=".apk") as package:
        package.write(data)
        package.flush()
        result = subprocess.run(
            [executable, "dump", "badging", package.name],
            capture_output=True,
            text=True,
            check=True,
        )
    match = re.search(r"^package:\s+name='([^']+)'", result.stdout, re.M)
    if not match:
        raise ValueError("APK badging output has no package name")
    return match.group(1)


def requested_field(question: dict) -> str:
    return (question.get("id", "") + " " + question.get("question", "")).lower()


def answer_for(
    question: dict,
    files: list[ArtifactFile],
    artifact_index: ArtifactIndex | None = None,
) -> str:
    field = requested_field(question)
    target = select_target(question, files, artifact_index)

    normalized = field.replace("-", "_")
    if "graph.execution_chain_artifact_ids" in field or "graph_execution_chain_artifact_ids" in normalized:
        return json.dumps(
            METADATA_GRAPH.execution_chain_artifact_ids(target, files),
            ensure_ascii=False,
            separators=(",", ":"),
        )
    if "identical_sha256_groups" in normalized:
        return identical_sha256_groups(target.data)
    if re.search(r"\bx509[._]sha256_fingerprint\b", normalized):
        return X509_METADATA.sha256_fingerprint(target.data)
    if re.search(r"\bregistry[._]hive_root_name\b", normalized):
        return REGISTRY_METADATA.hive_root_name(target.data)
    if re.search(r"\bevtx[._]record_count\b", normalized):
        return str(EVTX_METADATA.record_count(target.data))
    if re.search(r"\bprefetch[._]executable_name\b", normalized):
        return PREFETCH_METADATA.executable_name(target.data)
    if re.search(r"\bpcap[._]packet_count\b", normalized):
        return str(PCAP_METADATA.packet_count(target.data))
    if re.search(r"\bdisk[._]partition_start_lba_sequence\b", normalized):
        return json.dumps(
            DISK_METADATA.partition_start_lba_sequence(target.data),
            ensure_ascii=False,
            separators=(",", ":"),
        )
    sqlite_fields = SQLITE_METADATA.inspect_sqlite(target.data) if re.search(
        r"\bsqlite[._](?:page_size_bytes|write_version|read_version|"
        r"reserved_bytes_per_page|max_embedded_payload_fraction|"
        r"min_embedded_payload_fraction|leaf_payload_fraction|"
        r"file_change_counter|database_size_pages|first_freelist_trunk_page|"
        r"total_freelist_pages|schema_cookie|schema_format|"
        r"default_page_cache_size|largest_root_page|text_encoding|"
        r"user_version|incremental_vacuum_mode|application_id|"
        r"version_valid_for|sqlite_version_number)\b",
        normalized,
    ) else None
    if sqlite_fields is not None:
        for key, value in sqlite_fields.items():
            if key in normalized:
                return str(value)
        raise ValueError(f"No SQLite metadata field handler for answer ID {question.get('id')}")
    if "package_name" in normalized and target.name.lower().endswith(".apk"):
        return APK_METADATA.package_name(target.data)
    if "jar" in normalized and "main_class" in normalized:
        return JAR_METADATA.main_class(target.data)
    if "apk" in normalized and "package_name" in normalized:
        return APK_METADATA.package_name(target.data)
    if "elf" in normalized and (
        "e_machine_u16_hex" in normalized or "elf_machine_hex" in normalized
    ):
        return ELF_METADATA.inspect_elf(target.data)["machine_hex"]
    if "macho" in normalized and "cpu_type_set" in normalized:
        return json.dumps(
            MACHO_METADATA.cpu_types(target.data),
            ensure_ascii=False,
            separators=(",", ":"),
        )
    if "ooxml" in field and "external_relationship_targets" in normalized:
        return json.dumps(
            OOXML_METADATA.external_relationship_targets(target.data),
            ensure_ascii=False,
            separators=(",", ":"),
        )
    if "lnk" in field and (
        "target_path_windows" in normalized or "target_path" in normalized
    ):
        return SHORTCUT_METADATA.inspect_lnk(target.data)["target_path_windows"] or "none"
    if "msi" in field or target.name.lower().endswith(".msi"):
        info = msi_information(target.data)
        properties = info["properties"]
        if "product_code" in normalized:
            return properties.get("ProductCode", "")
        if "upgrade_code" in normalized:
            codes = info["upgrade_codes"]
            if "all" in normalized or "list" in normalized or "collision" in normalized:
                return json.dumps(codes, ensure_ascii=False, separators=(",", ":"))
            if len(codes) == 1:
                return codes[0]
            return json.dumps(codes, ensure_ascii=False, separators=(",", ":"))
        if "package_code" in normalized or "revision_number" in normalized:
            return info["package_code_guid"]
        if "product_version" in normalized:
            return properties.get("ProductVersion", "")
        if "product_name" in normalized:
            return properties.get("ProductName", "")
        if "manufacturer" in normalized or "manufacturer" in field:
            return properties.get("Manufacturer", "")
        if "template" in normalized or "platform" in normalized:
            return info["template"]

    if "filename" in field and target.name.lower().endswith(".zip"):
        target = named_file(question, target, files, artifact_index)

    data = target.data
    if "primary_audio_codec_name" in normalized:
        return MEDIA_METADATA.primary_audio_codec_name(
            data, suffix=Path(target.name).suffix or ".bin"
        )
    if "primary_video_dimensions" in normalized:
        return VIDEO_METADATA.primary_video_dimensions(
            data, suffix=Path(target.name).suffix or ".bin"
        )
    if "synthesis_sha256_order" in normalized:
        return synthesis_sha256_order(question, target, files, artifact_index)
    if "mvid_guid" in field or "dotnet-mvid-guid" in field:
        return PE_METADATA.inspect_dotnet_mvid(data)
    if "eocd_total_entries" in field or "eocd-total-entries" in field:
        return str(ZIP_METADATA.inspect_zip(data)["eocd_total_entries"])
    if "central_directory_member_names" in field or "central-directory-member-names" in field:
        names = ZIP_METADATA.inspect_zip(data)["central_directory_member_names"]
        return json.dumps(names, ensure_ascii=False, separators=(",", ":"))
    zip_fields = {
        "eocd_entries_on_disk": "eocd_entries_on_disk",
        "eocd_disk_number": "eocd_disk_number",
        "eocd_central_directory_disk": "eocd_central_directory_disk",
        "eocd_central_directory_size": "eocd_central_directory_size",
        "eocd_central_directory_offset": "eocd_central_directory_offset",
        "eocd_comment_length": "eocd_comment_length",
    }
    for token, key in zip_fields.items():
        if token in normalized:
            return str(ZIP_METADATA.inspect_zip(data)[key])

    if "md5" in field:
        return hashlib.md5(data).hexdigest()
    if "sha1" in field:
        return hashlib.sha1(data).hexdigest()
    if "sha256" in field:
        return hashlib.sha256(data).hexdigest()
    if "email" in field and "message_id" in normalized:
        message = BytesParser(policy=policy.default).parsebytes(data)
        message_id = message.get("Message-ID")
        return str(message_id).strip() if message_id is not None else "none"
    if "version_original_filename" in field or "version-original-filename" in field:
        version_info = PE_METADATA.inspect_version_info(data)
        return next(
            (
                value for key, value in version_info.items()
                if key.casefold() == "originalfilename"
            ),
            "none",
        )
    if "magic_prefix_hex" in normalized:
        match = re.search(r"magic[_-]prefix[_-]hex[_-](\d+)", normalized)
        count = int(match.group(1)) if match else 16
        return data[:count].hex()
    if "utf8_bom_present" in field or "utf8-bom-present" in field:
        return str(data.startswith(b"\xef\xbb\xbf")).lower()
    if "size_bytes" in field or "size-bytes" in field:
        return str(len(data))
    if "filename" in field or "base_filename" in field:
        return target.name
    if "jpeg" in field and "dimensions" in field:
        return jpeg_dimensions(data)
    if "png" in field and "dimensions" in field:
        if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            return "none"
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        return f"{width}x{height}"
    if "pdf" in field and "header_version" in field:
        match = re.match(rb"%PDF-([0-9.]+)", data)
        return match.group(1).decode("ascii") if match else "none"
    if "entry-point" in field or "entry_point" in field:
        return str(PE_METADATA.inspect_pe(data)["address_of_entry_point_rva_hex"])
    if "machine" in field and "pe" in field:
        pe = PE_METADATA.inspect_pe(data)
        return f"0x{int(pe['machine']):04x}"
    raise ValueError(f"No metadata field handler for answer ID {question.get('id')}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("challenge", help="challenge ID from the Game Master")
    parser.add_argument("--retry", action="store_true")
    parser.add_argument("--run-for-time", action="store_true")
    parser.add_argument(
        "--warm-connection",
        action="store_true",
        help="check status before retry and reuse that connection for the attempt",
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="report per-request and local processing times after completion",
    )
    parser.add_argument(
        "--records",
        type=Path,
        default=Path(__file__).with_name("attempt-records"),
    )
    args = parser.parse_args()

    if args.warm_connection and not args.retry:
        parser.error("--warm-connection requires --retry")
    global PROFILE_REQUESTS, REQUEST_SESSION
    PROFILE_REQUESTS = args.profile
    REQUEST_SESSION = GameMasterSession(os.environ["GAME_MASTER_PROXY_URL"])

    if args.warm_connection:
        warm_raw, _ = request({
            "op": "status",
            "challenge": args.challenge,
        })
        warm_status = json.loads(warm_raw)
        if warm_status.get("status") == "pending" or warm_status.get("result") == "pending":
            raise RuntimeError("Current attempt has unresolved scoring status")
        deadline = warm_status.get("deadline")
        if deadline:
            parsed_deadline = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
            required_ids = set(warm_status.get("answer_ids", []))
            accepted_ids = set(warm_status.get("accepted_ids", []))
            completed = (
                warm_status.get("result") == "CORRECT"
                and required_ids
                and required_ids <= accepted_ids
            )
            if parsed_deadline > datetime.now(timezone.utc) and not completed:
                raise RuntimeError("Current attempt still has an active deadline")

    payload = {"challenge": args.challenge}
    if args.retry:
        payload["op"] = "retry"
    if args.run_for_time:
        payload["run_for_time"] = True
    start_raw, _ = request(payload=payload)
    start_response = json.loads(start_raw)
    if not start_response.get("attempt_id") or not start_response.get("answer_ids"):
        # A solved legacy attempt can return only CORRECT plus its questions
        # from start. Recover its full assignment and accepted IDs via status.
        status_raw, _ = request({
            "op": "status",
            "challenge": args.challenge,
        })
        status_response = json.loads(status_raw)
        if not status_response.get("attempt_id") or not status_response.get("answer_ids"):
            raise RuntimeError(
                "Game Master start response and current status lack attempt metadata"
            )
        start_response = {**start_response, **status_response}
    attempt = start_response.get("attempt_id", "unknown-attempt")
    record = args.records / args.challenge / attempt
    record.mkdir(parents=True, exist_ok=True)
    (record / "start-response.json").write_text(
        json.dumps(start_response, indent=2, ensure_ascii=False) + "\n"
    )

    artifact_specs = start_response.get("artifacts") or []
    deliveries = list(enumerate(artifact_specs)) if artifact_specs else [(None, {})]
    downloaded: list[tuple[Path, str, str]] = []
    all_files: list[ArtifactFile] = []
    artifact_processing_ms = 0.0
    # Legacy timed-by-default routes omit run_for_time or report it as false.
    # Their server-issued deadline still marks the download as speed-critical.
    timed_attempt = (
        start_response.get("run_for_time") is True
        or start_response.get("deadline") is not None
    )
    for index, spec in deliveries:
        params = {"op": "artifact", "challenge": args.challenge}
        if index is not None:
            params["delivery"] = str(index)
        artifact_raw, artifact_headers = request(params)
        disposition = artifact_headers.get("Content-Disposition", "")
        name_match = re.search(
            r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', disposition, re.I
        )
        artifact_name = spec.get("filename") or (
            urllib.parse.unquote(name_match.group(1))
            if name_match else "artifact.bin"
        )
        artifact_name = Path(artifact_name.replace("\\", "/")).name
        if index is not None:
            destination = record / f"delivery-{index + 1}" / artifact_name
        else:
            destination = record / artifact_name
        processing_started = time.perf_counter()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(artifact_raw)
        artifact_hash = ""
        # Bundle integrity is not an answer; keep this optional check off the
        # timed path. Per-question hashes are still computed from member bytes.
        if not timed_attempt:
            artifact_hash = hashlib.sha256(artifact_raw).hexdigest()
            expected_hash = spec.get("sha256") or (
                start_response.get("sha256") if index is None else None
            )
            if expected_hash and expected_hash != artifact_hash:
                raise ValueError(f"Assigned artifact SHA-256 does not match {artifact_name}")
        downloaded.append((destination, artifact_hash, artifact_name))
        all_files.extend(collect_files(artifact_raw, artifact_name))
        artifact_processing_ms += (time.perf_counter() - processing_started) * 1000

    answer_started = time.perf_counter()
    artifact_index = index_artifacts(all_files)
    questions = start_response.get("questions", [])
    with ThreadPoolExecutor(max_workers=min(8, len(questions) or 1)) as executor:
        answer_values = executor.map(
            lambda question: answer_for(question, all_files, artifact_index),
            questions,
        )
        answers = {
            question["id"]: answer
            for question, answer in zip(questions, answer_values)
        }
    answer_build_ms = (time.perf_counter() - answer_started) * 1000
    if set(answers) != set(start_response.get("answer_ids", [])):
        raise ValueError("Candidate answer IDs do not match the Game Master response")
    (record / "candidate-answers.json").write_text(
        json.dumps(answers, indent=2, ensure_ascii=False) + "\n"
    )

    accepted_before = set(start_response.get("accepted_ids", []))
    if not args.retry and not accepted_before:
        # start reconnects to the current attempt; inspect accepted partial
        # answers before submitting. retry creates a new attempt with no carryover.
        # Artifact delivery may leave a stale keep-alive connection behind.
        REQUEST_SESSION.close()
        before_raw, _ = request({
            "op": "status",
            "challenge": args.challenge,
        })
        before = json.loads(before_raw)
        accepted_before = set(before.get("accepted_ids", []))
    pending = {
        answer_id: answer
        for answer_id, answer in answers.items()
        if answer_id not in accepted_before
    }
    graph_ids = {
        question["id"]
        for question in questions
        if "graph.execution_chain_artifact_ids" in requested_field(question)
        or "graph_execution_chain_artifact_ids" in requested_field(question).replace("-", "_")
    }
    batches = []
    ordinary = {key: value for key, value in pending.items() if key not in graph_ids}
    if ordinary:
        batches.append(ordinary)
    batches.extend({key: pending[key]} for key in pending if key in graph_ids)
    submission_results = []
    accepted_from_submit: set[str] = set()
    for batch in batches:
        result_raw, _ = request(payload={
            "challenge": args.challenge,
            "answers": batch,
        })
        batch_result = json.loads(result_raw)
        accepted_from_submit.update(batch_result.get("accepted_ids", []))
        submission_results.append({
            "submitted_ids": sorted(batch),
            "result": batch_result.get("result"),
            "status": batch_result.get("status"),
            "accepted_ids": sorted(batch_result.get("accepted_ids", [])),
            "remaining": batch_result.get("remaining"),
        })
    result = (
        {"result": "already_accepted"}
        if not submission_results
        else batch_result
    )
    status_raw, _ = request({
        "op": "status",
        "challenge": args.challenge,
    })
    status = json.loads(status_raw)
    (record / "status-response.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n"
    )
    manifest = [
        {"path": str(path.relative_to(record)), "sha256": digest or None}
        for path, digest, _ in downloaded
    ]
    (record / "artifact-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    accepted = accepted_before | accepted_from_submit | set(status.get("accepted_ids", []))
    if len(submission_results) <= 1:
        (record / "submission-result.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        )
    else:
        (record / "submission-result.json").write_text(
            json.dumps({
                "result": result.get("result"),
                "status": result.get("status"),
                "submissions": submission_results,
                "accepted_ids": sorted(accepted),
                "unaccepted_ids": sorted(set(answers) - accepted),
            }, indent=2, ensure_ascii=False) + "\n"
        )
    print(json.dumps({
        "attempt_id": attempt,
        "mode": start_response.get("mode"),
        "deadline": start_response.get("deadline"),
        "run_for_time": start_response.get("run_for_time"),
        "hall_of_fame_eligible": start_response.get("hall_of_fame_eligible"),
        "ranked_attempts_remaining": status.get("ranked_attempts_remaining"),
        "unique_attempts_remaining": status.get("unique_attempts_remaining"),
        "regular_variants_remaining": status.get("regular_variants_remaining"),
        "variant_fresh": start_response.get("variant_fresh"),
        "artifact_sha256": [digest for _, digest, _ in downloaded if digest],
        "result": result.get("result"),
        "scoring_status": result.get("status"),
        "accepted_before_submit": sorted(accepted_before),
        "submitted_ids": sorted(pending),
        "submission_batches": submission_results,
        "accepted_ids": sorted(accepted),
        "unaccepted_ids": sorted(set(answers) - accepted),
    }, ensure_ascii=False, indent=2))
    if args.profile:
        print(json.dumps({
            "profile": {
                "requests": REQUEST_TIMINGS,
                "artifact_processing_ms": round(artifact_processing_ms, 3),
                "answer_build_ms": round(answer_build_ms, 3),
            }
        }, ensure_ascii=False, indent=2))
    REQUEST_SESSION.close()


if __name__ == "__main__":
    main()
