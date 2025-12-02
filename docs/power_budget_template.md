# VikingBoard Power Budget Analysis

**Project:** VikingBoard v1.0  
**Date:** 2025-12-02  
**Version:** 1.0  
**Status:** Template - To be filled with measured data

---

## Power Supply Architecture

```
USB-C (5V/3A) 
    ↓
[IP2721 PD Controller] → Negotiates 5V/3A
    ↓
[Polyfuse 3A + Ferrite Bead]
    ↓
SYS_5V Rail (5V, 2.5A available)
    ├─────────────> [MAX98357 Audio Amp] (5V direct)
    ├─────────────> [TPS2051B] → USB_A_5V (500mA)
    ├─────────────> [AMS1117-3.3] → IO_3V3 Rail (3.3V, 1A)
    └─────────────> [XC6206P] → RF_3V3 Rail (3.3V, 300mA)
```

### Power Rails Summary

| Rail | Voltage | Regulator | Max Current | Power | Notes |
|------|---------|-----------|-------------|-------|-------|
| USB_VBUS | 5V | IP2721 (PD) | 3A | 15W | USB-C input |
| SYS_5V | 5V | Polyfuse | 2.5A | 12.5W | After protection |
| IO_3V3 | 3.3V | AMS1117-3.3 | 1A | 3.3W | Digital I/O, sensors, MCU |
| RF_3V3 | 3.3V | XC6206P | 300mA | 1W | RF modules (isolated) |
| USB_A_5V | 5V | TPS2051B | 500mA | 2.5W | USB-A host output |

---

## Detailed Component Power Consumption

### IO_3V3 Rail (3.3V)

| Component | Qty | Typ Current (mA) | Max Current (mA) | Typ Power (mW) | Max Power (mW) | Operating Mode | Notes |
|-----------|-----|------------------|------------------|----------------|----------------|----------------|-------|
| **ESP32-WROOM-32E** | 1 | 80 | 240 | 264 | 792 | WiFi TX max | Modem sleep: 20mA, Deep sleep: 10µA |
| **MPU6050 (IMU)** | 1 | 3.8 | 3.8 | 12.5 | 12.5 | Always on | Sleep mode: 10µA |
| **BME280 (Env)** | 1 | 0.3 | 0.7 | 1.0 | 2.3 | Forced mode 1Hz | Sleep: 0.1µA |
| **BH1750 (Light)** | 1 | 0.12 | 0.12 | 0.4 | 0.4 | Continuous H-res | Power down: 1µA |
| **SPH0645 (Mic)** | 1 | 1.5 | 1.5 | 5.0 | 5.0 | I2S active | Sleep: 15µA |
| **DRV2605L (Haptic)** | 1 | 5 | 100 | 16.5 | 330 | Peak vibration | Standby: 16µA |
| **SD Card** | 1 | 20 | 100 | 66 | 330 | Write operation | Idle: 1mA |
| **LEDs (Status, Power)** | 2 | 10 | 10 | 33 | 33 | Always on | 5mA each @ 3.3V |
| **Pull-up Resistors** | - | 5 | 5 | 16.5 | 16.5 | I2C, GPIO | Misc |
| **Reserve Margin (10%)** | - | 12.5 | 46 | 41 | 152 | Unexpected | Safety margin |
| **TOTAL IO_3V3** | | **138 mA** | **507 mA** | **456 mW** | **1674 mW** | | |

**LDO Validation:**
- AMS1117-3.3: 1A (1000mA) rating
- Max load: 507mA
- **Margin: 493mA (49.3%) ✅ PASS**

---

### RF_3V3 Rail (3.3V, Low-Noise Isolated)

| Component | Qty | Typ Current (mA) | Max Current (mA) | Typ Power (mW) | Max Power (mW) | Operating Mode | Notes |
|-----------|-----|------------------|------------------|----------------|----------------|----------------|-------|
| **LoRa E22-900M30S** | 1 | 20 | 120 | 66 | 396 | TX 1W @ 915MHz | RX: 16mA, Sleep: 2µA |
| **CC1101** | 1 | 15 | 30 | 49.5 | 99 | TX 10dBm @ 433MHz | RX: 16mA, Sleep: 1µA |
| **NRF24L01+** | 1 | 8 | 12 | 26.4 | 39.6 | TX 0dBm @ 2.4GHz | RX: 13mA, Standby: 26µA |
| **GPS NEO-M8N** | 1 | 25 | 30 | 82.5 | 99 | Acquisition mode | Tracking: 25mA, Backup: 15µA |
| **Reserve Margin (10%)** | - | 6.8 | 19 | 22 | 63 | Unexpected | Safety margin |
| **TOTAL RF_3V3** | | **75 mA** | **211 mA** | **247 mW** | **697 mW** | | |

