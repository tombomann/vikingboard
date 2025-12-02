#!/usr/bin/env python3
"""
Generate VikingBoard documentation from the spec.

Outputs:
- docs/vikingboard_nets.md
- docs/vikingboard_nets.csv
"""

from pathlib import Path
import sys

# Project root = parent of this file's directory
ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools"
sys.path.append(str(TOOLS_DIR))

from vikingboard_spec import iter_net_rows  # type: ignore

DOCS_DIR = ROOT / "docs"
DOCS_DIR.mkdir(exist_ok=True)


def write_markdown() -> None:
    md_path = DOCS_DIR / "vikingboard_nets.md"
    rows = list(iter_net_rows())

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# VikingBoard Net Table\n\n")
        f.write("| Ref | Pad | Net |\n")
        f.write("| :-- | :-- | :--- |\n")
        for row in rows:
            f.write(f"| {row['Ref']} | {row['Pad']} | `{row['Net']}` |\n")

    print(f"✅ Wrote {md_path}")


def write_csv() -> None:
    csv_path = DOCS_DIR / "vikingboard_nets.csv"
    rows = list(iter_net_rows())

    with csv_path.open("w", encoding="utf-8") as f:
        f.write("Ref,Pad,Net\n")
        for row in rows:
            f.write(f"{row['Ref']},{row['Pad']},{row['Net']}\n")

    print(f"✅ Wrote {csv_path}")


def main() -> None:
    print("🔧 Generating VikingBoard docs from spec...")
    write_markdown()
    write_csv()
    print("🎉 Done.")


if __name__ == "__main__":
    main()
