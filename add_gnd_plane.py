import pcbnew

# Hent aktiv board
board = pcbnew.GetBoard()
print(f"✓ Board: {board.GetFileName()}")

# Finn GND net
gnd_net = board.FindNet("GND")
if not gnd_net:
    print("❌ GND net ikke funnet!")
else:
    print(f"✓ GND net funnet (NetCode: {gnd_net.GetNetCode()})")
    
    # Opprett filled zone
    zone = pcbnew.ZONE(board)
    zone.SetLayer(pcbnew.B_Cu)
    zone.SetNetCode(gnd_net.GetNetCode())
    
    # Zone properties (KiCad 9.0)
    zone.SetLocalClearance(pcbnew.FromMM(0.2))
    zone.SetMinThickness(pcbnew.FromMM(0.25))
    
    # KiCad 9.0: Bruk integer for pad connection
    # 0=None, 1=Solid, 2=Thermal relief, 3=THT thermal
    zone.SetPadConnection(2)  # Thermal relief
    
    zone.SetThermalReliefGap(pcbnew.FromMM(0.2))
    zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.3))
    
    # Zone outline
    outline = pcbnew.SHAPE_POLY_SET()
    outline.NewOutline()
    outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(45), pcbnew.FromMM(65)))
    outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(130), pcbnew.FromMM(65)))
    outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(130), pcbnew.FromMM(115)))
    outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(45), pcbnew.FromMM(115)))
    zone.SetOutline(outline)
    
    # Add to board
    board.Add(zone)
    
    # Fill zone (KiCad 9.0 metode)
    filler = pcbnew.ZONE_FILLER(board)
    zones = board.Zones()
    filler.Fill(zones)
    
    # Refresh
    pcbnew.Refresh()
    print("✅ GND plane lagt til på B.Cu!")
    print("💾 Lagre nå: File → Save (Ctrl+S)")