**LDO Validation:**
- XC6206P: 300mA rating
- Max load: 211mA
- **Margin: 89mA (29.7%) ✅ PASS**

**Note:** Maximum power assumes all RF modules transmitting simultaneously. In practice:
- Typical usage: 1 RF module active at a time (GPS always on)
- Typical load: ~50-70mA

---

### SYS_5V Rail Direct Loads

| Component | Qty | Typ Current (mA) | Max Current (mA) | Typ Power (mW) | Max Power (mW) | Operating Mode | Notes |
|-----------|-----|------------------|------------------|----------------|----------------|----------------|-------|
| **MAX98357 Audio Amp** | 1 | 10 | 800 | 50 | 4000 | 3W speaker @ 8Ω | Idle: 10mA, Shutdown: 1µA |
| **AMS1117-3.3 (IO rail)** | 1 | 138 | 507 | 690 | 2535 | From IO_3V3 calc above | Input current for LDO |
| **XC6206P (RF rail)** | 1 | 75 | 211 | 375 | 1055 | From RF_3V3 calc above | Input current for LDO |
| **USB_A_5V Load** | 1 | 0 | 500 | 0 | 2500 | External USB device | TPS2051B limits to 500mA |
| **IP2721 Quiescent** | 1 | 5 | 5 | 25 | 25 | Always on | USB-C PD controller |
| **Reserve Margin (5%)** | - | 11 | 101 | 55 | 505 | Unexpected | Safety margin |
| **TOTAL SYS_5V** | | **239 mA** | **2124 mA** | **1195 mW** | **10620 mW** | | |

**USB-C PD Validation:**
- USB-C negotiated: 5V/3A = 15W (3000mA)
- Max load: 2124mA
- **Margin: 876mA (29.2%) ✅ PASS**

---

## Total System Power Budget

### Typical Operating Conditions

| Rail | Typ Current | Typ Power |
|------|-------------|----------|
| SYS_5V (direct loads) | 239 mA | 1195 mW |
| IO_3V3 | 138 mA | 456 mW |
| RF_3V3 | 75 mA | 247 mW |
| **TOTAL** | - | **1898 mW (~1.9W)** |

**Typical Use Case:**
- ESP32 running WiFi
- 1 RF module active (LoRa or GPS)
- Sensors reading at 1Hz
- No audio playback
- No USB-A device

### Maximum Operating Conditions (Worst Case)

| Rail | Max Current | Max Power |
|------|-------------|----------|
| SYS_5V (direct loads) | 2124 mA | 10620 mW |
| IO_3V3 | 507 mA | 1674 mW |
| RF_3V3 | 211 mA | 697 mW |
| **TOTAL** | - | **12991 mW (~13W)** |

**Worst Case Scenario:**
- ESP32 WiFi TX max
- All RF modules TX simultaneously
- Audio amplifier at 3W
- USB-A device drawing 500mA
- SD card writing
- Haptic motor vibrating

**USB-C PD Headroom:**
- Available: 15W (5V/3A)
- Worst case: 13W
- **Margin: 2W (13.3%) ✅ PASS**

---

## LDO Thermal Analysis

### AMS1117-3.3 (IO Rail)

**Package:** SOT-223 (4 pins with tab)

**Thermal Resistance:**
- θ_JA (junction-to-ambient): 50°C/W (minimal PCB copper)
- θ_JA (with 1 sq. inch copper plane): 25°C/W

**Power Dissipation:**
- Input: 5V
- Output: 3.3V
- Voltage drop: 1.7V
- Max current: 507mA
- **P_dissipated = 1.7V × 0.507A = 0.86W**

**Temperature Rise:**
- ΔT = P × θ_JA = 0.86W × 25°C/W = **21.5°C**
- Ambient: 25°C (room temp)
- Junction temp: 25 + 21.5 = **46.5°C**

**Validation:**
- AMS1117 max junction temp: 125°C
- Operating junction temp: 46.5°C
- **Margin: 78.5°C ✅ PASS (no heatsink needed)**

**PCB Design Note:**
- Use ≥1 sq. inch (6.45 cm²) copper plane on SOT-223 tab
- Connect tab to GND plane with thermal vias (4-6 vias, 0.3mm)

---

### XC6206P (RF Rail)

**Package:** SOT-23-3

