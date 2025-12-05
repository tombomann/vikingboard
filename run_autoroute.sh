#!/bin/bash
echo "🤖 VikingBoard FreeRouting Automation"
echo "====================================="

# Check Java
echo "Checking Java 21..."
java -version 2>&1 | grep "21\." || {
    echo "❌ Java 21 not found"
    echo "Install: brew install openjdk@21"
    exit 1
}
echo "✅ Java 21 OK"

# Backup PCB
echo ""
echo "📦 Backing up PCB..."
cp kicad/Vikingboard.kicad_pcb kicad/Vikingboard.kicad_pcb.backup
echo "✅ Backup saved"

echo ""
echo "📋 Next steps (manual):"
echo ""
echo "1. Open KiCad PCB Editor"
echo "   open -a KiCad ~/vikingboard/kicad/Vikingboard.kicad_pcb"
echo ""
echo "2. Add Board Outline (Edge.Cuts layer):"
echo "   - Select Edge.Cuts layer"
echo "   - Draw → Rectangle"
echo "   - Draw around entire board"
echo ""
echo "3. Run FreeRouting:"
echo "   - Tools → External Plugins → FreeRouting"
echo "   - Click 'Start Autorouter'"
echo "   - Wait 2-5 minutes"
echo "   - Review results"
echo ""
echo "4. Save and check:"
echo "   - File → Save"
echo "   - Inspect → Design Rules Checker"
echo "   - Fix any remaining errors"
echo ""
echo "5. Re-export production files:"
echo "   cd ~/vikingboard/kicad"
echo "   /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export gerbers \\"
echo "     --output gerbers/ Vikingboard.kicad_pcb"
echo ""
