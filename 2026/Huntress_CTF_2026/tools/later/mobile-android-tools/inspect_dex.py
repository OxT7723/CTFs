#!/usr/bin/env python3
"""List DEX classes and disassemble selected methods from an APK."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    parser.add_argument("--class-regex", default=".*")
    parser.add_argument("--method-regex", default=".*")
    args = parser.parse_args()

    from androguard.misc import AnalyzeAPK
    from loguru import logger

    logger.disable("androguard")

    apk, dex_files, _ = AnalyzeAPK(str(args.apk))
    print(f"Package: {apk.get_package()}")
    for dex in dex_files:
        for klass in dex.get_classes():
            class_name = klass.get_name()
            if not re.search(args.class_regex, class_name):
                continue
            for method in klass.get_methods():
                if not re.search(args.method_regex, method.get_name()):
                    continue
                print(f"\n{class_name}->{method.get_name()}{method.get_descriptor()}")
                for instruction in method.get_instructions():
                    output = instruction.get_output()
                    suffix = f" {output}" if output else ""
                    print(f"  {instruction.get_name()}{suffix}")


if __name__ == "__main__":
    main()
