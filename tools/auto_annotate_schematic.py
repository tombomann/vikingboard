import csv
from pathlib import Path

LCSC_MAP = {
    "ESP32-S3-WROOM-1U-N16R8": "C3046459",
    "CC1101": "C111074",
    "SX1262": "C2834871",
    "NRF24L01": "C109041",
    "PN532": "C510389",
    "EM4100": "C148677",
    "BME280": "C96014",
    "BH1750": "C212757",
    "MPU6050": "C84194",
    "NEO-6M": "C109017",
    "MPR121": "C103878",
    "WS2812B": "C47108",
    "USB-C": "C2886994",
    "SMA": "C168445",
    "10µF": "C15849",
    "100nF": "C14663"
}

def annotate_and_generate_bom():
    """Generer JLCPCB BOM fra eksisterende production/bom.csv"""
    
    # 1. Les production/bom.csv (generert av MASTER.sh)
    bom_path = Path("production/bom.csv")
    if not bom_path.exists():
        # Prøv production_output/ (KiKit output)
        bom_path = Path("production_output/vikingboard_bom.csv")
    
    if not bom_path.exists():
        print("❌ Ingen BOM funnet - kjør ./MASTER.sh først")
        return False
    
    print(f"📋 Leser BOM fra {bom_path}")
    
    with open(bom_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # 2. Match LCSC-koder
    components = []
    for row in rows:
        value = row.get("Value", row.get("value", ""))  # Handle både formater
        refs = row.get("Refs", row.get("ref", row.get("Id", "")))
        footprint = row.get("Footprint", row.get("footprint", ""))
        
        # Match LCSC
        lcsc = "MANUAL"
        for key, code in LCSC_MAP.items():
            if key.lower() in value.lower():
                lcsc = code
                break
        
        components.append({
            "Comment": value,
            "Designator": refs,
            "Footprint": footprint,
            "LCSC Part #": lcsc
        })
    
    # 3. Skriv JLCPCB-format BOM
    Path("manufacturing").mkdir(exist_ok=True)
    output_path = Path("manufacturing/BOM_JLCPCB.csv")
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, ["Comment", "Designator", "Footprint", "LCSC Part #"])
        writer.writeheader()
        writer.writerows(components)
    
    print(f"✅ {len(components)} komponenter annotert med LCSC-koder")
    print(f"📄 Output: {output_path}")
    
    # 4. Vis oppsummering
    lcsc_matched = sum(1 for c in components if c["LCSC Part #"] != "MANUAL")
    manual_needed = len(components) - lcsc_matched
    
    print(f"   ✓ {lcsc_matched} med LCSC-kode")
    if manual_needed > 0:
        print(f"   ⚠️  {manual_needed} trenger manuell LCSC-kode")
        manual_comps = [c["Comment"] for c in components if c["LCSC Part #"] == "MANUAL"]
        print(f"      Mangler: {', '.join(manual_comps[:3])}...")
    
    # 5. Valider kritiske komponenter
    critical = ["ESP32-S3", "CC1101", "SX1262", "NRF24"]
    found = [c for c in critical if any(c in comp["Comment"] for comp in components)]
    missing = [c for c in critical if c not in found]
    
    if missing:
        print(f"⚠️  Kritiske komponenter mangler i BOM: {missing}")
        print("   → Legg til i KiCad schematic og kjør ./MASTER.sh igjen")
    
    return True

if __name__ == "__main__":
    success = annotate_and_generate_bom()
    exit(0 if success else 1)
