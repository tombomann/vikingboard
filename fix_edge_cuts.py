import sys
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

board = pcbnew.LoadBoard("kicad/Vikingboard.kicad_pcb")

# Fjern alle eksisterende Edge.Cuts
print("Fjerner gamle Edge.Cuts linjer...")
items_to_remove = []
for item in board.GetDrawings():
    if item.GetLayer() == pcbnew.Edge_Cuts:
        items_to_remove.append(item)

for item in items_to_remove:
    board.Remove(item)
print(f"✓ Fjernet {len(items_to_remove)} gamle linjer")

# Finn bounds basert på komponenter
min_x = min_y = float('inf')
max_x = max_y = float('-inf')

for fp in board.GetFootprints():
    bbox = fp.GetBoundingBox()
    min_x = min(min_x, bbox.GetLeft())
    min_y = min(min_y, bbox.GetTop())
    max_x = max(max_x, bbox.GetRight())
    max_y = max(max_y, bbox.GetBottom())

# Legg til 5mm margin
margin = 5000000  # 5mm in nm
min_x -= margin
min_y -= margin
max_x += margin
max_y += margin

# Lag ny, riktig lukket outline
print("Lager ny board outline...")
pts = [
    pcbnew.VECTOR2I(min_x, min_y),  # Bottom-left
    pcbnew.VECTOR2I(max_x, min_y),  # Bottom-right
    pcbnew.VECTOR2I(max_x, max_y),  # Top-right
    pcbnew.VECTOR2I(min_x, max_y),  # Top-left
    pcbnew.VECTOR2I(min_x, min_y)   # Close (tilbake til start)
]

for i in range(len(pts) - 1):
    line = pcbnew.PCB_SHAPE(board)
    line.SetShape(pcbnew.SHAPE_T_SEGMENT)
    line.SetStart(pts[i])
    line.SetEnd(pts[i+1])
    line.SetLayer(pcbnew.Edge_Cuts)
    line.SetWidth(100000)  # 0.1mm
    board.Add(line)

width_mm = (max_x - min_x) / 1000000.0
height_mm = (max_y - min_y) / 1000000.0

pcbnew.SaveBoard("kicad/Vikingboard.kicad_pcb", board)
print(f"✅ Board outline: {width_mm:.1f}mm x {height_mm:.1f}mm")
print("💾 Husk å åpne filen i KiCad for å verifisere!")
