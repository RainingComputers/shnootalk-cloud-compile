from typing import Dict


def validate(programs: Dict[str, str]) -> bool:
    num_chars = 0

    for _, values in programs.items():
        num_chars += len(values)

    return num_chars < 65536
