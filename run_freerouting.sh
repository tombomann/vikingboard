#!/bin/bash

echo "VIKINGBOARD - FREEROUTING AUTOROUTER"
echo "====================================="
echo ""

# Steg 1: Export Specctra DSN
echo "STEG 1: Eksporterer Specctra DSN..."
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export specctra-dsn \
  kicad/Vikingboard.kicad_pcb \
  -o vikingboard.dsn

if [ -f "vikingboard.dsn" ]; then
    echo "✅ vikingboard.dsn opprettet"
else
    echo "❌ Feil: Kunne ikke lage DSN-fil"
    exit 1
fi

# Steg 2: Last ned FreeRouting hvis ikke finnes
echo ""
echo "STEG 2: Sjekker FreeRouting..."
if [ ! -f "freerouting.jar" ]; then
    echo "Laster ned FreeRouting..."
    curl -L -o freerouting.jar \
      https://github.com/freerouting/freerouting/releases/download/v1.9.0/freerouting-1.9.0.jar
    echo "✅ FreeRouting lastet ned"
else
    echo "✅ FreeRouting allerede installert"
fi

# Steg 3: Kjør FreeRouting
echo ""
echo "STEG 3: Starter FreeRouting..."
echo ""
echo "I FreeRouting GUI:"
echo "1. 'Open Board' → velg vikingboard.dsn"
echo "2. 'Autorouter' → 'Start'"
echo "3. Vent til ferdig (1-2 min)"
echo "4. 'File' → 'Export Specctra Session'"
echo "5. Lagre som: vikingboard.ses"
echo ""
read -p "Trykk Enter for å starte FreeRouting..."

java -jar freerouting.jar

# Steg 4: Import tilbake
echo ""
echo "STEG 4: Import routing tilbake til KiCad"
echo ""
if [ -f "vikingboard.ses" ]; then
    echo "✅ vikingboard.ses funnet!"
    echo ""
    echo "Kjør dette i KiCad PCB Editor:"
    echo "  File → Import → Specctra Session"
    echo "  Velg: vikingboard.ses"
    echo ""
    echo "Eller bruk kommando:"
    echo "  /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb import specctra-ses \\"
    echo "    vikingboard.ses \\"
    echo "    -o kicad/Vikingboard.kicad_pcb"
else
    echo "⚠️  vikingboard.ses ikke funnet"
    echo "   Husk å eksportere fra FreeRouting!"
fi

echo ""
echo "STEG 5: Verifiser resultat"
echo "  ./GO.sh"
