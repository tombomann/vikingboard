#!/bin/bash

echo "📁 Organiserer datablader..."

# RF
mv ~/Downloads/*E22*.pdf docs/datasheets/RF/ 2>/dev/null && echo "✅ LoRa flyttet"

# Sensors
mv ~/Downloads/*MPU*.pdf docs/datasheets/Sensors/ 2>/dev/null && echo "✅ MPU-6050 flyttet"
mv ~/Downloads/*BME280*.pdf docs/datasheets/Sensors/ 2>/dev/null && echo "✅ BME280 flyttet"
mv ~/Downloads/*BH1750*.pdf docs/datasheets/Sensors/ 2>/dev/null && echo "✅ BH1750 flyttet"
mv ~/Downloads/*bh1750*.pdf docs/datasheets/Sensors/ 2>/dev/null

# Audio
mv ~/Downloads/*SPH0645*.pdf docs/datasheets/Audio/ 2>/dev/null && echo "✅ SPH0645 flyttet"
mv ~/Downloads/*MAX98357*.pdf docs/datasheets/Audio/ 2>/dev/null && echo "✅ MAX98357 flyttet"

# Power
mv ~/Downloads/*IP2721*.pdf docs/datasheets/Power/ 2>/dev/null && echo "✅ IP2721 flyttet"
mv ~/Downloads/*AMS1117*.pdf docs/datasheets/Power/ 2>/dev/null && echo "✅ AMS1117 flyttet"
mv ~/Downloads/*ds1117*.pdf docs/datasheets/Power/ 2>/dev/null
mv ~/Downloads/*XC6206*.pdf docs/datasheets/Power/ 2>/dev/null && echo "✅ XC6206 flyttet"
mv ~/Downloads/*TPS2051*.pdf docs/datasheets/Power/ 2>/dev/null && echo "✅ TPS2051 flyttet"
mv ~/Downloads/*tps2051*.pdf docs/datasheets/Power/ 2>/dev/null
mv ~/Downloads/*USBLC6*.pdf docs/datasheets/Power/ 2>/dev/null && echo "✅ USBLC6 flyttet"
mv ~/Downloads/*usblc6*.pdf docs/datasheets/Power/ 2>/dev/null

# Connectors
mv ~/Downloads/*USB4085*.pdf docs/datasheets/Connectors/ 2>/dev/null && echo "✅ USB-C flyttet"
mv ~/Downloads/*usb4085*.pdf docs/datasheets/Connectors/ 2>/dev/null
mv ~/Downloads/*U.FL*.pdf docs/datasheets/Connectors/ 2>/dev/null && echo "✅ U.FL flyttet"
mv ~/Downloads/*ufl*.pdf docs/datasheets/Connectors/ 2>/dev/null

echo ""
echo "📊 Status:"
echo "RF: $(ls docs/datasheets/RF/*.pdf 2>/dev/null | wc -l | xargs) filer"
echo "Sensors: $(ls docs/datasheets/Sensors/*.pdf 2>/dev/null | wc -l | xargs) filer"
echo "Audio: $(ls docs/datasheets/Audio/*.pdf 2>/dev/null | wc -l | xargs) filer"
echo "Power: $(ls docs/datasheets/Power/*.pdf 2>/dev/null | wc -l | xargs) filer"
echo "Connectors: $(ls docs/datasheets/Connectors/*.pdf 2>/dev/null | wc -l | xargs) filer"
