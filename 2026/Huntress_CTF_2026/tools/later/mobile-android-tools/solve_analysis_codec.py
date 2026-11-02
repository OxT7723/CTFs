#!/usr/bin/env python3
"""Statically evaluate the app's reachable Release.code DEX call chain."""

from __future__ import annotations

import re
import subprocess
import tempfile
import zipfile
from pathlib import Path


MASK32 = (1 << 32) - 1
MASK64 = (1 << 64) - 1


def signed(value: int, bits: int) -> int:
    mask = (1 << bits) - 1
    value &= mask
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def descriptor_widths(descriptor: str) -> list[int]:
    params = descriptor.split("(", 1)[1].split(")", 1)[0].replace(" ", "")
    widths = []
    index = 0
    while index < len(params):
        if params[index] == "[":
            while params[index] == "[":
                index += 1
            if params[index] == "L":
                index = params.index(";", index) + 1
            else:
                index += 1
            widths.append(1)
        elif params[index] == "L":
            index = params.index(";", index) + 1
            widths.append(1)
        else:
            widths.append(2 if params[index] in "JD" else 1)
            index += 1
    return widths


class DexEvaluator:
    def __init__(
        self,
        apk_path: Path,
        split_assets: dict[str, bytes] | None = None,
        verify_dex_integrity: bool = True,
    ):
        from loguru import logger
        from androguard.misc import AnalyzeAPK
        from androguard.core.dex import DEX

        logger.disable("androguard")
        self.apk_path = apk_path
        self.split_assets = split_assets or {}
        self.apk_assets = {}
        self.static_fields = {}
        _, dex_files, _ = AnalyzeAPK(str(apk_path))
        self.methods = {}
        for dex in dex_files:
            for klass in dex.get_classes():
                for method in klass.get_methods():
                    key = (method.get_class_name(), method.get_name(), method.get_descriptor())
                    self.methods[key] = method
        with zipfile.ZipFile(apk_path) as archive:
            for member in archive.infolist():
                if member.is_dir() or not member.filename.startswith("assets/"):
                    continue
                asset_name = member.filename.removeprefix("assets/")
                data = archive.read(member)
                self.apk_assets[asset_name] = data
                if not asset_name.lower().endswith(".dex"):
                    continue
                from decode_puzzle_assets import dex_strings

                dex_strings(data, verify_integrity=verify_dex_integrity)
                secondary = DEX(data)
                for klass in secondary.get_classes():
                    for method in klass.get_methods():
                        key = (method.get_class_name(), method.get_name(), method.get_descriptor())
                        self.methods[key] = method

    @staticmethod
    def _typed(operands, kind: int) -> list[int]:
        return [int(item[1]) for item in operands if len(item) == 2 and int(item[0]) == kind]

    @staticmethod
    def _references(operands) -> list[str]:
        return [
            item[2]
            for item in operands
            if len(item) == 3 and isinstance(item[2], str) and "->" in item[2]
        ]

    @staticmethod
    def _strings(operands) -> list[str]:
        return [
            item[2]
            for item in operands
            if len(item) == 3 and isinstance(item[2], str) and "->" not in item[2]
        ]

    def _invoke(self, reference: str, registers: list[int], is_static: bool, values):
        class_name, suffix = reference.split("->", 1)
        name, descriptor = suffix.split("(", 1)
        descriptor = "(" + descriptor
        widths = descriptor_widths(descriptor)
        cursor = 0
        receiver = None
        if not is_static:
            receiver = values[registers[0]]
            cursor = 1
        args = []
        for width in widths:
            if cursor >= len(registers):
                raise ValueError(
                    f"Invoke register mismatch for {reference}: "
                    f"registers={registers}, widths={widths}, static={is_static}"
                )
            args.append(values[registers[cursor]])
            cursor += width

        if class_name.endswith("/Assets;") and name == "readSplit":
            asset_name = str(args[0])
            try:
                return [signed(value, 8) for value in self.split_assets[asset_name]]
            except KeyError as error:
                raise ValueError(
                    f"Split asset {asset_name!r} was not found in the APK set"
                ) from error
        if class_name.endswith("/Assets;") and name == "read":
            asset_name = str(args[0])
            try:
                return [signed(value, 8) for value in self.apk_assets[asset_name]]
            except KeyError as error:
                raise ValueError(
                    f"Asset {asset_name!r} was not found in the APK"
                ) from error
        if class_name == "Ljava/nio/ByteBuffer;" and name == "wrap":
            data, offset, length = args
            return (
                "byte-buffer",
                bytes(value & 0xFF for value in data)[offset : offset + length],
            )
        if class_name == "Ldalvik/system/InMemoryDexClassLoader;" and name == "<init>":
            return None

        key = (class_name, name, descriptor)
        if key in self.methods:
            method = self.methods[key]
            code = method.get_code()
            if code is None:
                if "native" in method.get_access_flags_string().lower():
                    if name == "nativeShare" and len(args) in {1, 2}:
                        return self._native_share(*args)
                raise ValueError(f"Cannot evaluate DEX method {reference}")
            call_args = args if is_static else [receiver, *args]
            return self.execute(method, call_args)

        if class_name == "Ljava/lang/StringBuilder;":
            if name == "<init>":
                return None
            if name == "append":
                value = args[0]
                receiver.append(chr(value & 0xFFFF) if descriptor.startswith("(C)") else str(value))
                return receiver
            if name == "toString":
                return "".join(receiver)
        if class_name == "Ljava/lang/String;" and name == "charAt":
            return ord(receiver[args[0]])
        if class_name == "Ljava/lang/String;" and name == "indexOf":
            return receiver.find(chr(args[0]))
        if class_name == "Ljava/lang/String;" and name == "substring":
            return receiver[args[0] :]
        if class_name == "Ljava/lang/Class;" and name == "forName":
            descriptor = "L" + args[0].replace(".", "/") + ";"
            return ("class", descriptor)
        if class_name == "Ljava/lang/Class;" and name == "getClassLoader":
            return ("class-loader",)
        if class_name == "Ljava/lang/ClassLoader;" and name == "loadClass":
            return ("class", "L" + str(args[0]).replace(".", "/") + ";")
        if class_name == "Ljava/lang/Class;" and name == "getDeclaredMethod":
            if not isinstance(receiver, tuple) or receiver[0] != "class":
                raise ValueError(f"Invalid reflected class receiver: {receiver!r}")
            parameter_types = args[1]
            parameter_descriptor = "".join(
                item[1] if isinstance(item, tuple) and item[0] == "class" else str(item)
                for item in parameter_types
            )
            matches = [
                key for key in self.methods
                if key[0] == receiver[1]
                and key[1] == args[0]
                and key[2].startswith(f"({parameter_descriptor})")
            ]
            if len(matches) != 1:
                raise ValueError(f"Could not resolve reflected method {receiver[1]}->{args[0]}")
            return ("method", matches[0])
        if class_name == "Ljava/lang/reflect/Method;" and name == "invoke":
            if not isinstance(receiver, tuple) or receiver[0] != "method":
                raise ValueError(f"Invalid reflected method receiver: {receiver!r}")
            method_key = receiver[1]
            method = self.methods[method_key]
            reflected_args = [
                item[1] if isinstance(item, tuple) and item[0] == "boxed-long" else item
                for item in args[1]
            ]
            if "static" in method.get_access_flags_string():
                call_args = reflected_args
            else:
                call_args = [args[0], *reflected_args]
            value = self.execute(method, call_args)
            return ("boxed-long", value) if method_key[2].endswith(")J") else value
        if class_name == "Ljava/lang/Long;" and name == "valueOf":
            return ("boxed-long", args[0])
        if class_name == "Ljava/lang/Long;" and name == "longValue":
            if not isinstance(receiver, tuple) or receiver[0] != "boxed-long":
                raise ValueError(f"Invalid boxed Long receiver: {receiver!r}")
            return receiver[1]
        raise ValueError(f"Unsupported external DEX call: {reference}")

    def _native_share(self, argument: int, integrity_word: int | None = None) -> int:
        """Emulate the JNI arithmetic from x86_64 machine code without loading it."""
        with zipfile.ZipFile(self.apk_path) as archive, tempfile.TemporaryDirectory() as temp:
            libraries = [
                member
                for member in archive.infolist()
                if not member.is_dir() and member.filename.endswith(".so")
            ]
            if len(libraries) != 1:
                raise ValueError(f"Expected one native library, found {len(libraries)}")
            library = Path(temp) / "libarena.so"
            library.write_bytes(archive.read(libraries[0]))
            symbols = subprocess.run(
                ["nm", "-D", "--defined-only", str(library)],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            ).stdout.splitlines()
            names = [
                fields[-1]
                for line in symbols
                if (fields := line.split())
                and "nativeShare" in fields[-1]
            ]
            if len(names) != 1:
                raise ValueError(f"Expected one nativeShare symbol, found {names}")
            symbol = names[0]
            disassembly = subprocess.run(
                ["objdump", "-d", "-M", "intel", str(library)],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            ).stdout
        marker = f"<{symbol}>:"
        if marker not in disassembly:
            raise ValueError(f"Native disassembly omitted {symbol}")
        body = disassembly.split(marker, 1)[1]
        instructions = []
        for line in body.splitlines():
            if re.search(r"<[^>]+>:$", line.strip()):
                break
            match = re.match(r"^\s*([0-9a-f]+):\s*(.*)$", line)
            if not match:
                continue
            columns = [column.strip() for column in match.group(2).split("\t") if column.strip()]
            # Objdump wraps long immediates onto continuation rows containing
            # only an address and raw bytes. They are data, not instructions.
            if len(columns) < 2 or not re.match(r"^[a-z][a-z0-9.]*\b", columns[-1]):
                continue
            parts = columns[-1].split(None, 1)
            instructions.append(
                (int(match.group(1), 16), parts[0], parts[1] if len(parts) > 1 else "")
            )

        registers = {"rdx": signed(argument, 64)}
        if integrity_word is not None:
            registers["rcx"] = signed(integrity_word, 64)
        aliases = {
            "rax": ("rax", 64), "eax": ("rax", 32), "ax": ("rax", 16), "al": ("rax", 8),
            "rbx": ("rbx", 64), "ebx": ("rbx", 32), "bx": ("rbx", 16), "bl": ("rbx", 8),
            "rcx": ("rcx", 64), "ecx": ("rcx", 32), "cx": ("rcx", 16), "cl": ("rcx", 8),
            "rdx": ("rdx", 64), "edx": ("rdx", 32), "dx": ("rdx", 16), "dl": ("rdx", 8),
            "rsi": ("rsi", 64), "esi": ("rsi", 32), "si": ("rsi", 16), "sil": ("rsi", 8),
            "rdi": ("rdi", 64), "edi": ("rdi", 32), "di": ("rdi", 16), "dil": ("rdi", 8),
            "rbp": ("rbp", 64), "ebp": ("rbp", 32), "bp": ("rbp", 16), "bpl": ("rbp", 8),
            "rsp": ("rsp", 64), "esp": ("rsp", 32), "sp": ("rsp", 16), "spl": ("rsp", 8),
        }

        def read(operand: str) -> int:
            operand = operand.strip().lower()
            if operand in aliases:
                base, width = aliases[operand]
                value = registers.get(base, 0)
                return value & ((1 << width) - 1)
            return int(operand, 0)

        def write(operand: str, value: int) -> None:
            operand = operand.strip().lower()
            if operand not in aliases:
                raise ValueError(f"Unsupported native destination {operand}")
            base, width = aliases[operand]
            value &= (1 << width) - 1
            if width == 32:
                registers[base] = signed(value, 64)
            elif width == 64:
                registers[base] = signed(value, 64)
            else:
                mask = (1 << width) - 1
                registers[base] = signed((registers.get(base, 0) & ~mask) | value, 64)

        def rotate(value: int, shift: int, left: bool) -> int:
            shift &= 63
            value &= MASK64
            if not shift:
                return signed(value, 64)
            if left:
                return signed((value << shift) | (value >> (64 - shift)), 64)
            return signed((value >> shift) | (value << (64 - shift)), 64)

        address_to_index = {address: index for index, (address, _, _) in enumerate(instructions)}
        flags = {"equal": False, "less": False}
        pc = 0
        steps = 0
        while pc < len(instructions):
            steps += 1
            if steps > 100_000:
                raise ValueError("Native instruction limit exceeded")
            _, opcode, operand_text = instructions[pc]
            operands = [value.strip() for value in operand_text.split(",")] if operand_text else []
            next_pc = pc + 1
            if opcode in {"endbr64", "nop", "push", "pop", "leave"}:
                pc = next_pc
                continue
            if opcode == "ret":
                if "rax" not in registers:
                    raise ValueError("Native function returned without setting RAX")
                return signed(registers["rax"], 64)
            if opcode == "cmp":
                left, right = read(operands[0]), read(operands[1])
                width = aliases[operands[0].strip().lower()][1] if operands[0].strip().lower() in aliases else 64
                flags = {
                    "equal": left == right,
                    "less": signed(left, width) < signed(right, width),
                }
                pc = next_pc
                continue
            if opcode in {"je", "jz", "jne", "jnz", "jl", "jge", "jle", "jg"}:
                take = {
                    "je": flags["equal"],
                    "jz": flags["equal"],
                    "jne": not flags["equal"],
                    "jnz": not flags["equal"],
                    "jl": flags["less"],
                    "jge": not flags["less"],
                    "jle": flags["less"] or flags["equal"],
                    "jg": not flags["less"] and not flags["equal"],
                }[opcode]
                if take:
                    target = int(operands[0].split()[0], 16)
                    if target not in address_to_index:
                        raise ValueError(f"Native branch target {target:#x} was not disassembled")
                    next_pc = address_to_index[target]
                pc = next_pc
                continue
            if opcode in {"mov", "movabs"}:
                write(operands[0], read(operands[1]))
            elif opcode == "movzx":
                write(operands[0], read(operands[1]))
            elif opcode in {"add", "sub", "xor", "and", "or", "imul"}:
                left, right = read(operands[0]), read(operands[-1])
                result = {
                    "add": lambda: left + right,
                    "sub": lambda: left - right,
                    "xor": lambda: left ^ right,
                    "and": lambda: left & right,
                    "or": lambda: left | right,
                    "imul": lambda: left * right,
                }[opcode]()
                write(operands[0], result)
            elif opcode in {"rol", "ror"}:
                write(operands[0], rotate(read(operands[0]), read(operands[1]), opcode == "rol"))
            elif opcode in {"shl", "sal", "shr", "sar"}:
                value, shift = read(operands[0]), read(operands[1]) & 63
                if opcode in {"shl", "sal"}:
                    result = value << shift
                elif opcode == "shr":
                    result = (value & MASK64) >> shift
                else:
                    result = value >> shift
                write(operands[0], result)
            else:
                raise ValueError(f"Unsupported native opcode: {opcode} {operand_text}")
            pc = next_pc
        raise ValueError(f"No return instruction in native method {symbol}")

    def execute(self, method, arguments):
        code = method.get_code()
        instructions = list(code.get_bc().get_instructions())
        offsets = []
        by_offset = {}
        offset = 0
        for index, instruction in enumerate(instructions):
            offsets.append(offset)
            by_offset[offset] = index
            offset += instruction.get_length()

        values = [None] * code.get_registers_size()
        descriptor = method.get_descriptor()
        widths = descriptor_widths(descriptor)
        incoming_words = sum(widths)
        if "static" not in method.get_access_flags_string():
            incoming_words += 1
        register = len(values) - incoming_words
        arg_index = 0
        if "static" not in method.get_access_flags_string():
            values[register] = arguments[0]
            register += 1
            arg_index = 1
        for argument, width in zip(arguments[arg_index:], widths):
            values[register] = argument
            register += width

        result = None
        pc = 0
        steps = 0
        while pc < len(instructions):
            steps += 1
            if steps > 100_000:
                raise ValueError(f"DEX execution limit exceeded in {method.get_name()}")
            instruction = instructions[pc]
            name = instruction.get_name()
            operands = instruction.get_operands()
            regs = self._typed(operands, 0)
            literals = self._typed(operands, 1)
            branch_offsets = self._typed(operands, 3)
            strings = self._strings(operands)
            references = self._references(operands)
            next_pc = pc + 1

            if name == "const-class":
                descriptor = next(
                    value
                    for value in self._strings(operands)
                    if value.startswith("L") and value.endswith(";")
                )
                values[regs[0]] = ("class", descriptor)
            elif name.startswith("const-wide"):
                values[regs[0]] = literals[-1]
            elif name.startswith("const-string"):
                values[regs[0]] = strings[0]
            elif name.startswith("const"):
                values[regs[0]] = signed(literals[-1], 32)
            elif name.startswith("move-result"):
                values[regs[0]] = result
            elif name.startswith("move"):
                values[regs[0]] = values[regs[1]]
            elif name == "new-instance":
                values[regs[0]] = []
            elif name == "new-array":
                values[regs[0]] = [None] * values[regs[1]]
            elif name == "array-length":
                values[regs[0]] = len(values[regs[1]])
            elif name in {"aput", "aput-wide", "aput-object", "aput-byte"}:
                value = values[regs[0]]
                if name == "aput-byte":
                    value = signed(value, 8)
                values[regs[1]][values[regs[2]]] = value
            elif name in {"aget", "aget-wide", "aget-object", "aget-byte"}:
                value = values[regs[1]][values[regs[2]]]
                if name == "aget-byte":
                    value = signed(value, 8)
                values[regs[0]] = value
            elif name.startswith("invoke-"):
                reference = references[-1]
                is_static = name.startswith("invoke-static")
                result = self._invoke(reference, regs, is_static, values)
            elif name == "sput-object":
                self.static_fields[references[-1]] = values[regs[0]]
            elif name == "sget-object":
                reference = references[-1]
                if reference.startswith("Ljava/lang/Long;->TYPE"):
                    values[regs[0]] = ("class", "J")
                else:
                    values[regs[0]] = self.static_fields.get(reference)
            elif name in {
                "xor-long/2addr",
                "and-long/2addr",
                "mul-long/2addr",
                "add-long/2addr",
                "or-long/2addr",
                "shl-long/2addr",
                "shr-long/2addr",
                "ushr-long/2addr",
            }:
                left, right = values[regs[0]], values[regs[1]]
                op = name.split("-")[0]
                value = {
                    "xor": lambda: left ^ right,
                    "and": lambda: left & right,
                    "mul": lambda: left * right,
                    "add": lambda: left + right,
                    "or": lambda: left | right,
                    "shl": lambda: left << (right & 63),
                    "shr": lambda: left >> (right & 63),
                    "ushr": lambda: (left & MASK64) >> (right & 63),
                }[op]()
                values[regs[0]] = signed(value, 64)
            elif name in {"xor-int", "and-int", "or-int", "mul-int", "add-int", "sub-int"}:
                left, right = values[regs[1]], values[regs[2]]
                op = name.split("-")[0]
                value = {
                    "xor": lambda: left ^ right,
                    "and": lambda: left & right,
                    "or": lambda: left | right,
                    "mul": lambda: left * right,
                    "add": lambda: left + right,
                    "sub": lambda: left - right,
                }[op]()
                values[regs[0]] = signed(value, 32)
            elif name.endswith("-int/2addr") and name != "ushr-int/2addr":
                left, right = values[regs[0]], values[regs[1]]
                op = name.split("-")[0]
                value = {
                    "xor": lambda: left ^ right,
                    "and": lambda: left & right,
                    "or": lambda: left | right,
                    "mul": lambda: left * right,
                    "add": lambda: left + right,
                    "sub": lambda: left - right,
                }[op]()
                values[regs[0]] = signed(value, 32)
            elif name in {"xor-long", "or-long", "add-long", "sub-long", "mul-long"}:
                left, right = values[regs[1]], values[regs[2]]
                op = name.split("-")[0]
                value = {
                    "xor": lambda: left ^ right,
                    "or": lambda: left | right,
                    "add": lambda: left + right,
                    "sub": lambda: left - right,
                    "mul": lambda: left * right,
                }[op]()
                values[regs[0]] = signed(value, 64)
            elif name in {"and-int/lit8", "and-int/lit16"}:
                values[regs[0]] = signed(values[regs[1]] & literals[-1], 32)
            elif name in {
                "or-int/lit8",
                "or-int/lit16",
                "xor-int/lit8",
                "xor-int/lit16",
                "mul-int/lit8",
                "mul-int/lit16",
            }:
                left, right = values[regs[1]], literals[-1]
                op = name.split("-")[0]
                value = {
                    "or": lambda: left | right,
                    "xor": lambda: left ^ right,
                    "mul": lambda: left * right,
                }[op]()
                values[regs[0]] = signed(value, 32)
            elif name in {"add-int/lit8", "add-int/lit16", "rsub-int/lit8"}:
                left, right = values[regs[1]], literals[-1]
                values[regs[0]] = signed(right - left if name.startswith("rsub") else left + right, 32)
            elif name.startswith("rem-int/lit"):
                left, right = values[regs[1]], literals[-1]
                quotient = abs(left) // abs(right) * (1 if left * right >= 0 else -1)
                values[regs[0]] = signed(left - quotient * right, 32)
            elif name in {"shl-long", "ushr-long", "shr-long"}:
                source, shift = values[regs[1]], values[regs[2]] & 63
                if name == "shl-long":
                    value = source << shift
                elif name == "ushr-long":
                    value = (source & MASK64) >> shift
                else:
                    value = source >> shift
                values[regs[0]] = signed(value, 64)
            elif name in {"shl-int", "ushr-int", "shr-int"}:
                source, shift = values[regs[1]], values[regs[2]] & 31
                if name == "shl-int":
                    value = source << shift
                elif name == "ushr-int":
                    value = (source & MASK32) >> shift
                else:
                    value = source >> shift
                values[regs[0]] = signed(value, 32)
            elif name in {"shl-int/lit8", "shr-int/lit8", "ushr-int/lit8"}:
                source, shift = values[regs[1]], literals[-1] & 31
                if name == "shl-int/lit8":
                    value = source << shift
                elif name == "ushr-int/lit8":
                    value = (source & MASK32) >> shift
                else:
                    value = source >> shift
                values[regs[0]] = signed(value, 32)
            elif name == "ushr-int/2addr":
                values[regs[0]] = signed(
                    (values[regs[0]] & MASK32) >> (values[regs[1]] & 31), 32
                )
            elif name in {"long-to-int", "int-to-long"}:
                values[regs[0]] = signed(values[regs[1]], 32 if name == "long-to-int" else 64)
            elif name == "if-eq":
                if values[regs[0]] == values[regs[1]]:
                    next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name == "if-ne":
                if values[regs[0]] != values[regs[1]]:
                    next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name == "if-nez":
                if values[regs[0]] != 0:
                    next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name == "if-eqz":
                if values[regs[0]] == 0:
                    next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name == "if-lt":
                if values[regs[0]] < values[regs[1]]:
                    next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name == "if-ge":
                if values[regs[0]] >= values[regs[1]]:
                    next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name == "if-lez":
                if values[regs[0]] <= 0:
                    next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name == "if-gez":
                if values[regs[0]] >= 0:
                    next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name == "packed-switch":
                payload_offset = offsets[pc] + branch_offsets[-1] * 2
                payload_index = by_offset.get(payload_offset)
                if (
                    payload_index is None
                    or instructions[payload_index].get_name() != "packed-switch-payload"
                ):
                    raise ValueError(f"Missing packed-switch payload in {method.get_name()}")
                payload = instructions[payload_index]
                keys, targets = payload.get_keys(), payload.get_targets()
                key = values[regs[0]]
                if key in keys:
                    target = targets[keys.index(key)]
                    next_pc = by_offset[offsets[pc] + target * 2]
            elif name.startswith("goto"):
                next_pc = by_offset[offsets[pc] + branch_offsets[-1] * 2]
            elif name.startswith("return"):
                return values[regs[0]] if regs else None
            elif name == "check-cast":
                pass
            elif name == "nop":
                pass
            else:
                raise ValueError(f"Unsupported DEX opcode {name} in {method.get_name()}")
            pc = next_pc
        return None

    def answer(self) -> str:
        candidates = [
            (key, method)
            for key, method in self.methods.items()
            if key[0].endswith("/Release;")
            and key[1] == "code"
            and key[2].endswith(")Ljava/lang/String;")
        ]
        if len(candidates) != 1:
            raise ValueError(f"Expected one Release.code method, found {len(candidates)}")
        _, method = candidates[0]
        result = self.execute(method, [None])
        if not isinstance(result, str) or not re.fullmatch(r"ANS-[A-F0-9]{16}", result):
            raise ValueError(f"Release.code returned an unexpected value: {result!r}")
        return result


def analysis_answer(
    apk_path: Path,
    split_assets: dict[str, bytes] | None = None,
    verify_dex_integrity: bool = True,
) -> bytes:
    return DexEvaluator(
        apk_path,
        split_assets,
        verify_dex_integrity=verify_dex_integrity,
    ).answer().encode("ascii")
