#!/bin/bash

echo "FIXING KIKIT INSTALLATION"
echo "=========================="
echo ""

KICAD_PYTHON="/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3"
KICAD_PIP="/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/pip3"

# Sjekk at KiCad Python eksisterer
if [ ! -f "$KICAD_PYTHON" ]; then
    echo "❌ KiCad Python ikke funnet!"
    echo "   Forventet: $KICAD_PYTHON"
    exit 1
fi

echo "✓ KiCad Python funnet: $KICAD_PYTHON"
echo ""

# Avinstaller fra feil Python (hvis nødvendig)
echo "Avinstallerer kikit fra system Python..."
sudo /Library/Frameworks/Python.framework/Versions/3.14/bin/pip3 uninstall -y kikit 2>/dev/null || true

# Installer i riktig Python
echo ""
echo "Installerer kikit i KiCad Python..."
sudo "$KICAD_PIP" install --upgrade kikit

# Lag wrapper script
echo ""
echo "Lager kikit wrapper..."
sudo tee /usr/local/bin/kikit > /dev/null << 'WRAPPER'
#!/bin/bash
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 -m kikit.ui "$@"
WRAPPER

sudo chmod +x /usr/local/bin/kikit

# Test
echo ""
echo "Testing kikit..."
if kikit --help &>/dev/null; then
    echo "✅ KiKit installert og fungerer!"
    kikit --version
else
    echo "❌ KiKit test feilet"
    exit 1
fi
