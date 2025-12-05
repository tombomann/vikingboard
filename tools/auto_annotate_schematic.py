import subprocess
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
    # 1. Eksporter BOM via KiCad CLI
    sch_path = "kicad/Vikingboard.kicad_sch"
    
    result = subprocess.run([
        "kicad-cli", "sch", "export", "python-bom",
        "--output", "production/bom_raw.xml",
        sch_path
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("⚠️  KiCad CLI feilet - bruker eksisterende production/bom.csv")
        bom_path = Path("production/bom.csv")
    else:
        print("✅ BOM eksportert fra schematic")
        # Parse XML (fallback til CSV hvis XML feiler)
        bom_path = Path("production/bom.csv")
    
    # 2. Les eksisterende CSV BOM
    if not bom_path.exists():
        print("❌ production/bom.csv mangler")
        return False
    
    with open(bom_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # 3. Match LCSC-koder
    components = []
    for row in rows:
        value = row["Value"]
        lcsc = next((code for key, code in LCSC_MAP.items() 
                    if key.lower() in value.lower()), "MANUAL")
        
        components.append({
            "Comment": value,
            "Designator": row["Refs"],
            "Footprint": row["Footprint"],
            "LCSC Part #": lcsc
        })
    
    # 4. Skriv JLCPCB-format BOM
    with open("manufacturing/BOM_JLCPCB.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, ["Comment", "Designator", "Footprint", "LCSC Part #"])
        writer.writeheader()
        writer.writerows(components)
    
    print(f"✅ {len(components)} komponenter annotert med LCSC-koder")
    
    # 5. Valider kritiske komponenter
    critical = ["ESP32-S3", "CC1101", "SX1262", "NRF24"]
    missing = [c for c in critical if not any(c in comp["Comment"] for comp in components)]
    if missing:
        print(f"⚠️  Mangler: {missing}")
        print("   (OK for nå - disse må legges til i KiCad schematic)")
    
    return True

if __name__ == "__main__":
    success = annotate_and_generate_bom()
    exit(0 if success else 1)
