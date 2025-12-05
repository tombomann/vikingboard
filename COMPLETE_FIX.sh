#!/bin/bash

echo "VIKINGBOARD - KOMPLETT FIX"
echo "=========================="
echo ""

# Steg 1: Fix Edge.Cuts outline
echo "STEG 1: Fikser Edge.Cuts outline..."
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 << 'PYTHON'
import sys
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

board = pcbnew.LoadBoard("kicad/Vikingboard.kicad_pcb")

# Board outline coordinates (med margin)
pts = [
    pcbnew.VECTOR2I(45000000, 65000000),    # Bottom-left
    pcbnew.VECTOR2I(135000000, 65000000),   # Bottom-right
    pcbnew.VECTOR2I(135000000, 115000000),  # Top-right
    pcbnew.VECTOR2I(45000000, 115000000),   # Top-left
    pcbnew.VECTOR2I(45000000, 65000000)     # Close path
]

# Lag Edge.Cuts rectangle
for i in range(len(pts) - 1):
    line = pcbnew.PCB_SHAPE(board)
    line.SetShape(pcbnew.SHAPE_T_SEGMENT)
    line.SetStart(pts[i])
    line.SetEnd(pts[i+1])
    line.SetLayer(pcbnew.Edge_Cuts)
    line.SetWidth(100000)  # 0.1mm
    board.Add(line)

pcbnew.SaveBoard("kicad/Vikingboard.kicad_pcb", board)
print("✅ Edge.Cuts outline lagt til: 90mm x 50mm")
PYTHON

echo ""
echo "STEG 2: Kjør DRC..."
./GO.sh

echo ""
echo "STEG 3: ROUTING GUIDE"
echo "====================="
echo ""
echo "Du har 28 forbindelser som må routes manuelt."
echo ""
echo "ANBEFALING: Bruk FreeRouting (autorouter)"
echo ""
echo "1. Last ned FreeRouting:"
echo "   https://github.com/freerouting/freerouting/releases"
echo ""
echo "2. I KiCad PCB Editor:"
echo "   - File → Export → Specctra DSN"
echo "   - Lagre som: vikingboard.dsn"
echo ""
echo "3. Åpne FreeRouting:"
echo "   - Open Board → velg vikingboard.dsn"
echo "   - Autorouter → Start"
echo "   - Vent til ferdig (1-2 min)"
echo "   - File → Export Specctra Session"
echo "   - Lagre som: vikingboard.ses"
echo ""
echo "4. Tilbake i KiCad:"
echo "   - File → Import → Specctra Session"
echo "   - Velg vikingboard.ses"
echo "   - Alle 28 forbindelser routes automatisk!"
echo ""
echo "5. Kjør ./GO.sh igjen"
echo "   - Forventet: 0 violations, 0 unconnected"
echo ""
