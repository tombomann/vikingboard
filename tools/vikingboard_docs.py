#!/usr/bin/env python3
"""
VikingBoard documentation generator.

Leser pins fra vikingboard_spec.get_all_pins() og genererer:
- docs/vikingboard_nets.md (Markdown tabell)
- docs/vikingboard_nets.csv (CSV)
"""

import csv
from pathlib import Path
from typing import List
from vikingboard_spec import get_all_pins, Pin  # type: ignore


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
MD_PATH = DOCS_DIR / "vikingboard_nets.md"
CSV_PATH = DOCS_DIR / "vikingboard_nets.csv"


def generate_markdown(pins: List[Pin], path: Path) -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# VikingBoard net overview\n\n")
        f.write("| Ref | Pad | Net |\n")
        f.write("| :-- | :-- | :-- |\n")
        for pin in sorted(pins, key=lambda p: (p.ref, str(p.pad))):
            f.write(f"| {pin.ref} | {pin.pad} | `{pin.net}` |\n")


def generate_csv(pins: List[Pin], path: Path) -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Ref", "Pad", "Net"])
        for pin in sorted(pins, key=lambda p: (p.ref, str(p.pad))):
            writer.writerow([pin.ref, pin.pad, pin.net])


def main() -> None:
    pins = get_all_pins()
    print(f"[INFO] Loaded {len(pins)} pins from vikingboard_spec.get_all_pins()")
    generate_markdown(pins, MD_PATH)
    generate_csv(pins, CSV_PATH)
    print(f"[INFO] Wrote {MD_PATH} and {CSV_PATH}")


if __name__ == "__main__":
    main()
