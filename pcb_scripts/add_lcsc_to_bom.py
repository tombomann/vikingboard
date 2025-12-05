import csv

# Read current BOM
with open('vikingboard_bom.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Add LCSC column (placeholder - you must fill manually)
with open('vikingboard_bom_lcsc.csv', 'w', newline='') as f:
    fieldnames = ['Designator', 'Value', 'Footprint', 'LCSC', 'Quantity']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in rows:
        writer.writerow({
            'Designator': row['Refs'],
            'Value': row['Value'],
            'Footprint': row['Footprint'],
            'LCSC': 'FILL_MANUALLY',  # ← Must add real LCSC codes
            'Quantity': row['Qty']
        })

print("Created vikingboard_bom_lcsc.csv")
print("You must manually add LCSC part numbers!")
