#!/usr/bin/env python3
"""
vikingboard_sch_generate.py - Minimal schematic generator for VikingBoard.

- Leser vikingboard_spec.get_all_pins()
- Lager en enkel .kicad_sch med stub-symboler for J1, J3, U1..U8
  og tekstlabels for alle nets.
"""

from pathlib import Path
from typing import Set
from vikingboard_spec import get_all_pins  # forutsetter at denne finnes

REPO_ROOT = Path(__file__).resolve().parents[1]
SCH_PATH = REPO_ROOT / "kicad" / "Vikingboard_auto.kicad_sch"


def main():
    pins = get_all_pins()
    refs: Set[str] = set(p.ref for p in pins)
    nets: Set[str] = set(p.net for p in pins)

    lines = []
    lines.append("(kicad_sch (version 20211014) (generator vikingboard_sch_generate)")
    lines.append('  (paper "A4")')

    y = 0
    for ref in sorted(refs):
        y += 20
        lines.append('  (symbol (lib_id "Device:Stub")')
        lines.append(f"    (at 0 {y})")
        lines.append(f'    (property "Reference" "{ref}" (at 0 {y+2}) (effects (font (size 1.27 1.27))))')
        lines.append(f'    (property "Value" "{ref}" (at 0 {y+4}) (effects (font (size 1.27 1.27))))')
        lines.append("  )")

    x = 60
    y = 0
    for net in sorted(nets):
        y += 5
        lines.append(f'  (text (at {x} {y}) (effects (font (size 1 1)))')
        lines.append(f'    "{net}"')
        lines.append("  )")

    lines.append(")")

    SCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCH_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[INFO] Generated schematic stub at {SCH_PATH}")


if __name__ == "__main__":
    main()
