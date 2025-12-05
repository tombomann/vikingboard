#!/bin/bash
echo "🔧 Quick Fix VikingBoard"

# Test alle verktøy
echo "Testing tools:"
command -v java && echo "✅ Java" || echo "❌ Java"
command -v generate_interactive_bom && echo "✅ iBOM" || echo "❌ iBOM" 
command -v kikit && echo "✅ KiKit" || echo "❌ KiKit"
[[ -f "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli" ]] && echo "✅ KiCad CLI" || echo "❌ KiCad CLI"

echo ""
echo "Files:"
[[ -f "kicad/Vikingboard.kicad_pcb" ]] && echo "✅ PCB" || echo "❌ PCB"
[[ -f "kicad/Vikingboard.kicad_sch" ]] && echo "✅ SCH" || echo "❌ SCH"
