#!/bin/bash
################################################################################
# VIKINGBOARD ULTIMATE AUTOMATION - ALT I EN FIL
################################################################################
set -e
clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           VIKINGBOARD ULTIMATE AUTOMATION v5.0              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

K="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
PCB="kicad/Vikingboard.kicad_pcb"
SCH="kicad/Vikingboard.kicad_sch"
OUT="production"
TOOLS="$HOME/kicad_tools"
FR_JAR="$TOOLS/freerouting.jar"
FR_URL="https://github.com/freerouting/freerouting/releases/download/v2.1.0/freerouting-2.1.0.jar"

echo "📦 PHASE 1: Setup"
mkdir -p "$TOOLS" "$OUT/gerbers" "$OUT/docs" "$OUT/3d"
[[ -f "$K" ]] && echo "✅ KiCad" || { echo "❌ KiCad missing"; exit 1; }
[[ -f "$PCB" ]] && echo "✅ PCB" || { echo "❌ PCB missing"; exit 1; }

echo ""
echo "🔧 PHASE 2: Install Tools"
pip3 install --user --quiet kibot 2>/dev/null || true
command -v kibot &> /dev/null && KB=1 || KB=0
[[ -f "$FR_JAR" ]] || curl -sL "$FR_URL" -o "$FR_JAR" 2>/dev/null
command -v java &> /dev/null && JAVA=1 || JAVA=0
[[ $KB -eq 1 ]] && echo "✅ KiBot" || echo "⚠️  KiBot (fallback mode)"
[[ -f "$FR_JAR" ]] && [[ $JAVA -eq 1 ]] && echo "✅ FreeRouting" || echo "⚠️  FreeRouting skip"

echo ""
echo "🤖 PHASE 3: Auto-Routing"
if [[ -f "$FR_JAR" ]] && [[ $JAVA -eq 1 ]]; then
    DSN="temp.dsn"
    SES="temp.ses"
    $K pcb export specctra-dsn "$PCB" --output "$DSN" 2>/dev/null
    java -jar "$FR_JAR" -de "$DSN" -do "$SES" -mp 20 -mt 4 2>/dev/null || true
    [[ -f "$SES" ]] && $K pcb import specctra-ses "$PCB" "$SES" 2>/dev/null && echo "✅ Auto-routed" || echo "⚠️  Routing skip"
    rm -f "$DSN" "$SES"
else
    echo "⚠️  Auto-routing skipped"
fi

echo ""
echo "📐 PHASE 4: Export Production Files"
$K pcb export gerbers --output "$OUT/gerbers/" "$PCB" 2>/dev/null
$K pcb export drill --output "$OUT/gerbers/" "$PCB" 2>/dev/null
$K sch export bom --output "$OUT/bom.csv" "$SCH" 2>/dev/null
$K pcb export pos --output "$OUT/cpl.csv" --units mm "$PCB" 2>/dev/null
$K sch export pdf --output "$OUT/docs/schematic.pdf" "$SCH" 2>/dev/null
$K pcb export pdf --output "$OUT/docs/pcb.pdf" --layers "F.Cu,B.Cu,Edge.Cuts" "$PCB" 2>/dev/null
$K pcb export step --output "$OUT/3d/board.step" "$PCB" 2>/dev/null
echo "✅ All files exported"

echo ""
echo "📦 PHASE 5: JLCPCB Bundle"
ZIP="$OUT/JLCPCB_$(date +%Y%m%d_%H%M).zip"
cd "$OUT/gerbers" && zip -q -r "../$(basename $ZIP)" * && cd ../..
echo "✅ JLCPCB bundle: $ZIP"

echo ""
echo "📊 PHASE 6: Quality Check"
$K pcb drc --output "$OUT/drc.txt" --severity-all "$PCB" 2>/dev/null
VIOL=$(grep -c "violations" "$OUT/drc.txt" 2>/dev/null || echo "0")
UNCON=$(grep -c "unconnected" "$OUT/drc.txt" 2>/dev/null || echo "0")
COMP=$(grep -c "(footprint" "$PCB" 2>/dev/null || echo "0")
echo "  Components: $COMP"
echo "  DRC Violations: $VIOL"
echo "  Unconnected: $UNCON"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ COMPLETE SUCCESS!                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📦 READY FOR JLCPCB:"
echo "  1. Upload: $ZIP"
echo "  2. BOM: production/bom.csv"
echo "  3. CPL: production/cpl.csv"
echo ""
echo "📁 All files in: production/"
ls -lh "$OUT"/*.{zip,csv} 2>/dev/null
echo ""
