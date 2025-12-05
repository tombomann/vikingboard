#!/bin/bash

echo "📝 Forbereder commit..."

# Legg til alle datablader
git add docs/datasheets/

# Sjekk om det er noe å committe
if git diff --cached --quiet; then
    echo "⚠️  Ingen nye filer å committe"
    exit 0
fi

# Tell antall filer per kategori
RF_COUNT=$(ls docs/datasheets/RF/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
SENSORS_COUNT=$(ls docs/datasheets/Sensors/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
AUDIO_COUNT=$(ls docs/datasheets/Audio/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
POWER_COUNT=$(ls docs/datasheets/Power/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
CONNECTORS_COUNT=$(ls docs/datasheets/Connectors/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)

# Generer commit-melding
COMMIT_MSG="Update component datasheets (Issue #5)

Progress status:
- RF: ${RF_COUNT}/4
- Sensors: ${SENSORS_COUNT}/3
- Audio: ${AUDIO_COUNT}/2
- Power: ${POWER_COUNT}/5
- Connectors: ${CONNECTORS_COUNT}/3

Total: $((RF_COUNT + SENSORS_COUNT + AUDIO_COUNT + POWER_COUNT + CONNECTORS_COUNT))/17 datasheets"

echo ""
echo "Commit-melding:"
echo "----------------------------------------"
echo "$COMMIT_MSG"
echo "----------------------------------------"
echo ""

git commit -m "$COMMIT_MSG"

echo "📤 Pusher til GitHub..."
git push origin main

echo "✅ Ferdig!"
echo ""
echo "📊 Nåværende status:"
echo "RF: ${RF_COUNT}/4"
echo "Sensors: ${SENSORS_COUNT}/3"
echo "Audio: ${AUDIO_COUNT}/2"
echo "Power: ${POWER_COUNT}/5"
echo "Connectors: ${CONNECTORS_COUNT}/3"
