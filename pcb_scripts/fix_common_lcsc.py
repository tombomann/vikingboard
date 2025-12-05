import csv

# Common LCSC codes for standard components
common_lcsc = {
    '10µF': 'C15850',      # 10µF 0805 cap
    '100nF': 'C14663',     # 0.1µF 0805 cap
    '10k': 'C17513',       # 10k 0805 resistor
    '1k': 'C17513',        # 1k 0805 resistor
    '4.7k': 'C17673',      # 4.7k 0805 resistor
    '100k': 'C17407',      # 100k 0805 resistor
}

# Read current BOM
rows = []
with open('vikingboard_bom_jlcpcb.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        value = row['Value']
        if row['LCSC'] == 'MANUAL':
            # Try to match common component
            for key, lcsc in common_lcsc.items():
                if key in value:
                    row['LCSC'] = lcsc
                    break
        rows.append(row)

# Write back
with open('vikingboard_bom_jlcpcb.csv', 'w', newline='') as f:
    fieldnames = ['Designator', 'Value', 'Footprint', 'LCSC', 'Quantity']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Updated BOM with common LCSC codes")
