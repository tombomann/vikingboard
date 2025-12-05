#!/bin/bash
echo "🔍 VikingBoard Full Project Analysis"
echo "===================================="
echo ""

# 1. Git/GitHub status
echo "📦 Git Status:"
git status --short
echo ""
git log --oneline -5
echo ""

# 2. File structure
echo "📁 Project Structure:"
echo "Gerbers: $(ls -lh kicad/vikingboard_gerbers.zip 2>/dev/null | awk '{print $5}' || echo 'MISSING')"
echo "BOM: $(ls -lh pcb_scripts/vikingboard_bom_jlcpcb.csv 2>/dev/null | awk '{print $5}' || echo 'MISSING')"
echo "CPL: $(ls -lh pcb_scripts/vikingboard_cpl_jlcpcb.csv 2>/dev/null | awk '{print $5}' || echo 'MISSING')"
echo "Spec: $(ls -lh pcb_scripts/vikingboard_spec.py 2>/dev/null | awk '{print $5}' || echo 'MISSING')"
echo ""

# 3. Component count
echo "🔩 Component Summary:"
python3 << 'PYEND'
import csv
try:
    with open('pcb_scripts/vikingboard_bom_jlcpcb.csv', 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        total_unique = len(rows)
        total_qty = sum(int(r['Quantity']) for r in rows)
        with_lcsc = sum(1 for r in rows if r['LCSC'] != 'MANUAL')
        print(f"  Unique parts: {total_unique}")
        print(f"  Total quantity: {total_qty}")
        print(f"  With LCSC codes: {with_lcsc}/{total_unique} ({100*with_lcsc//total_unique}%)")
except Exception as e:
    print(f"  Error: {e}")
PYEND
echo ""

# 4. Datasheet status
echo "📚 Datasheet Status:"
./manage_datasheets.sh status 2>/dev/null || echo "  (Run ./manage_datasheets.sh for details)"
echo ""

# 5. KiCad files check
echo "🎨 KiCad Files:"
echo "  PCB: $(ls kicad/*.kicad_pcb 2>/dev/null | wc -l | xargs) file(s)"
echo "  Schematic: $(ls kicad/*.kicad_sch 2>/dev/null | wc -l | xargs) file(s)"
echo "  Gerbers: $(ls kicad/gerbers/*.gbr 2>/dev/null | wc -l | xargs) file(s)"
echo ""

# 6. Documentation
echo "📄 Documentation:"
echo "  README: $(ls README.md 2>/dev/null | wc -l | xargs)"
echo "  Docs: $(ls docs/*.md 2>/dev/null | wc -l | xargs) file(s)"
echo "  Pin mapping: $(ls docs/*nets* 2>/dev/null | wc -l | xargs) file(s)"
echo ""

# 7. Production readiness
echo "✅ Production Checklist:"
checks=0
total=7

[[ -f "kicad/vikingboard_gerbers.zip" ]] && echo "  ✓ Gerbers ZIP" && ((checks++)) || echo "  ✗ Gerbers ZIP"
[[ -f "pcb_scripts/vikingboard_bom_jlcpcb.csv" ]] && echo "  ✓ BOM (JLCPCB format)" && ((checks++)) || echo "  ✗ BOM"
[[ -f "pcb_scripts/vikingboard_cpl.csv" ]] && echo "  ✓ CPL (placement)" && ((checks++)) || echo "  ✗ CPL"
[[ -f "pcb_scripts/vikingboard_spec.py" ]] && echo "  ✓ Spec file" && ((checks++)) || echo "  ✗ Spec"
[[ -d "docs" ]] && echo "  ✓ Documentation" && ((checks++)) || echo "  ✗ Documentation"
[[ -f "kicad/Vikingboard.kicad_pcb" ]] && echo "  ✓ PCB design" && ((checks++)) || echo "  ✗ PCB"
[[ -f "kicad/Vikingboard.kicad_sch" ]] && echo "  ✓ Schematic" && ((checks++)) || echo "  ✗ Schematic"

echo ""
echo "Score: $checks/$total ($(( checks * 100 / total ))%)"
echo ""

echo "🎯 Next Steps:"
if [[ $checks -eq $total ]]; then
    echo "  ✅ Ready for production upload to JLCPCB!"
else
    echo "  ⚠️  Complete missing items before manufacturing"
fi
