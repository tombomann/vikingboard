#!/usr/bin/env python3
"""
vikingboard_kicad_check.py

Lightweight KiCad integration checker for the VikingBoard project.

Current goals:
- Load the structured pin/net spec from vikingboard_spec.py
- Verify that the KiCad schematic file exists
- Summarize what the spec expects (refs, nets, total connections)
- Prepare the ground for future deep KiCad S-expression parsing
"""

import sys
from pathlib import Path
from collections import Counter

# Make sure we can import vikingboard_spec when running from anywhere
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Try both import paths so we stay flexible
try:
    from tools.vikingboard_spec import iter_net_rows
except ModuleNotFoundError:
    try:
        from vikingboard_spec import iter_net_rows
    except ModuleNotFoundError as e:
        print("❌ Could not import vikingboard_spec. Make sure tools/vikingboard_spec.py exists.")
        print(f"Details: {e}")
        sys.exit(1)


def normalize_row(row):
    """
    Normalize one row from iter_net_rows() into a dict with keys:
      - ref
      - pad
      - net

    Supports:
      - dict-like rows with any case ('Ref', 'REF', 'ref', etc.)
      - tuple/list rows like (ref, pad, net)
    """
    # Case 1: dict-like
    if isinstance(row, dict):
        # Build a lowercased-key map
        lower = {str(k).lower(): v for k, v in row.items()}
        try:
            ref = lower["ref"]
            pad = lower["pad"]
            net = lower["net"]
        except KeyError as e:
            raise KeyError(f"Row dict missing expected key ({e}); row={row!r}")
        return {"ref": str(ref), "pad": str(pad), "net": str(net)}

    # Case 2: sequence (tuple/list)
    if isinstance(row, (list, tuple)):
        if len(row) < 3:
            raise ValueError(f"Row sequence too short, expected at least 3 items: {row!r}")
        ref, pad, net = row[0], row[1], row[2]
        return {"ref": str(ref), "pad": str(pad), "net": str(net)}

    # Unknown
    raise TypeError(f"Unsupported row type from iter_net_rows(): {type(row)!r}, value={row!r}")


def load_spec():
    raw_rows = list(iter_net_rows())
    if not raw_rows:
        print("⚠️ Spec returned no rows. Is vikingboard_spec.py empty?")
        return []

    norm_rows = []
    for idx, r in enumerate(raw_rows, start=1):
        try:
            norm_rows.append(normalize_row(r))
        except Exception as e:
            print(f"❌ Error normalizing row #{idx}: {e}")
            print(f"   Raw row: {r!r}")
            sys.exit(1)

    return norm_rows


def summarize_spec(rows):
    refs = {r["ref"] for r in rows}
    nets = {r["net"] for r in rows}
    print("📊 Spec summary")
    print(f"  - Total connections: {len(rows)}")
    print(f"  - Unique references : {len(refs)}  -> {sorted(refs)}")
    print(f"  - Unique nets       : {len(nets)}")

    per_ref = Counter(r["ref"] for r in rows)
    print("  - Connections per ref:")
    for ref, cnt in sorted(per_ref.items()):
        print(f"      {ref}: {cnt} pads")


def check_kicad_files():
    kicad_dir = REPO_ROOT / "kicad"
    sch_file = kicad_dir / "Vikingboard.kicad_sch"
    pcb_file = kicad_dir / "Vikingboard.kicad_pcb"

    print("\n📁 KiCad project check")
    print(f"  - KiCad dir : {kicad_dir}")

    ok = True

    if sch_file.exists():
        print(f"  ✅ Schematic: {sch_file}")
    else:
        print(f"  ❌ Missing schematic file: {sch_file}")
        ok = False

    if pcb_file.exists():
        print(f"  ✅ PCB file : {pcb_file}")
    else:
        print(f"  ❌ Missing PCB file: {pcb_file}")
        ok = False

    # Future: parse schematic S-expressions here and compare against spec
    return ok


def main():
    print("🔍 VikingBoard KiCad/spec integration check\n")

    # 1) Load and normalize spec
    rows = load_spec()
    if not rows:
        print("❌ No spec data to work with, aborting.")
        sys.exit(1)

    summarize_spec(rows)

    # 2) Check KiCad files exist
    ok_files = check_kicad_files()

    # 3) Placeholder for future deep checks
    print("\n🧠 Deep cross-checks")
    print("  - Schematic parsing and net/pin verification is not implemented yet.")
    print("  - This script currently only verifies spec + file presence.")
    print("  - Next step will be to read .kicad_sch and map symbols/pins to the spec.")

    if ok_files:
        print("\n✅ Basic KiCad/spec integration looks sane (files present).")
        sys.exit(0)
    else:
        print("\n⚠️ KiCad/spec integration incomplete (missing files).")
        sys.exit(1)


if __name__ == "__main__":
    main()
