#!/bin/bash
set -e
clear
echo "╔════════════════════════════════════════════╗"
echo "║   VIKINGBOARD MASTER AUTOMATION v4.0      ║"
echo "║         MED KiKit CLI SUPPORT             ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Paths
K="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
PCB="kicad/Vikingboard.kicad_pcb"
SCH="kicad/Vikingboard.kicad_sch"
OUT="production_output"
REPORTS="reports"
BACKUP="backups"
DOCS="documentation"
AUTO="automation"
JLCPCB="$OUT/jlcpcb_bundle"

# Setup directories
mkdir -p "$OUT/gerbers" "$REPORTS" "$BACKUP" "$DOCS" "$AUTO" "$JLCPCB"

# Check tools
[[ -f "$K" ]] && echo "✅ KiCad CLI" || { echo "❌ KiCad missing"; exit 1; }
command -v kikit &> /dev/null && KIKIT_OK=1 && echo "✅ KiKit CLI" || { KIKIT_OK=0; echo "⚠️  KiKit not found"; }
[[ -f "$PCB" ]] && echo "✅ PCB" || { echo "❌ PCB missing"; exit 1; }
[[ -f "$SCH" ]] && echo "✅ Schematic" || { echo "❌ SCH missing"; exit 1; }

echo ""
echo "💾 Backing up..."
T=$(date +%Y%m%d_%H%M%S)
cp "$PCB" "$BACKUP/Vikingboard_${T}.kicad_pcb" 2>/dev/null
cp "$SCH" "$BACKUP/Vikingboard_${T}.kicad_sch" 2>/dev/null
echo "✅ Backup saved: $T"

echo ""
echo "📐 Exporting Gerbers..."
$K pcb export gerbers --output "$OUT/gerbers/" "$PCB" 2>/dev/null
$K pcb export drill --output "$OUT/gerbers/" "$PCB" 2>/dev/null
ZIP="$OUT/vikingboard_gerbers_$(date +%Y%m%d).zip"
cd "$OUT/gerbers" && zip -q -r "../$(basename $ZIP)" * && cd - > /dev/null
echo "✅ Gerbers: $(du -h "$ZIP" | awk '{print $1}')"

echo ""
echo "📋 Exporting BOM/CPL..."
$K sch export bom --output "$OUT/vikingboard_bom.csv" "$SCH" 2>/dev/null
BOM=$(($(wc -l < "$OUT/vikingboard_bom.csv") - 1))
echo "✅ BOM: $BOM components"

$K pcb export pos --output "$OUT/vikingboard_cpl.csv" --units mm --side front "$PCB" 2>/dev/null
CPL=$(($(wc -l < "$OUT/vikingboard_cpl.csv") - 1))
echo "✅ CPL: $CPL placements"

echo ""
echo "🏭 Creating KiKit JLCPCB Bundle..."
if [[ $KIKIT_OK -eq 1 ]]; then
    kikit fab jlcpcb \
      --assembly \
      --schematic "$SCH" \
      --no-drc \
      "$PCB" \
      "$JLCPCB" 2>/dev/null && echo "✅ KiKit bundle created" || echo "⚠️  KiKit bundle failed"
    
    if [[ -d "$JLCPCB" ]] && [[ -n "$(ls -A $JLCPCB 2>/dev/null)" ]]; then
        JLCZIP="$OUT/jlcpcb_complete_$(date +%Y%m%d).zip"
        cd "$JLCPCB" && zip -q -r "../$(basename $JLCZIP)" * && cd - > /dev/null
        echo "✅ JLCPCB ZIP: $(du -h "$JLCZIP" | awk '{print $1}')"
    fi
else
    echo "⚠️  KiKit not available, skipping JLCPCB bundle"
    JLCZIP=""
fi

echo ""
echo "✅ Running DRC..."
$K pcb drc --output "$REPORTS/drc_report.txt" --severity-all "$PCB" 2>/dev/null
VIOL=$(grep -c "violations" "$REPORTS/drc_report.txt" 2>/dev/null || echo "0")
UNCON=$(grep -c "unconnected_items" "$REPORTS/drc_report.txt" 2>/dev/null || echo "0")
if [[ $UNCON -eq 0 ]]; then
    echo "✅ Perfect - No issues"
else
    echo "⚠️  $VIOL violations, $UNCON unconnected"
fi

echo ""
echo "📄 Exporting Documentation..."
$K sch export pdf --output "$DOCS/schematic.pdf" "$SCH" 2>/dev/null
$K pcb export pdf --output "$DOCS/pcb.pdf" --layers "F.Cu,B.Cu,Edge.Cuts" "$PCB" 2>/dev/null
$K pcb export svg --output "$DOCS/" --layers "F.Cu" "$PCB" 2>/dev/null || true
echo "✅ PDFs exported"

echo ""
echo "🎯 Exporting 3D Model..."
$K pcb export step --output "$OUT/vikingboard_3d.step" "$PCB" 2>/dev/null
echo "✅ STEP: $(du -h "$OUT/vikingboard_3d.step" | awk '{print $1}')"

echo ""
echo "📊 Project Statistics..."
COMP_COUNT=$(grep -c "footprint" "$PCB" 2>/dev/null || echo "?")
NET_COUNT=$(grep -c "^  (net " "$PCB" 2>/dev/null || echo "?")
VIA_COUNT=$(grep -c "via" "$PCB" 2>/dev/null || echo "0")
echo "📦 Components: $COMP_COUNT"
echo "🔌 Nets: $NET_COUNT"
echo "🔩 Vias: $VIA_COUNT"

