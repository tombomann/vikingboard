#!/bin/bash

echo "VIKINGBOARD - KOMPLETT WORKFLOW MED KIKIT"
echo "=========================================="
echo ""

# Steg 1: Åpne KiCad og legg til GND plane
echo "STEG 1: Legg til GND plane"
echo "-------------------------"
echo "1. Kjør: open -a KiCad kicad/Vikingboard.kicad_pro"
echo "2. Åpne PCB Editor"
echo "3. Tools → Scripting Console"
echo "4. Kjør: exec(open('add_gnd_plane.py').read())"
echo "5. Lagre: Ctrl+S"
echo ""
read -p "Trykk Enter når GND plane er lagt til..."

# Steg 2: Legg til board outline med KiKit
echo ""
echo "STEG 2: Legg til board outline"
echo "-------------------------------"
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 << 'PYTHON'
import sys
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

# Last board
board = pcbnew.LoadBoard("kicad/Vikingboard.kicad_pcb")

# Finn bounds
min_x = min_y = float('inf')
max_x = max_y = float('-inf')

for item in board.GetFootprints():
    bbox = item.GetBoundingBox()
    min_x = min(min_x, bbox.GetLeft() / 1000000.0)
    min_y = min(min_y, bbox.GetTop() / 1000000.0)
    max_x = max(max_x, bbox.GetRight() / 1000000.0)
    max_y = max(max_y, bbox.GetBottom() / 1000000.0)

# Legg til margin
margin = 5  # 5mm margin
min_x -= margin
min_y -= margin
max_x += margin
max_y += margin

# Lag edge cuts rectangle
edge_layer = pcbnew.Edge_Cuts
rect_pts = [
    pcbnew.VECTOR2I(int(min_x * 1000000), int(min_y * 1000000)),
    pcbnew.VECTOR2I(int(max_x * 1000000), int(min_y * 1000000)),
    pcbnew.VECTOR2I(int(max_x * 1000000), int(max_y * 1000000)),
    pcbnew.VECTOR2I(int(min_x * 1000000), int(max_y * 1000000)),
    pcbnew.VECTOR2I(int(min_x * 1000000), int(min_y * 1000000))
]

for i in range(len(rect_pts) - 1):
    line = pcbnew.PCB_SHAPE(board)
    line.SetShape(pcbnew.SHAPE_T_SEGMENT)
    line.SetStart(rect_pts[i])
    line.SetEnd(rect_pts[i+1])
    line.SetLayer(edge_layer)
    line.SetWidth(int(0.1 * 1000000))
    board.Add(line)

pcbnew.SaveBoard("kicad/Vikingboard.kicad_pcb", board)
print(f"✅ Board outline lagt til: {max_x-min_x:.1f}mm x {max_y-min_y:.1f}mm")
PYTHON

# Steg 3: Kjør DRC
echo ""
echo "STEG 3: Kjør DRC validering"
echo "----------------------------"
kikit drc run kicad/Vikingboard.kicad_pcb

# Steg 4: Export for JLCPCB
echo ""
echo "STEG 4: Export for JLCPCB"
echo "--------------------------"
kikit fab jlcpcb \
  --assembly \
  --schematic kicad/Vikingboard.kicad_sch \
  kicad/Vikingboard.kicad_pcb \
  production/kikit_output/

echo ""
echo "✅ FERDIG!"
echo "=========="
echo "Files for JLCPCB: production/kikit_output/"
ls -lh production/kikit_output/
