#!/usr/bin/env python3
import os

PROJECT_ROOT = os.path.expanduser("~/vikingboard")
KICAD_DIR = os.path.join(PROJECT_ROOT, "kicad")

PROJECT_FILES = {
    "Vikingboard.kicad_pro": '(kicad_project (version 20231120))\n',
    "Vikingboard.kicad_sch": '(kicad_sch (version 20231120))\n',
    "Vikingboard.kicad_pcb": '(kicad_pcb (version 20231120))\n',
}

def main():
    print("🤖 VikingBoard setup checker")
    print(f"📁 Prosjektrot: {PROJECT_ROOT}")
    os.makedirs(KICAD_DIR, exist_ok=True)
    print(f"📁 KiCad-mappe: {KICAD_DIR}")

    for fname, content in PROJECT_FILES.items():
        path = os.path.join(KICAD_DIR, fname)
        if os.path.exists(path):
            print(f"✅ Finnes allerede: {fname}")
        else:
            with open(path, "w") as f:
                f.write(content)
            print(f"🆕 Opprettet: {fname}")

    print("\n📋 Statusrapport:")
    for fname in PROJECT_FILES.keys():
        path = os.path.join(KICAD_DIR, fname)
        print(f" - {fname}: {'OK' if os.path.exists(path) else 'Mangler'}")

    print("\n🎯 Neste steg (manuelt):")
    print("  1) Åpne KiCad og last inn kicad/Vikingboard.kicad_pro")
    print("  2) Legg inn symbolene U1–U8, J1 og J3 i schematic")
    print("  3) Kjør 'Update PCB from schematic' i KiCad (så U1..J3 havner på PCB)")
    print("  4) I PCB editor: kjør vikingboard_nets.py i Python-konsollen")

if __name__ == "__main__":
    main()