echo ""
echo "📝 Creating Helper Scripts..."

cat > "quick_export.sh" << 'QEXPORT'
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
QEXPORT
chmod +x quick_export.sh

cat > "open_kicad.sh" << 'OPENK'
#!/bin/bash
echo "Opening VikingBoard in KiCad..."
open -a KiCad kicad/Vikingboard.kicad_pcb
OPENK
chmod +x open_kicad.sh

cat > "check_status.sh" << 'CHECKSTATUS'
#!/bin/bash
echo "VikingBoard Status"
echo "=================="
[[ -f production_output/vikingboard_gerbers_*.zip ]] && echo "✅ Gerbers" || echo "❌ Gerbers"
[[ -f production_output/vikingboard_bom.csv ]] && echo "✅ BOM" || echo "❌ BOM"
[[ -f production_output/vikingboard_cpl.csv ]] && echo "✅ CPL" || echo "❌ CPL"
[[ -f production_output/vikingboard_3d.step ]] && echo "✅ 3D Model" || echo "❌ 3D Model"
[[ -f production_output/jlcpcb_complete_*.zip ]] && echo "✅ JLCPCB Bundle" || echo "⚠️  JLCPCB Bundle"
echo ""
grep "Found" reports/drc_report.txt 2>/dev/null || echo "No DRC report"
CHECKSTATUS
chmod +x check_status.sh

if [[ $KIKIT_OK -eq 1 ]]; then
cat > "make_jlcpcb.sh" << 'JLCSCRIPT'
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
JLCSCRIPT
chmod +x make_jlcpcb.sh
fi

echo "✅ Helper scripts created"

cat > "QUICKSTART.md" << 'QUICKGUIDE'
# VikingBoard QuickStart

## Production Files
All files in: production_output/

## Upload to JLCPCB

### Option 1: JLCPCB Bundle (if available)
1. Go to: https://jlcpcb.com
2. Upload: jlcpcb_complete_*.zip
3. Everything auto-configured
4. Order

### Option 2: Manual Upload
1. Go to: https://jlcpcb.com
2. Upload: vikingboard_gerbers_*.zip
3. For SMT Assembly:
   - Click SMT Assembly
   - Upload vikingboard_bom.csv
   - Upload vikingboard_cpl.csv
4. Order

## Cost Estimate
- 5 PCBs: $2-5 USD
- With assembly: $20-50 USD

## Helper Commands
- ./MASTER.sh - Re-export everything
- ./make_jlcpcb.sh - Create JLCPCB bundle only
- ./quick_export.sh - Fast gerber export
- ./open_kicad.sh - Open PCB in KiCad
- ./check_status.sh - Check status

## Fix Unconnected Pads
1. ./open_kicad.sh
2. Tools → Plugin Manager → FreeRouting
3. Tools → FreeRouting → Start
4. Wait 2-5 minutes
5. ./MASTER.sh

Generated: $(date)
QUICKGUIDE

echo "✅ Quick guide created"

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║           ✅ ALL COMPLETE                  ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "📦 PRODUCTION FILES:"
ls -lh "$OUT"/*.{zip,csv,step} 2>/dev/null | awk '{printf "  %-45s %6s\n", $9, $5}'
echo ""
echo "📚 DOCUMENTATION:"
ls -lh "$DOCS"/*.pdf 2>/dev/null | awk '{printf "  %-45s %6s\n", $9, $5}'
echo ""
echo "⚙️  QUALITY:"
echo "  Violations: $VIOL"
echo "  Unconnected: $UNCON pads"
echo ""
echo "📊 STATISTICS:"
echo "  Components: $COMP_COUNT"
echo "  Nets: $NET_COUNT"
echo "  Vias: $VIA_COUNT"

if [[ $UNCON -gt 0 ]]; then
    echo ""
    echo "🔧 FIX ROUTING:"
    echo "  1. ./open_kicad.sh"
    echo "  2. Tools → Plugin Manager → FreeRouting"
    echo "  3. Tools → FreeRouting → Start (wait 2-5 min)"
    echo "  4. ./MASTER.sh"
fi

echo ""
echo "🚀 READY FOR JLCPCB:"
if [[ -n "$JLCZIP" ]] && [[ -f "$JLCZIP" ]]; then
    echo "  EASIEST: Upload $JLCZIP"
    echo "  OR manually:"
fi
echo "  Gerbers: $ZIP"
echo "  BOM: production_output/vikingboard_bom.csv"
echo "  CPL: production_output/vikingboard_cpl.csv"

echo ""
echo "💡 HELPER COMMANDS:"
[[ $KIKIT_OK -eq 1 ]] && echo "  ./make_jlcpcb.sh   - Create JLCPCB bundle"
echo "  ./quick_export.sh  - Fast re-export"
echo "  ./open_kicad.sh    - Open in KiCad"
echo "  ./check_status.sh  - Status check"
echo "  cat QUICKSTART.md  - Full guide"

echo ""
echo "Completed: $(date)" > "$AUTO/last_run.log"
echo "Gerbers: $ZIP" >> "$AUTO/last_run.log"
echo "BOM: $BOM components" >> "$AUTO/last_run.log"
echo "CPL: $CPL placements" >> "$AUTO/last_run.log"
echo "DRC violations: $VIOL" >> "$AUTO/last_run.log"
echo "Unconnected pads: $UNCON" >> "$AUTO/last_run.log"
echo "Components: $COMP_COUNT" >> "$AUTO/last_run.log"

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║    VikingBoard Automation - SUCCESS        ║"
echo "╚════════════════════════════════════════════╝"
echo ""
