#!/usr/bin/env python3
import pcbnew

# Last PCB
board = pcbnew.LoadBoard("kicad/Vikingboard.kicad_pcb")

# Finn GND net
gnd_net = board.FindNet("GND")
if gnd_net is None:
    print("❌ GND net ikke funnet!")
    exit(1)

# Opprett filled zone på back copper
zone = pcbnew.ZONE(board)
zone.SetLayer(pcbnew.B_Cu)
zone.SetNetCode(gnd_net.GetNetCode())

# Sett zone properties
zone.SetLocalClearance(pcbnew.FromMM(0.2))  # 0.2mm clearance
zone.SetMinThickness(pcbnew.FromMM(0.25))   # 0.25mm min width
zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL_RELIEF)
zone.SetThermalReliefGap(pcbnew.FromMM(0.2))
zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.3))

# Definer zone outline (basert på dine koordinater)
outline = pcbnew.SHAPE_POLY_SET()
outline.NewOutline()
outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(45), pcbnew.FromMM(65)))  # Bottom-left
outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(130), pcbnew.FromMM(65))) # Bottom-right
outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(130), pcbnew.FromMM(115)))# Top-right
outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(45), pcbnew.FromMM(115))) # Top-left

zone.SetOutline(outline)

# Legg til zone
board.Add(zone)

# Fill zone
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

# Lagre
pcbnew.SaveBoard("kicad/Vikingboard.kicad_pcb", board)
print("✅ GND plane lagt til og fylt på B.Cu layer")