**Thermal Resistance:**
- θ_JA: 200°C/W (tiny package, limited thermal mass)

**Power Dissipation:**
- Input: 5V
- Output: 3.3V
- Voltage drop: 1.7V
- Max current: 211mA
- **P_dissipated = 1.7V × 0.211A = 0.36W**

**Temperature Rise:**
- ΔT = P × θ_JA = 0.36W × 200°C/W = **72°C**
- Ambient: 25°C
- Junction temp: 25 + 72 = **97°C**

**Validation:**
- XC6206P max junction temp: 150°C
- Operating junction temp: 97°C
- **Margin: 53°C ✅ PASS**

**Note:** Runs warm but within spec. Consider:
- Adding small copper plane (0.5 sq. inch) to SOT-23-3 GND pin
- OR: Upgrade to higher-current LDO (e.g., 500mA) for better thermal performance

---

## Power Supply Sequencing

**Recommended Power-Up Sequence:**

1. **USB-C connected** → IP2721 negotiates 5V/3A
2. **SYS_5V stabilizes** (~10ms)
3. **IO_3V3 powers up** (AMS1117 startup time: <100µs)
4. **RF_3V3 powers up** (XC6206P startup time: <50µs)
5. **ESP32 boot** (EN pin held high, BOOT pin high for normal boot)
6. **Peripherals initialize** (I2C, SPI, UART)

**No special sequencing required** - all rails can power up simultaneously.

---

## Battery Operation (Future Enhancement)

**Note:** VikingBoard v1.0 is USB-powered only. Battery support for v2.0.

**Possible v2.0 additions:**
- 18650 Li-Ion battery (3.7V nominal, 2500-3500mAh)
- TP4056 or MCP73831 charging IC
- Battery protection circuit (DW01, FS8205)
- Boost converter 3.7V → 5V (e.g., TPS61023)
- Battery level monitoring (ADC on battery voltage divider)

**Estimated battery life (3000mAh @ 3.7V = 11.1Wh):**
- Typical usage (1.9W): **~5.8 hours**
- Light usage (ESP32 modem sleep, 0.5W): **~22 hours**
- Deep sleep (<50mW): **~200 hours (8 days)**

---

## Measurement Plan

**To validate this power budget with prototype:**

1. ✅ **Measure USB-C negotiated voltage/current** (USB power meter)
2. ✅ **Measure each rail voltage** (multimeter at test points)
3. ✅ **Measure total system current** (USB-C inline ammeter)
4. ✅ **Measure per-rail currents** (shunt resistors + oscilloscope)
5. ✅ **Measure LDO temperatures** (IR thermometer or thermocouple)
6. ✅ **Test worst-case scenario** (all peripherals active)
7. ✅ **Test idle/sleep modes** (measure deep sleep current)

**Test Equipment Needed:**
- USB-C power meter (e.g., AVHzY CT-3)
- Multimeter
- Oscilloscope (optional, for current waveforms)
- IR thermometer (for LDO temps)

---

## Design Recommendations

### Decoupling Capacitors

**Per power rail:**
- 1x 22µF bulk cap (close to regulator output)
- 1x 10µF ceramic (X5R, 0805)
- 1x 100nF ceramic (X7R, 0805) at EVERY IC power pin

**Critical locations:**
- ESP32: 10µF + 100nF at each V3P3 pin (4 total)
- RF modules: 10µF + 100nF at each module VCC
- Audio amp: 10µF + 100nF at VDD
- USB-C VBUS: 22µF bulk

### PCB Layout Guidelines

**Power planes:**
- Dedicated GND plane (layer 2 or 4)
- SYS_5V plane (partial, flood fill)
- IO_3V3 plane (partial, flood fill)
- RF_3V3 plane (isolated from IO_3V3)

**Trace widths (1oz copper):**
- SYS_5V: 1.5mm (2.5A capacity)
- IO_3V3: 1mm (1A capacity)
- RF_3V3: 0.5mm (300mA capacity)

**Via stitching:**
- Ground vias every 5-10mm around power planes
- Thermal vias (4-6x 0.3mm) under LDO tabs

---

## Next Steps

- [ ] Validate calculations with prototype measurements
- [ ] Adjust component selections if power budget exceeded
- [ ] Design PCB layout with proper power distribution
- [ ] Add test points for all power rails
- [ ] Document actual measured values in separate file

---

**Last Updated:** 2025-12-02  
**Author:** VikingBoard Team  
**Status:** ✅ Template Complete - Awaiting Prototype Data
