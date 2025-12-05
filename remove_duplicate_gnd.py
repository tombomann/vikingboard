import sys
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

board = pcbnew.LoadBoard("kicad/Vikingboard.kicad_pcb")

gnd_zones = {}
for zone in board.Zones():
    if zone.GetNetname() == "GND":
        layer = zone.GetLayer()
        if layer not in gnd_zones:
            gnd_zones[layer] = zone
        else:
            board.Remove(zone)

filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
pcbnew.SaveBoard("kicad/Vikingboard.kicad_pcb", board)
print("✅ Duplicate GND zones removed!")
