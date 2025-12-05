#!/bin/bash
set -e

echo "🚀 VikingBoard - Production Export"
echo "==================================="

KICAD_CLI="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
PCB="kicad/Vikingboard.kicad_pcb"
SCH="kicad/Vikingboard.kicad_sch"
OUT="production_output"
REPORTS="reports"

# Backup
cp "$PCB" "${PCB}.backup_$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
mkdir -p "$OUT/gerbers" "$REPORTS"

# 1. Gerbers + Drill
echo "📐 Exporting Gerbers..."
$KICAD_CLI pcb export gerbers --output "$OUT/gerbers/" "$PCB" 2>/dev/null
$KICAD_CLI pcb export drill --output "$OUT/gerbers/" "$PCB" 2>/dev/null
cd "$OUT/gerbers" && zip -q -r ../vikingboard_gerbers_$(date +%Y%m%d).zip * && cd ../..
echo "✅ Gerbers ready"

# 2. BOM + CPL
echo "📋 Exporting BOM/CPL..."
$KICAD_CLI sch export bom --output "$OUT/vikingboard_bom.csv" "$SCH" 2>/dev/null
$KICAD_CLI pcb export pos --output "$OUT/vikingboard_cpl.csv" --units mm --side front "$PCB" 2>/dev/null
echo "✅ BOM/CPL ready"

# 3. DRC
echo "✅ Running DRC..."
$KICAD_CLI pcb drc --output "$REPORTS/drc_report.txt" --severity-all "$PCB" 2>/dev/null
echo "✅ DRC complete"

# 4. PDFs
echo "📄 Exporting PDFs..."
$KICAD_CLI sch export pdf --output "$OUT/schematic.pdf" "$SCH" 2>/dev/null
$KICAD_CLI pcb export pdf --output "$OUT/pcb.pdf" --layers "F.Cu,B.Cu,Edge.Cuts" "$PCB" 2>/dev/null
echo "✅ PDFs ready"

# 5. 3D Model
echo "🎯 Exporting 3D..."
$KICAD_CLI pcb export step --output "$OUT/vikingboard.step" "$PCB" 2>/dev/null
echo "✅ STEP ready"

# Summary
echo ""
echo "════════════════════════════════════"
echo "✅ Production Files Ready!"
echo "════════════════════════════════════"
echo ""
ls -lh "$OUT"/*.{zip,pdf,csv,step} 2>/dev/null | awk '{printf "  %-50s %8s\n", $9, $5}'

echo ""
echo "📊 Quality:"
violations=$(grep "Found.*violations" "$REPORTS/drc_report.txt" 2>/dev/null | head -1)
unconnected=$(grep -c "unconnected_items" "$REPORTS/drc_report.txt" 2>/dev/null || echo "0")
echo "  DRC: $violations"
echo "  Unconnected: $unconnected pads"

echo ""
echo "📦 Upload til JLCPCB:"
echo "  1. Gerbers: production_output/vikingboard_gerbers_*.zip"
echo "  2. BOM: production_output/vikingboard_bom.csv"
echo "  3. CPL: production_output/vikingboard_cpl.csv"
echo ""
echo "🔧 Next: Fix $unconnected unconnected pads i KiCad (use FreeRouting plugin)"
