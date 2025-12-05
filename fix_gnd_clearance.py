import sys
sys.path.insert(0, '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import pcbnew

board = pcbnew.LoadBoard("kicad/Vikingboard.kicad_pcb")

print("Fikser GND zone clearance...")
fixed = 0

for zone in board.Zones():
    if zone.GetNetname() == "GND":
        # Sett riktig clearance (0.2mm = 200000 nm)
        zone.SetLocalClearance(200000)  # 0.2mm
        zone.SetMinThickness(250000)    # 0.25mm
        zone.SetThermalReliefGap(200000)  # 0.2mm
        zone.SetThermalReliefSpokeWidth(300000)  # 0.3mm
        fixed += 1
        print(f"  ✓ Fixed GND zone on layer {zone.GetLayerName()}")

# Refill zones
print("\nRefilling zones...")
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

pcbnew.SaveBoard("kicad/Vikingboard.kicad_pcb", board)
print(f"\n✅ Fixed {fixed} GND zone(s)")
print("💾 Run ./GO.sh to verify!")
