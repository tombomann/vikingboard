#!/bin/bash
set -e

echo "🤖 VikingBoard - Complete CLI Automation Setup"
echo "=============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 required"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "❌ pip3 required"; exit 1; }
command -v brew >/dev/null 2>&1 || { echo "❌ Homebrew required"; exit 1; }
echo "✅ Prerequisites OK"
echo ""

# Install Python automation tools
echo "📦 Installing Python KiCad automation tools..."
pip3 install --upgrade InteractiveHtmlBom
pip3 install --upgrade kikit
pip3 install --upgrade pcbdraw
echo "✅ Python tools installed"
echo ""

# Install FreeRouting
echo "📦 Installing FreeRouting autorouter..."
mkdir -p ~/kicad_automation
cd ~/kicad_automation
if [[ ! -f freerouting.jar ]]; then
    curl -L -o freerouting.jar \
      https://github.com/freerouting/freerouting/releases/download/v1.9.0/freerouting-1.9.0.jar
    echo "✅ FreeRouting downloaded"
else
    echo "✅ FreeRouting already exists"
fi
cd - > /dev/null
echo ""

# Create automation directory structure
echo "📁 Creating automation directories..."
mkdir -p ~/vikingboard/{automation,production_output,reports}
echo "✅ Directories created"
echo ""

# Summary
echo "✅ Installation Complete!"
echo ""
echo "Installed tools:"
echo "  ✓ InteractiveHtmlBom - Interactive assembly guide"
echo "  ✓ KiKit - Production file automation"
echo "  ✓ PcbDraw - PCB visualization"
echo "  ✓ FreeRouting - Auto-router (Java)"
echo ""
echo "Next: Run ./improve_project.sh to enhance VikingBoard"
