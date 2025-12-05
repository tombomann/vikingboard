#!/bin/bash
K="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
OUT="production_output"
PCB="kicad/Vikingboard.kicad_pcb"
mkdir -p "$OUT/gerbers"
$K pcb export gerbers --output "$OUT/gerbers/" "$PCB" 2>/dev/null
$K pcb export drill --output "$OUT/gerbers/" "$PCB" 2>/dev/null
ZIP="$OUT/quick_$(date +%H%M).zip"
cd "$OUT/gerbers" && zip -q -r "../$(basename $ZIP)" * && cd - > /dev/null
echo "Quick export: $ZIP"
