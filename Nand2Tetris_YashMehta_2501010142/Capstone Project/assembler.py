"""
Capstone Project – Nand to Tetris I
Student Roll Number: 2501010142
Personal Number K: 42
"""

#!/usr/bin/env python3
"""
A simple two-pass Hack assembler.
Usage:
    python assembler.py Add.asm
Output:
    Add.hack
    symbols.txt  (labels and variables, as required for K = 42)
"""

import sys
from pathlib import Path

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
for i in range(16):
    PREDEFINED[f"R{i}"] = i

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}
DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}


def clean_lines(path):
    result = []
    for line_number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.split("//", 1)[0].strip()
        line = "".join(line.split())
        if line:
            result.append((line_number, line))
    return result


def assemble(path):
    lines = clean_lines(path)
    symbols = dict(PREDEFINED)
    labels = {}
    rom_address = 0

    # Pass 1: record label addresses.
    for line_number, line in lines:
        if line.startswith("(") and line.endswith(")"):
            name = line[1:-1]
            if not name or name in symbols or name in labels:
                raise ValueError(f"Line {line_number}: invalid or duplicate label")
            labels[name] = rom_address
        else:
            rom_address += 1

    symbols.update(labels)
    variables = {}
    next_variable = 16

    # Pass 2: translate instructions.
    machine_code = []
    for line_number, line in lines:
        if line.startswith("(") and line.endswith(")"):
            continue

        if line.startswith("@"):
            value = line[1:]
            if value.isdigit():
                address = int(value)
            else:
                if value not in symbols:
                    if value not in variables:
                        variables[value] = next_variable
                        symbols[value] = next_variable
                        next_variable += 1
                address = symbols[value]

            if not 0 <= address <= 32767:
                raise ValueError(f"Line {line_number}: A-instruction address out of range")
            machine_code.append(format(address, "016b"))
            continue

        # C-instruction: dest=comp;jump (either dest or jump may be absent).
        if line.count("=") > 1 or line.count(";") > 1:
            raise ValueError(f"Line {line_number}: invalid C-instruction")

        if "=" in line:
            dest, rest = line.split("=", 1)
        else:
            dest, rest = "", line

        if ";" in rest:
            comp, jump = rest.split(";", 1)
        else:
            comp, jump = rest, ""

        if comp not in COMP:
            raise ValueError(f"Line {line_number}: invalid comp field '{comp}'")
        if dest not in DEST:
            raise ValueError(f"Line {line_number}: invalid dest field '{dest}'")
        if jump not in JUMP:
            raise ValueError(f"Line {line_number}: invalid jump field '{jump}'")

        machine_code.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])

    # K = 42, and 42 mod 3 = 0: save labels and variables.
    symbol_lines = ["Symbol,Address"]
    for name, address in labels.items():
        symbol_lines.append(f"{name},{address}")
    for name, address in variables.items():
        symbol_lines.append(f"{name},{address}")

    output_path = path.with_suffix(".hack")
    output_path.write_text("\n".join(machine_code) + "\n")
    Path("symbols.txt").write_text("\n".join(symbol_lines) + "\n")
    return output_path, len(machine_code), len(labels), len(variables)


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
        raise SystemExit(1)

    source = Path(sys.argv[1])
    if not source.exists():
        print(f"File not found: {source}")
        raise SystemExit(1)

    try:
        output, count, label_count, variable_count = assemble(source)
        print(f"Created {output} ({count} instructions)")
        print(f"Saved {label_count} labels and {variable_count} variables in symbols.txt")
    except ValueError as error:
        print(error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
