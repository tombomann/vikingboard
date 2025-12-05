import sys
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

board = pcbnew.LoadBoard("kicad/Vikingboard.kicad_pcb")

# Fjern ALLE eksisterende GND zones
print("Fjerner alle eksisterende GND zones...")
zones_removed = 0
for zone in list(board.Zones()):
    if zone.GetNetname() == "GND":
        board.Remove(zone)
        zones_removed += 1

print(f"  ✗ Removed {zones_removed} GND zones")

# Lag EN ny, ren GND zone på B.Cu
print("\nLager ny GND zone på B.Cu...")
gnd_net = board.FindNet("GND")

if gnd_net:
    zone = pcbnew.ZONE(board)
    zone.SetLayer(pcbnew.B_Cu)
    zone.SetNetCode(gnd_net.GetNetCode())
    
    # Settings
    zone.SetLocalClearance(200000)  # 0.2mm
    zone.SetMinThickness(250000)    # 0.25mm
    zone.SetPadConnection(2)         # Thermal relief
    zone.SetThermalReliefGap(200000)
    zone.SetThermalReliefSpokeWidth(300000)
    
    # Outline (board bounds)
    outline = pcbnew.SHAPE_POLY_SET()
    outline.NewOutline()
    outline.Append(pcbnew.VECTOR2I(45000000, 65000000))
    outline.Append(pcbnew.VECTOR2I(135000000, 65000000))
    outline.Append(pcbnew.VECTOR2I(135000000, 115000000))
    outline.Append(pcbnew.VECTOR2I(45000000, 115000000))
    zone.SetOutline(outline)
    
    board.Add(zone)
    print("  ✓ Created GND zone on B.Cu")
    
    # Fill
    print("\nFilling zone...")
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    
    pcbnew.SaveBoard("kicad/Vikingboard.kicad_pcb", board)
    print("\n✅ GND zone rebuilt successfully!")
else:
    print("❌ ERROR: GND net not found!")
