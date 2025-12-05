import csv
import re

# Parse spec for LCSC codes
spec_path = 'vikingboard_spec.py'
lcsc_map = {}

with open(spec_path, 'r') as f:
    content = f.read()
    # Extract name and lcsc pairs
    matches = re.findall(r'"name":\s*"([^"]+)".*?"lcsc":\s*"([^"]+)"', content, re.DOTALL)
    for name, lcsc in matches:
        lcsc_map[name] = lcsc

# Read KiCad BOM
with open('vikingboard_bom.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Write JLCPCB BOM
with open('vikingboard_bom_jlcpcb.csv', 'w', newline='') as f:
    fieldnames = ['Designator', 'Value', 'Footprint', 'LCSC', 'Quantity']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in rows:
        value = row['Value']
        # Try to find LCSC code
        lcsc = lcsc_map.get(value, 'MANUAL')
        
        writer.writerow({
            'Designator': row['Refs'],
            'Value': value,
            'Footprint': row['Footprint'],
            'LCSC': lcsc,
            'Quantity': row['Qty']
        })

print("Created vikingboard_bom_jlcpcb.csv")
print("\nComponents with LCSC codes:")
for k, v in lcsc_map.items():
    print(f"  {k}: {v}")
