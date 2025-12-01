#!/usr/bin/env python3
"""
VikingBoard EDA automation entrypoint.

This module is the central place for:
- reading and validating the VikingBoard pin and net configuration
- exporting documentation (Markdown/CSV/JSON)
- preparing data structures that can be used to generate KiCad schematics or PCB updates

All logic and comments are in English, because the repository is English-only.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import csv

# === Data model =============================================================

@dataclass
class NetAssignment:
    ref: str
    pad: str
    net: str

# This should stay in sync with your Python pinmap logic.
# It is intentionally simple and English-only.
MODULE_CONFIG = {
    "U1": [
        ("SPI_SCK", "10"),
        ("SPI_MOSI", "11"),
        ("SPI_MISO", "12"),
        ("I2C_SCL", "13"),
        ("I2C_SDA", "14"),
        ("MCP_INT", "21"),
        ("+5V_SYS", "5V"),
        ("GND",     "GND"),
        ("EN",      "EN"),
        ("GPS_RX",  "43"),
        ("GPS_TX",  "44"),
    ],
    "U2": [
        ("GND",      "10"),
        ("+3V3_IO",  "9"),
        ("I2C_SCL",  "12"),
        ("I2C_SDA",  "13"),
        ("MCP_INT",  "20"),
        ("EN",       "18"),
        ("GND",      "15"),
        ("GND",      "16"),
        ("GND",      "17"),
        ("LORA_CS",       "21"),
        ("LORA_BUSY",     "22"),
        ("LORA_DIO1",     "23"),
        ("GPS_PPS",       "24"),
        ("CC1101_CS",     "25"),
        ("CC1101_GDO0",   "26"),
        ("NRF24_CS",      "27"),
        ("NRF24_CE",      "28"),
        ("NRF24_IRQ",     "1"),
        ("KBD_RST",       "2"),
        ("KBD_INT",       "3"),
        ("FZ_GPIO1",      "4"),
        ("FZ_GPIO2",      "5"),
        ("FZ_GPIO3",      "6"),
        ("FZ_GPIO4",      "7"),
        ("FZ_GPIO5",      "8"),
    ],
    # U3..U8, J1, J3 can be added here in the same style
}


# === Export helpers =========================================================

def build_assignments() -> list[NetAssignment]:
    """Flatten MODULE_CONFIG into a list of NetAssignment objects."""
    result: list[NetAssignment] = []
    for ref, mappings in MODULE_CONFIG.items():
        for net, pad in mappings:
            result.append(NetAssignment(ref=ref, pad=str(pad), net=net))
    return result


def export_markdown(path: Path, assignments: list[NetAssignment]) -> None:
    """Export the net assignments as a Markdown table."""
    lines = []
    lines.append("| Ref | Pad | Net |")
    lines.append("| :-- | :-- | :-- |")
    for a in assignments:
        lines.append(f"| {a.ref} | {a.pad} | `{a.net}` |")
    path.write_text("\n".join(lines), encoding="utf-8")


def export_csv(path: Path, assignments: list[NetAssignment]) -> None:
    """Export the net assignments as a CSV file."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ref", "Pad", "Net"])
        for a in assignments:
            writer.writerow([a.ref, a.pad, a.net])


def export_json(path: Path, assignments: list[NetAssignment]) -> None:
    """Export the net assignments as a JSON file."""
    data = [asdict(a) for a in assignments]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    """Main entrypoint for local automation."""
    project_root = Path(__file__).resolve().parent.parent
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    assignments = build_assignments()

    export_markdown(docs_dir / "vikingboard_nets_auto.md", assignments)
    export_csv(docs_dir / "vikingboard_nets_auto.csv", assignments)
    export_json(docs_dir / "vikingboard_nets_auto.json", assignments)

    print("✅ VikingBoard EDA automation export completed.")
    print(f"   Markdown: {docs_dir / 'vikingboard_nets_auto.md'}")
    print(f"   CSV:      {docs_dir / 'vikingboard_nets_auto.csv'}")
    print(f"   JSON:     {docs_dir / 'vikingboard_nets_auto.json'}")


if __name__ == "__main__":
    main()
