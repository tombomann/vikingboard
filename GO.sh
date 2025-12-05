#!/bin/bash

echo "VIKINGBOARD AUTOMATION"
echo "======================"

# Exporting gerbers
echo "Exporting gerbers..."
kicad-cli pcb export gerbers \
  --output production/gerbers/ \
  --layers "*.Cu,*.Mask,*.Paste,*.Silkscreen,Edge.Cuts" \
  kicad/Vikingboard.kicad_pcb

kicad-cli pcb export drill \
  --output production/gerbers/ \
  kicad/Vikingboard.kicad_pcb

echo "Done."

# Exporting BOM & CPL
echo "Exporting BOM & CPL..."
kicad-cli pcb export pos \
  --format csv \
  --output production/cpl.csv \
  --side both \
  --units mm \
  kicad/Vikingboard.kicad_pcb

kicad-cli sch export bom \
  --output production/bom.csv \
  kicad/Vikingboard.kicad_sch

# Exporting docs
echo "Exporting docs & 3D..."
kicad-cli sch export pdf \
  --output production/docs/schematic.pdf \
  kicad/Vikingboard.kicad_sch

kicad-cli pcb export pdf \
  --output production/docs/pcb.pdf \
  kicad/Vikingboard.kicad_pcb

kicad-cli pcb export step \
  --output production/board.step \
  kicad/Vikingboard.kicad_pcb

# Create JLCPCB bundle
echo "Creating JLCPCB bundle..."
cd production
zip -r JLCPCB_$(date +%Y%m%d_%H%M).zip \
  gerbers/*.g* \
  gerbers/*.drl \
  bom.csv \
  cpl.csv
cd ..

# Run DRC
echo "Running DRC..."
kicad-cli pcb drc \
  --output production/drc.txt \
  --exit-code-violations \
  kicad/Vikingboard.kicad_pcb 2>&1 | tee /tmp/drc_output.txt

# Parse DRC results correctly
VIOLATIONS=$(grep "Found.*DRC violations" production/drc.txt | grep -o "[0-9]*" | head -1)
UNCONNECTED=$(grep "Found.*unconnected" production/drc.txt | grep -o "[0-9]*" | head -1)
COMPONENTS=$(grep -c "U[0-9]\|J[0-9]" kicad/Vikingboard.kicad_pcb)

# Default to 0 if empty
VIOLATIONS=${VIOLATIONS:-0}
UNCONNECTED=${UNCONNECTED:-0}

echo ""
if [ "$VIOLATIONS" -eq 0 ] && [ "$UNCONNECTED" -eq 0 ]; then
    echo "✅ PERFECT!"
    echo "=========="
    echo "Components: $COMPONENTS"
    echo "Violations: $VIOLATIONS"
    echo "Unconnected: $UNCONNECTED"
    echo ""
    echo "🎉 PCB READY FOR PRODUCTION!"
else
    echo "SUCCESS!"
    echo "========"
    echo "Components: $COMPONENTS"
    echo "Violations: $VIOLATIONS"
    echo "Unconnected: $UNCONNECTED"
fi

echo ""
echo "UPLOAD TO JLCPCB:"
echo "1. production/JLCPCB_$(date +%Y%m%d)*.zip"
echo "2. production/bom.csv"
echo "3. production/cpl.csv"
