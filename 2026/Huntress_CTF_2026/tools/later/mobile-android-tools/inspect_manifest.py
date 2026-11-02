#!/usr/bin/env python3
"""Report exported Android activities and the URI routes in their manifest."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


def xmltree(apk: Path, aapt: str = "aapt") -> str:
    executable = shutil.which(aapt)
    if executable is None:
        raise FileNotFoundError(
            f"Could not find {aapt!r}; install Android build-tools or pass --aapt"
        )
    return subprocess.check_output(
        [executable, "dump", "xmltree", str(apk), "AndroidManifest.xml"],
        text=True,
        errors="replace",
    )


def parse_xmltree(text: str) -> dict:
    """Build a small tree from ``aapt dump xmltree`` without decoding the APK."""
    root = {"tag": "#document", "attributes": {}, "children": []}
    stack: list[tuple[int, dict]] = [(-1, root)]

    for line in text.splitlines():
        element = re.match(r"^(\s*)E:\s*([^\s(]+)", line)
        if element:
            indent = len(element.group(1))
            while stack and stack[-1][0] >= indent:
                stack.pop()
            node = {
                "tag": element.group(2),
                "attributes": {},
                "children": [],
            }
            stack[-1][1]["children"].append(node)
            stack.append((indent, node))
            continue

        attribute = re.match(r"^\s*A:\s*([^\s(=]+)(?:\([^)]*\))?=(.*)$", line)
        if not attribute or len(stack) == 0:
            continue
        name, raw_value = attribute.groups()
        quoted = re.search(r'"((?:\\.|[^"\\])*)"', raw_value)
        if quoted:
            value: str | bool = json.loads(f'"{quoted.group(1)}"')
        elif name == "android:exported":
            number = re.search(r"0x([0-9a-fA-F]+)", raw_value)
            value = bool(int(number.group(1), 16)) if number else None
        else:
            value = raw_value.strip()
        stack[-1][1]["attributes"][name] = value

    return root


def walk(node: dict):
    yield node
    for child in node["children"]:
        yield from walk(child)


def manifest_summary(text: str) -> dict:
    tree = parse_xmltree(text)
    manifest = next((node for node in tree["children"] if node["tag"] == "manifest"), None)
    package = manifest["attributes"].get("package", "") if manifest else ""
    activities = []

    for node in walk(tree):
        if node["tag"] not in {"activity", "activity-alias"}:
            continue
        attributes = node["attributes"]
        name = attributes.get("android:name", "")
        if name.startswith("."):
            name = package + name
        elif name and "." not in name:
            name = f"{package}.{name}" if package else name

        filters = []
        for child in node["children"]:
            if child["tag"] != "intent-filter":
                continue
            actions = []
            categories = []
            data = []
            for item in child["children"]:
                item_attributes = item["attributes"]
                if item["tag"] == "action":
                    actions.append(item_attributes.get("android:name", ""))
                elif item["tag"] == "category":
                    categories.append(item_attributes.get("android:name", ""))
                elif item["tag"] == "data":
                    data.append({
                        key.removeprefix("android:"): value
                        for key, value in item_attributes.items()
                        if key.startswith("android:")
                    })
            filters.append({
                "actions": actions,
                "categories": categories,
                "data": data,
            })

        activities.append({
            "name": name,
            "exported": attributes.get("android:exported"),
            "permission": attributes.get("android:permission"),
            "intent_filters": filters,
        })
    return {"package": package, "activities": activities}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    parser.add_argument("--aapt", default="aapt", help="aapt executable name or path")
    args = parser.parse_args()
    print(json.dumps(manifest_summary(xmltree(args.apk, args.aapt)), indent=2))


if __name__ == "__main__":
    main()
