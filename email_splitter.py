#!/usr/bin/env python3
import os
from pathlib import Path

SEPARATOR = "=========================================================================\n"

def split_eml_file(eml_path: Path, output_dir: Path) -> None:
    # Read entire .eml file as text
    content = eml_path.read_text(encoding="utf-8", errors="replace")

    # Split on the separator string
    parts = content.split(SEPARATOR)

    # Write each part to a new file with index starting at 0
    for idx, part in enumerate(parts):
        # Skip completely empty parts (optional)
        if not part.strip():
            continue

        out_name = f"{eml_path.stem.replace("File_ _ATMLA-L ","")}_{idx}.eml"
        out_path = output_dir / out_name
        out_path.write_text(part, encoding="utf-8")

def main():
    base_dir = Path(".").resolve()
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # Iterate over all .eml files in the directory (non-recursive)
    for eml_path in base_dir.glob("*.eml"):
        split_eml_file(eml_path, output_dir)

if __name__ == "__main__":
    main()
