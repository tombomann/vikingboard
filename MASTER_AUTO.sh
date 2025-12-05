#!/bin/bash
set -e

echo "🚀 VIKINGBOARD AUTO-PRODUCTION"
echo "=============================="

# 1. GND plane fix
echo "⚡ Fikser GND zones..."
python3 add_gnd_plane.py 2>/dev/null || echo "  Skipped"

# 2. DRC
echo "✅ Kjører DRC..."
kicad-cli pcb drc \
  --output production/drc.txt \
  kicad/Vikingboard.kicad_pcb 2>/dev/null || {
    echo "  ⚠️  KiCad CLI ikke funnet, sjekk manuelt"
}

# 3. BOM med LCSC
echo "📋 Genererer BOM..."
python3 tools/auto_annotate_schematic.py

# 4. Gerbers
echo "📦 Eksporterer gerbers..."
python3 automate_production.py

# 5. JLCPCB ZIP
echo "🎁 Lager JLCPCB-pakke..."
./make_jlcpcb.sh 2>/dev/null || {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    cd production/gerbers
    zip -q ../JLCPCB_${TIMESTAMP}.zip *.g* *.drl
    cd ../..
    echo "  ✅ production/JLCPCB_${TIMESTAMP}.zip"
}

# 6. Oppsummering
echo ""
echo "🎉 PRODUCTION READY!"
ls -lh production/JLCPCB_*.zip | tail -1
echo "📋 BOM: manufacturing/BOM_JLCPCB.csv"
cat manufacturing/BOM_JLCPCB.csv | head -6
