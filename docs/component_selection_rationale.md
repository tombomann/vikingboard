# Component Selection Rationale

**Project:** VikingBoard v1.0  
**Date:** 2025-12-02  
**Status:** Phase 1 - Foundation Complete

---

## Overview

This document explains the reasoning behind component selections for VikingBoard. Each choice balances:

- **Cost** - Target hobbyist/maker market ($100-150 total BOM)
- **Availability** - Components in stock at major distributors
- **Community Support** - Arduino libraries, documentation, examples
- **Performance** - Meets or exceeds Flipper Zero capabilities
- **Manufacturability** - Hand-solderable or commonly available modules

---

## MCU Selection

### Decision: ESP32-WROOM-32E ✅

**Alternatives Considered:**
- ESP32-S3-WROOM-1
- ESP32-C6-WROOM-1
- STM32F4 series
- RP2040

**Why ESP32-WROOM-32E:**

| Factor | Rating | Notes |
|--------|--------|-------|
| **Cost** | ⭐⭐⭐⭐⭐ | $2.50 in single quantities |
| **Availability** | ⭐⭐⭐⭐⭐ | Massive stock at all distributors |
| **Community** | ⭐⭐⭐⭐⭐ | Huge Arduino/ESP-IDF ecosystem |
| **WiFi/BT** | ⭐⭐⭐⭐ | WiFi 4 (802.11n), BT 4.2 integrated |
| **GPIO** | ⭐⭐⭐⭐ | 34 programmable GPIOs |
| **Documentation** | ⭐⭐⭐⭐⭐ | Excellent datasheets, app notes |
| **RF Design** | ⭐⭐⭐⭐⭐ | Reference designs, proven antenna layouts |

**Why NOT ESP32-S3:**
- $3.50+ (40% more expensive)
- Native USB is nice, but USB-UART bridge works fine
- Less mature ecosystem (released 2020 vs 2016 for WROOM-32E)
- VikingBoard v1.0 focuses on proven, reliable choices

**Why NOT ESP32-C6:**
- Very new (2023) - immature software support
- WiFi 6 and Zigbee/Thread not needed for v1.0 use cases
- Higher risk for first production run

**Decision Rationale:**  
ESP32-WROOM-32E is the **gold standard** for maker projects. It has:
- 9+ years of community testing and debugging
- Hundreds of thousands of projects using it
- Known-good RF design patterns
- Cheapest option with integrated WiFi/BT

For VikingBoard v1.0, **reliability > bleeding-edge features**.

---

## Sensor Selection

### IMU: MPU-6050 ✅

**Alternatives Considered:**
- BMI160 (Bosch)
- LSM6DS3 (STMicroelectronics)
- ICM-20948 (9-axis with magnetometer)

**Why MPU-6050:**

| Factor | MPU-6050 | BMI160 | LSM6DS3 |
|--------|----------|--------|----------|
| **Price** | $3 | $5 | $4 |
| **Availability** | Excellent | Good | Good |
| **Arduino Lib** | Adafruit_MPU6050 (mature) | Bosch API (complex) | STM lib (moderate) |
| **Community** | Massive (10+ years) | Growing | Moderate |
| **Range** | ±2g to ±16g, ±250°/s to ±2000°/s | Same | Same |
| **Power** | 3.8mA | 850µA | 900µA |

**Decision Rationale:**  
MPU-6050 is the **de facto standard IMU** for hobbyist projects. While BMI160 has better power consumption, MPU-6050 has:
- 10+ years of proven reliability
- Countless code examples and tutorials
- Simple I2C interface with well-tested libraries
- Lowest cost

For VikingBoard v1.0, ease of use and community support outweighs slight power savings.

---

### Environment: BME280 ✅

**Alternatives Considered:**
- BME688 (Bosch, with air quality sensor)
- BMP280 (pressure only)
- DHT22 (temperature + humidity, analog)

**Why BME280:**

| Factor | BME280 | BME688 | BMP280 | DHT22 |
|--------|--------|--------|--------|-------|
| **Price** | $5 | $12 | $3 | $2 |
| **Sensors** | Temp + Humidity + Pressure | Temp + Humidity + Pressure + Gas | Pressure + Temp | Temp + Humidity |
| **Accuracy** | ±1°C, ±3% RH, ±1 hPa | Same | ±1°C, ±1 hPa | ±2°C, ±5% RH |
| **Interface** | I2C/SPI | I2C/SPI | I2C/SPI | 1-wire (timing sensitive) |
| **Library** | Adafruit_BME280 | Bosch BSEC (complex) | Adafruit_BMP280 | DHT library (flaky) |

