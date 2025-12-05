#!/bin/bash
PCB="kicad/Vikingboard.kicad_pcb"
SCH="kicad/Vikingboard.kicad_sch"
OUT="production_output/jlcpcb_bundle"
mkdir -p "$OUT"
echo "Creating JLCPCB bundle with KiKit..."
kikit fab jlcpcb --assembly --schematic "$SCH" --no-drc "$PCB" "$OUT" 2>/dev/null
ZIP="production_output/jlcpcb_$(date +%Y%m%d_%H%M).zip"
cd "$OUT" && zip -q -r "../../$(basename $ZIP)" * && cd - > /dev/null
echo "JLCPCB bundle: $ZIP"
