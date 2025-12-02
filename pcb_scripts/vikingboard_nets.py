#!/usr/bin/env python3
"""
vikingboard_nets.py - Synkroniser nett fra spec til KiCad PCB.

Kjøres fra KiCad PCB Editor → Tools → Scripting Console (PyShell).
"""

import csv
from pathlib import Path
from typing import Dict, List, Tuple

import pcbnew

# === KONFIGURASJON ===
DRY_RUN = False  # Sett til False for å faktisk skrive endringer

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_CSV = REPO_ROOT / "docs" / "vikingboard_nets.csv"


def iter_net_rows_from_csv(csv_path: Path) -> List[Tuple[str, str, str]]:
    """Les CSV og returner liste av (ref, pad, net) tupler."""
    rows = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ref = row.get("Ref", "").strip()
            pad = row.get("Pad", "").strip()
            net = row.get("Net", "").strip().strip("`")
            if ref and pad and net:
                rows.append((ref, pad, net))
    return rows


def build_spec_dict(rows: List[Tuple[str, str, str]]) -> Dict[Tuple[str, str], str]:
    """Bygg dict fra (ref, pad) -> net_name."""
    spec = {}
    for ref, pad, net in rows:
        spec[(ref, pad)] = net
    return spec


def get_or_create_net(board: pcbnew.BOARD, net_name: str) -> pcbnew.NETINFO_ITEM:
    """Hent eksisterende nett eller opprett nytt hvis det ikke finnes."""
    # Prøv å finne eksisterende nett
    netinfo = board.FindNet(net_name)
    if netinfo is not None and netinfo.GetNetname() == net_name:
        return netinfo
    
    # Opprett nytt nett
    netinfo = pcbnew.NETINFO_ITEM(board, net_name)
    board.Add(netinfo)
    return netinfo


def apply_nets_from_spec(spec: Dict[Tuple[str, str], str]):
    """Gå gjennom spec og sett nett på pads."""
    board = pcbnew.GetBoard()
    if board is None:
        print("[ERROR] No board loaded in PCB editor.")
        return

    print("=== VikingBoard net-script ===")
    print(f"Mode: {'DRY_RUN' if DRY_RUN else 'APPLY'}")
    
    total = len(spec)
    fp_not_found = 0
    pads_not_found = 0
    changed = 0

    print(f"[INFO] Total spec entries: {total}")

    # Bygg dict over footprints
    footprints = {fp.GetReference(): fp for fp in board.GetFootprints()}

    for (ref, pad_name), net_name in spec.items():
        fp = footprints.get(ref)
        if fp is None:
            print(f"[ERROR] Footprint not found for ref {ref}")
            fp_not_found += 1
            continue

        # Finn pad
        pad = None
        for p in fp.Pads():
            if p.GetNumber() == pad_name:
                pad = p
                break

        if pad is None:
            print(f"[ERROR] Pad '{pad_name}' not found on footprint {ref}")
            pads_not_found += 1
            continue

        # Sjekk current net
        current_net = pad.GetNetname()
        if current_net == net_name:
            continue  # Allerede riktig

        print(f"[CHANGE] {ref}.{pad_name}: {current_net} -> {net_name}")

        if not DRY_RUN:
            netinfo = get_or_create_net(board, net_name)
            pad.SetNet(netinfo)
            changed += 1

    print("\n--- Summary ---")
    print(f"Total spec entries  : {total}")
    print(f"Footprints not found: {fp_not_found}")
    print(f"Pads not found      : {pads_not_found}")
    print(f"Pads changed        : {changed}")
    if DRY_RUN:
        print("\n[NOTE] DRY_RUN is True. No changes were written to the board.")
        print("       Set DRY_RUN = False and reload the module to apply changes.")
    else:
        print("\n[NOTE] Changes written to the board. Save the PCB to persist.")


def print_markdown_preview(spec: Dict[Tuple[str, str], str]):
    rows = list(spec.items())
    print("\n--- Markdown pin map (from spec) ---")
    print("| Ref | Pad | Net |")
    print("| :-- | :-- | :-- |")
    for (ref, pad), net in sorted(rows):
        print(f"| {ref} | {pad} | `{net}` |")


def main():
    rows = iter_net_rows_from_csv(DOCS_CSV)
    print(f"[INFO] iter_net_rows_from_csv() yielded {len(rows)} rows")
    spec = build_spec_dict(rows)
    print(f"[INFO] Normalized {len(spec)} spec entries")

    apply_nets_from_spec(spec)
    print_markdown_preview(spec)


if __name__ == "__main__":
    main()