**Decision Rationale:**  
BME280 is **best-in-class** for environmental sensing:
- Excellent accuracy for all three measurements
- Robust I2C interface (vs DHT22's timing-sensitive 1-wire)
- Mature, stable Arduino library
- Good value for 3-in-1 sensor

BME688 is tempting for air quality, but:
- 2.4x cost increase
- Complex BSEC library (not beginner-friendly)
- Gas sensor requires calibration period

For v1.0, **BME280 hits the sweet spot** of capability vs complexity.

---

### Light: BH1750FVI ✅

**Alternatives Considered:**
- TSL2561 (Adafruit)
- VEML7700 (Vishay)
- BH1750 (ROHM)

**Why BH1750FVI:**

| Factor | BH1750 | TSL2561 | VEML7700 |
|--------|--------|---------|----------|
| **Price** | $1.50 | $6 | $2.50 |
| **Range** | 1-65535 lux | 0.1-40000 lux | 0-120k lux |
| **Resolution** | 16-bit | 16-bit | 16-bit |
| **Interface** | I2C | I2C | I2C |
| **Library** | BH1750 (simple) | Adafruit_TSL2561 | Adafruit_VEML7700 |

**Decision Rationale:**  
BH1750 is the **simplest and cheapest** ambient light sensor:
- Direct lux output (no calibration needed)
- Very simple I2C commands
- Widely available
- Lowest cost

For basic light sensing (e.g., auto-brightness, daylight detection), BH1750 is perfect.

---

## Audio Components

### Microphone: SPH0645LM4H (I2S MEMS) ✅

**Alternatives Considered:**
- MAX4466 (analog with op-amp)
- INMP441 (I2S MEMS)
- Electret microphone + ADC

**Why SPH0645LM4H:**

| Factor | SPH0645 | INMP441 | MAX4466 | Electret |
|--------|---------|---------|---------|----------|
| **Price** | $4 | $3 | $7 | $1 |
| **Interface** | I2S (digital) | I2S (digital) | Analog | Analog |
| **SNR** | 65 dB | 61 dB | 60 dB | 50 dB |
| **Library** | Adafruit I2S | ESP32 I2S | analogRead() | analogRead() |
| **ADC Needed** | No | No | Yes | Yes |

**Decision Rationale:**  
SPH0645 is **digital I2S microphone**:
- No ADC needed (ESP32 has hardware I2S)
- Better noise immunity than analog
- Simple integration with ESP32 I2S peripheral
- Adafruit has proven breakout design we can reference

INMP441 is slightly cheaper, but SPH0645 has:
- Better SNR (65 vs 61 dB)
- More community examples
- Proven Adafruit reference design

---

### Speaker Amplifier: MAX98357A (I2S, 3W) ✅

**Alternatives Considered:**
- PAM8302 (analog, 2.5W)
- PAM8403 (analog, 3W stereo)
- TPA2016D2 (I2C controlled, 2.8W)

**Why MAX98357A:**

| Factor | MAX98357A | PAM8302 | TPA2016D2 |
|--------|-----------|---------|----------|
| **Price** | $3.50 | $1.50 | $4 |
| **Input** | I2S (digital) | Analog | Analog (I2C control) |
| **Power** | 3W | 2.5W | 2.8W |
| **Filter** | Filter-free (Class D) | Requires LC filter | Requires LC filter |
| **Library** | ESP32 I2S | analogWrite() | TPA2016 lib |

**Decision Rationale:**  
MAX98357A is **I2S digital amplifier**:
- Direct connection to ESP32 I2S output
- No external LC filter needed (filter-free Class D)
- Better audio quality than analog input amps
- Adafruit has reference design

Digital I2S chain (I2S mic → ESP32 → I2S amp) is **cleaner** than:
- Analog mic → ADC → DAC → analog amp (introduces noise)

---

## Power Management

### USB-C PD Controller: IP2721 ✅

**Alternatives Considered:**
- FUSB302 (Fairchild)
- STUSB4500 (STMicroelectronics)
- Resistor divider (5V/1.5A only)

**Why IP2721:**

| Factor | IP2721 | FUSB302 | STUSB4500 |
|--------|--------|---------|----------|
| **Price** | $0.80 | $1.50 | $2 |
| **Config** | Auto (no I2C) | I2C required | I2C or NVM |
| **Negotiation** | 5V/3A | 5V/9V/12V/15V/20V | 5V/9V/15V/20V |
| **Package** | QFN-10 | WQFN-14 | QFN-24 |

**Decision Rationale:**  
IP2721 is **simplest USB-C PD solution**:
- Auto-negotiates 5V/3A without I2C configuration
- Cheapest option
- Small QFN-10 package
- We only need 5V (LDOs step down to 3.3V)

FUSB302 and STUSB4500 can negotiate higher voltages (9V, 12V, 20V), but:
- VikingBoard doesn't need >5V
- Adds complexity (I2C config, higher voltage rails)
- More expensive

**5V/3A = 15W** is sufficient for VikingBoard worst-case power budget (~10W max).

---

### 3.3V IO LDO: AMS1117-3.3 (1A) ✅

**Alternatives Considered:**
- AP2112K-3.3 (600mA)
- MCP1826S-3302E (1A)
- XC6206P332MR (200mA)

**Why AMS1117-3.3:**

| Factor | AMS1117-3.3 | AP2112K | MCP1826S |
|--------|-------------|---------|----------|
| **Price** | $0.40 | $0.40 | $0.60 |
| **Current** | 1A | 600mA | 1A |
| **Dropout** | 1.2V | 250mV | 210mV |
| **Package** | SOT-223 | SOT-23-3 | SOT-223 |
| **Availability** | Excellent | Good | Good |

**Decision Rationale:**  
AMS1117-3.3 is **industry standard 3.3V LDO**:
- 1A capacity handles ESP32 + sensors + peripherals
- Ubiquitous availability (millions in stock)
- SOT-223 is hand-solderable with large thermal pad
- Proven reliability in thousands of designs

AP2112K has lower dropout, but only 600mA:
- Power budget analysis shows 800-1000mA peak on IO rail
- Not enough margin with 600mA LDO

---

### 3.3V RF LDO: XC6206P332MR (300mA, low-noise) ✅

**Alternatives Considered:**
- TPS7A4700 (1A, ultra-low-noise)
- AMS1117-3.3 (reuse same LDO)

**Why XC6206P332MR:**

| Factor | XC6206P | TPS7A4700 | AMS1117 |
|--------|---------|-----------|----------|
| **Price** | $0.20 | $2.50 | $0.40 |
| **Current** | 300mA | 1A | 1A |
| **Noise** | 50µV RMS | 4.17µV RMS | 200µV RMS |
| **Package** | SOT-23-3 | SOT-223 | SOT-223 |

**Decision Rationale:**  
XC6206P is **low-noise LDO for RF modules**:
- Separate 3.3V rail isolates RF noise from digital I/O
- 300mA sufficient for RF modules (LoRa 120mA, CC1101 30mA, NRF24 12mA, GPS 30mA = 192mA max)
- Much lower noise than AMS1117 (50µV vs 200µV)
- Very cheap ($0.20)

TPS7A4700 has ultra-low noise (4µV), but:
- 10x cost increase ($2.50 vs $0.20)
- Overkill for v1.0 (XC6206P noise is already excellent)

---

### USB-A Current Limiter: TPS2051BDBVR (500mA) ✅

**Alternatives Considered:**
- Simple polyfuse
- MIC2025 (500mA switch)

**Why TPS2051B:**

| Factor | TPS2051B | Polyfuse | MIC2025 |
|--------|----------|----------|----------|
| **Price** | $0.60 | $0.10 | $0.80 |
| **Current Limit** | 500mA (precise) | ~500mA (varies) | 500mA |
| **Response** | Fast (<1µs) | Slow (seconds) | Fast |
| **Auto-retry** | Yes | Yes (after cool-down) | Yes |
| **Package** | SOT-23-5 | Radial | SOT-23-5 |

**Decision Rationale:**  
TPS2051B is **precision current limiter**:
- USB 2.0 spec requires 500mA max for bus-powered devices
- Fast overcurrent response protects VikingBoard if user plugs in faulty device
- Auto-retry after fault clears
- SOT-23-5 is tiny and cheap

Polyfuse is cheaper, but:
- Slower response (seconds vs microseconds)
- Less precise current limit
- Can't auto-retry without cooling down

---

## RF Modules

### LoRa: E22-900M30S (EBYTE) ✅

**Alternatives Considered:**
- RFM95W (HopeRF)
- SX1276 bare chip
- LoRa32 integrated module

**Why E22-900M30S:**

| Factor | E22-900M30S | RFM95W | SX1276 chip |
|--------|-------------|--------|-------------|
| **Price** | $7 | $10 | $5 + PCB design |
| **TX Power** | 1W (30dBm) | 100mW (20dBm) | 100mW (20dBm) |
| **Range** | ~10km (line-of-sight) | ~2km | ~2km |
| **Interface** | UART or SPI | SPI | SPI |
| **Antenna** | U.FL connector | U.FL | Requires matching network |
| **Certification** | FCC/CE | FCC/CE | Need to certify |

**Decision Rationale:**  
E22-900M30S is **high-power LoRa module**:
- 1W TX power (10x RFM95W) = 5x range increase
- Pre-certified (FCC/CE) saves $5k+ certification cost
- UART mode simplifies integration (no SPI conflicts)
- EBYTE has good reputation in maker community

---

### CC1101: Generic Module ✅

**Why CC1101 module:**
- Sub-1GHz transceiver (433MHz in Europe/Asia)
- SPI interface
- Cheap ($3 for breakout module)
- Widely used for ISM band experimentation

**Note:** Will test with breakout module first, then design custom footprint for v1.1 if needed.

---

### NRF24L01+: Generic Module ✅

**Why NRF24L01+:**
- 2.4GHz transceiver (complements 433/868MHz modules)
- Very cheap ($2)
- Huge community support
- Good for short-range (<100m) high-speed links

**Note:** Using generic module for v1.0. Known for power issues, so will add proper decoupling and optional LDO.

---

### GPS: u-blox NEO-M8N ✅

**Alternatives Considered:**
- NEO-6M (older generation)
- NEO-M9N (newer, more expensive)
- Quectel L76 (smaller, lower power)

**Why NEO-M8N:**

| Factor | NEO-M8N | NEO-6M | NEO-M9N | Quectel L76 |
|--------|---------|--------|---------|-------------|
| **Price** | $12 | $8 | $20 | $10 |
| **Sensitivity** | -167dBm | -161dBm | -167dBm | -165dBm |
| **Update Rate** | 10Hz | 5Hz | 25Hz | 10Hz |
| **Cold Start** | 26s | 29s | 24s | 32s |
| **Power** | 30mA | 45mA | 32mA | 25mA |

**Decision Rationale:**  
NEO-M8N is **proven GPS module**:
- Excellent sensitivity (-167dBm)
- Mature u-blox software support
- Good balance of performance and cost
- Active antenna support (external U.FL)

NEO-6M is cheaper but older (2012 vs 2014):
- Lower sensitivity (-161 vs -167dBm)
- Slower update rate (5Hz vs 10Hz)

NEO-M9N is better, but:
- 66% more expensive
- Marginal improvement for v1.0 use cases

---

## Peripheral Components

### Haptic Driver: DRV2605L ✅

**Alternatives Considered:**
- Simple transistor + vibration motor
- Haptic motor without driver

**Why DRV2605L:**
- 123 pre-programmed haptic effects (clicks, buzzes, ramps)
- I2C control (simple integration)
- ERM and LRA motor support
- Texas Instruments quality
- Adafruit library exists

**Decision Rationale:**  
DRV2605L enables **advanced haptic feedback**:
- More than just "buzz on/off"
- Flipper Zero uses advanced haptics for UX
- I2C control is elegant (vs PWM + transistor)

---

### ESD Protection: USBLC6-2SC6 ✅

**Why USBLC6-2SC6:**
- Dual-line protection (D+ and D- simultaneously)
- Very low capacitance (3.5pF) - doesn't affect USB 2.0 signaling
- SOT-23-6 package (small, cheap)
- Industry standard for USB protection

---

## Summary

### Cost Breakdown (Estimated, 1-off quantities)

| Category | Components | Estimated Cost |
|----------|------------|----------------|
| **MCU** | ESP32-WROOM-32E | $2.50 |
| **Sensors** | MPU6050, BME280, BH1750 | $9.50 |
| **Audio** | SPH0645, MAX98357 | $7.50 |
| **Haptic** | DRV2605L | $3.00 |
| **RF Modules** | LoRa E22, CC1101, NRF24, GPS | $24.00 |
| **Power** | IP2721, AMS1117, XC6206, TPS2051B, USBLC6 | $2.30 |
| **Passives** | Caps, resistors, LEDs, crystals | $5.00 |
| **Connectors** | USB-C, USB-A, 4x U.FL, microSD, headers | $10.00 |
| **PCB** | 4-layer, 100x80mm (JLCPCB) | $30.00 |
| **Enclosure** | 3D printed or off-the-shelf | $15.00 |
| **Misc** | Speaker, antennas, hardware | $10.00 |
| **TOTAL** | | **~$119** |

### Design Philosophy

VikingBoard v1.0 component selections prioritize:

1. ✅ **Proven reliability** over bleeding-edge features
2. ✅ **Community support** over niche/exotic parts
3. ✅ **Cost-effectiveness** without sacrificing quality
4. ✅ **Availability** at major distributors (DigiKey, Mouser, LCSC)
5. ✅ **Manufacturability** for hobbyist assembly (hand-solderable when possible)

This approach ensures VikingBoard v1.0 has the **highest chance of success** on first production run.

---

## Next Steps

- [ ] Order components (2-3 week lead time from China/USA)
- [ ] Download all datasheets to `docs/datasheets/`
- [ ] Create detailed power budget spreadsheet
- [ ] Design KiCad symbols and footprints
- [ ] Begin schematic entry

---

**Last Updated:** 2025-12-02  
**Author:** VikingBoard Team  
**Status:** ✅ Phase 1 Complete
