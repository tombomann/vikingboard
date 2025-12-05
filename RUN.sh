#!/bin/bash
set -e
clear
echo "VIKINGBOARD AUTOMATION"
echo "======================"
K="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
PCB="kicad/Vikingboard.kicad_pcb"
SCH="kicad/Vikingboard.kicad_sch"

# Check files exist
if [[ ! -f "$PCB" ]]; then
    echo "ERROR: PCB file not found: $PCB"
    exit 1
fi
if [[ ! -f "$SCH" ]]; then
    echo "ERROR: Schematic file not found: $SCH"
    echo "Available schematics:"
    ls -1 kicad/*.kicad_sch
    exit 1
fi

OUT="production"
mkdir -p "$OUT/gerbers" "$OUT/docs" backups
echo ""
echo "Using files:"
echo "  PCB: $PCB"
echo "  SCH: $SCH"
echo ""
echo "Backing up..."
T=$(date +%Y%m%d_%H%M%S)
cp "$PCB" "backups/pcb_$T.kicad_pcb"
cp "$SCH" "backups/sch_$T.kicad_sch"
echo "Exporting gerbers..."
$K pcb export gerbers --output "$OUT/gerbers/" "$PCB" 2>/dev/null
$K pcb export drill --output "$OUT/gerbers/" "$PCB" 2>/dev/null
echo "Exporting BOM & CPL..."
$K sch export bom --output "$OUT/bom.csv" "$SCH" 2>/dev/null
$K pcb export pos --output "$OUT/cpl.csv" --units mm --side front "$PCB" 2>/dev/null
echo "Exporting docs..."
$K sch export pdf --output "$OUT/docs/schematic.pdf" "$SCH" 2>/dev/null
$K pcb export pdf --output "$OUT/docs/pcb.pdf" --layers "F.Cu,B.Cu,Edge.Cuts" "$PCB" 2>/dev/null
echo "Exporting 3D..."
$K pcb export step --output "$OUT/3d.step" "$PCB" 2>/dev/null
echo "Creating JLCPCB bundle..."
ZIP="$OUT/JLCPCB_$(date +%Y%m%d_%H%M).zip"
cd "$OUT/gerbers" && zip -q -r "../$(basename $ZIP)" * && cd - > /dev/null
echo "Running DRC..."
$K pcb drc --output "$OUT/drc.txt" --severity-all "$PCB" 2>/dev/null
VIOL=$(grep -c violations "$OUT/drc.txt" 2>/dev/null || echo 0)
UNCON=$(grep -c unconnected "$OUT/drc.txt" 2>/dev/null || echo 0)
COMP=$(grep -c footprint "$PCB" 2>/dev/null || echo 0)
echo ""
echo "COMPLETE!"
echo "========="
echo "Components: $COMP"
echo "Violations: $VIOL"
echo "Unconnected: $UNCON"
echo ""
echo "FILES READY:"
ls -lh "$OUT"/*.{zip,csv,step} 2>/dev/null
echo ""
echo "UPLOAD TO JLCPCB:"
echo "1. $ZIP"
echo "2. $OUT/bom.csv"
echo "3. $OUT/cpl.csv"
echo ""
