# VikingBoard 98-Pin Specification

**Version:** 1.0.2
**Date:** 2025-12-02

**Total Pins:** 98

---

## Power Rails

| Rail | Voltage | Max Current | Source | Regulator | Notes |
|------|---------|-------------|--------|-----------|-------|
| USB_VBUS | 5.0V | 3.0A | USB-C PD | IP2721 (USB-C PD controller) | 5V/3A via USB Power Delivery negotiation |
| SYS_5V | 5.0V | 2.5A | USB_VBUS | Polyfuse 3A + ferrite bead | Main 5V rail after protection |
| IO_3V3 | 3.3V | 1.0A | SYS_5V | AMS1117-3.3 (1A LDO, SOT-223) | Digital I/O, sensors, MCU |
| RF_3V3 | 3.3V | 0.3A | SYS_5V | XC6206P332MR (300mA low-noise LDO, SOT-23-3) | RF modules - separate rail for noise isolation |
| USB_A_5V | 5.0V | 0.5A | SYS_5V | TPS2051BDBVR (500mA current-limited switch, SOT-23-5) | USB-A host port output |

---

## RF Modules

| Module | Part Number | Frequency | Antenna | Interface | Notes |
|--------|-------------|-----------|---------|-----------|-------|
| LoRa_E22 | E22-900M30S (EBYTE) | 868/915MHz | U.FL J_ANT1 | UART | 1W TX power, UART or SPI mode |
| CC1101 | TI CC1101 module | 433MHz | U.FL J_ANT2 | SPI | Sub-1GHz transceiver |
| NRF24 | NRF24L01+ | 2.4GHz | U.FL J_ANT3 | SPI | 2.4GHz transceiver |
| GPS | u-blox NEO-M8N | 1575.42MHz (L1 band) | U.FL J_ANT_GPS | UART | GPS receiver with external active antenna |
| ESP32_WiFi_BT | ESP32-WROOM-32E | 2.4GHz | PCB trace antenna | Internal | WiFi/Bluetooth, PCB antenna with keep-out zone |

---

## Component Selections

| Category | Function | Part Number | Manufacturer | Interface | Price | Rationale |
|----------|----------|-------------|--------------|-----------|-------|-----------|
| MCU | Main microcontroller | ESP32-WROOM-32E | Espressif | WiFi/BT | $2.50 | Mature, excellent support, WiFi/BT integrated |
| Sensor | IMU | MPU-6050 | InvenSense | I2C | $3.00 | Gold standard IMU, massive Arduino support |
| Sensor | Environment | BME280 | Bosch | I2C | $5.00 | Best-in-class temp/humidity/pressure sensor |
| Sensor | Light | BH1750FVI | ROHM | I2C | $1.50 | Simple, accurate ambient light sensor |
| Audio | Microphone | SPH0645LM4H | Knowles | I2S | $4.00 | MEMS I2S digital microphone, Adafruit lib exists |
| Audio | Speaker Amp | MAX98357A | Maxim | I2S | $3.50 | 3W I2S amplifier, filter-free, Adafruit ref design |
| Haptic | Vibration driver | DRV2605L | Texas Instruments | I2C | $3.00 | Advanced haptic driver, 123 effects, I2C control |
| Power | USB-C PD | IP2721 | Injoinic | N/A | $0.80 | Auto-negotiates 5V/3A, QFN-10 package |
| Power | 3.3V IO LDO | AMS1117-3.3 | Advanced Monolithic | N/A | $0.40 | 1A LDO, SOT-223, widely available |
| Power | 3.3V RF LDO | XC6206P332MR | Torex | N/A | $0.20 | Low-noise 300mA LDO for RF modules |
| Power | USB-A switch | TPS2051BDBVR | Texas Instruments | N/A | $0.60 | 500mA current limiter, overcurrent protection |
| Protection | USB ESD | USBLC6-2SC6 | STMicroelectronics | N/A | $0.30 | Dual-line ESD protection for USB |

---

## Power

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 1 | `GND` | Ground | GND | 0mA | N/A | Primary ground reference |
| 2 | `GND` | Ground | GND | 0mA | N/A | Primary ground reference |
| 3 | `SYS_5V` | System 5V rail | 5V | 2500mA | N/A | Main 5V from USB-C PD |
| 4 | `SYS_5V` | System 5V rail | 5V | 2500mA | N/A | Main 5V from USB-C PD |
| 5 | `IO_3V3` | IO 3.3V rail | 3.3V | 1000mA | N/A | Digital I/O and sensors |
| 6 | `IO_3V3` | IO 3.3V rail | 3.3V | 1000mA | N/A | Digital I/O and sensors |
| 7 | `RF_3V3` | RF 3.3V rail | 3.3V | 300mA | N/A | RF modules isolated rail |
| 8 | `RF_3V3` | RF 3.3V rail | 3.3V | 300mA | N/A | RF modules isolated rail |
| 9 | `GND` | Ground | GND | 0mA | N/A | Power ground |
| 10 | `GND` | Ground | GND | 0mA | N/A | Power ground |
| 11 | `USB_A_5V` | USB-A Host 5V | 5V | 500mA | N/A | USB-A output power |
| 12 | `GND` | Ground | GND | 0mA | N/A | USB ground |
| 13 | `GND` | Ground | GND | 0mA | N/A | Ground distribution |
| 14 | `GND` | Ground | GND | 0mA | N/A | Ground distribution |
| 22 | `GND` | Ground | GND | 0mA | N/A | USB ground |
| 31 | `GND` | Ground | GND | 0mA | N/A | SPI ground |
| 32 | `GND` | Ground | GND | 0mA | N/A | SPI ground |
| 37 | `GND` | Ground | GND | 0mA | N/A | I2C ground |
| 38 | `GND` | Ground | GND | 0mA | N/A | I2C ground |
| 48 | `GND` | Ground | GND | 0mA | N/A | RF ground |
| 49 | `GND` | Ground | GND | 0mA | N/A | RF ground |
| 50 | `GND` | Ground | GND | 0mA | N/A | RF ground |
| 57 | `GND` | Ground | GND | 0mA | N/A | UART ground |
| 58 | `GND` | Ground | GND | 0mA | N/A | UART ground |
| 65 | `GND` | Ground | GND | 0mA | N/A | Audio ground |
| 66 | `GND` | Ground | GND | 0mA | N/A | Audio ground |
| 81 | `GND` | Ground | GND | 0mA | N/A | GPIO ground |
| 82 | `GND` | Ground | GND | 0mA | N/A | GPIO ground |
| 85 | `MOD1_GND` | Module 1 ground | GND | 0mA | N/A | Module slot 1 ground |
| 90 | `MOD1_GND` | Module 1 ground | GND | 0mA | N/A | Module slot 1 ground |
| 98 | `GND` | Ground | GND | 0mA | N/A | Final ground pin |

## USB

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 15 | `USB_C_DP` | USB-C D+ data | 3.3V | 0mA | N/A | USB 2.0 differential pair + |
| 16 | `USB_C_DN` | USB-C D- data | 3.3V | 0mA | N/A | USB 2.0 differential pair - |
| 17 | `USB_C_CC1` | USB-C CC1 | 3.3V | 0mA | N/A | Configuration channel 1 |
| 18 | `USB_C_CC2` | USB-C CC2 | 3.3V | 0mA | N/A | Configuration channel 2 |
| 19 | `USB_A_DP` | USB-A Host D+ | 3.3V | 0mA | GPIO19 | USB-A host data + (shared GPIO19 with SPI_MISO) |
| 20 | `USB_A_DN` | USB-A Host D- | 3.3V | 0mA | GPIO20 | USB-A host data - |

## SPI Bus

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 23 | `SPI_SCK` | SPI clock | 3.3V | 0mA | GPIO18 | Shared SPI bus (shared GPIO18 with IR_TX) |
| 24 | `SPI_MOSI` | SPI MOSI | 3.3V | 0mA | GPIO23 | Master out slave in (shared GPIO23 with IR_RX) |
| 25 | `SPI_MISO` | SPI MISO | 3.3V | 0mA | GPIO19 | Master in slave out (shared GPIO19 with USB_A_DP) |
| 26 | `SPI_CS_CC1101` | CC1101 chip select | 3.3V | 0mA | GPIO5 | CC1101 CS active low (shared GPIO5 with PWM3) |
| 27 | `SPI_CS_NRF24` | NRF24 chip select | 3.3V | 0mA | GPIO15 | NRF24 CS active low (shared GPIO15 with PWM4) |
| 28 | `SPI_CS_LORA` | LoRa chip select | 3.3V | 0mA | GPIO13 | LoRa E22 CS (shared GPIO13 with HAPTIC_EN) |
| 29 | `SPI_CS_SD` | SD card chip select | 3.3V | 0mA | GPIO14 | SD card CS active low (shared GPIO14 with AMP_ENABLE) |

## I2C Bus

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 33 | `I2C_SCL` | I2C clock | 3.3V | 0mA | GPIO22 | Shared I2C bus, 4.7k pullup (shared GPIO22 with I2S_DATA_IN, MOD1_SCL) |
| 34 | `I2C_SDA` | I2C data | 3.3V | 0mA | GPIO21 | Shared I2C bus, 4.7k pullup (shared GPIO21 with USB_A_EN, MOD1_SDA) |

## RF Control

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 39 | `CC1101_GDO0` | CC1101 GDO0 | 3.3V | 0mA | GPIO32 | CC1101 data/interrupt (shared GPIO32 with FZ_GPIO12) |
| 40 | `CC1101_GDO2` | CC1101 GDO2 | 3.3V | 0mA | GPIO33 | CC1101 status (shared GPIO33 with FZ_GPIO11) |
| 41 | `NRF24_CE` | NRF24 chip enable | 3.3V | 0mA | GPIO4 | NRF24 TX/RX mode (shared GPIO4 with PWM2) |
| 42 | `NRF24_IRQ` | NRF24 interrupt | 3.3V | 0mA | GPIO16 | NRF24 interrupt (shared GPIO16 with UART_GPS/LORA_RX) |
| 43 | `LORA_M0` | LoRa M0 mode | 3.3V | 0mA | GPIO25 | LoRa E22 mode pin (shared GPIO25 with I2S_WS, MOD1_GPIO1) |
| 44 | `LORA_M1` | LoRa M1 mode | 3.3V | 0mA | GPIO26 | LoRa E22 mode pin (shared GPIO26 with I2S_BCK, MOD1_GPIO2) |
| 45 | `LORA_AUX` | LoRa auxiliary | 3.3V | 0mA | GPIO17 | LoRa E22 status (shared GPIO17 with UART_GPS/LORA_TX) |

## UART

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 51 | `UART0_TX` | Debug UART TX | 3.3V | 0mA | GPIO1 | Debug console output |
| 52 | `UART0_RX` | Debug UART RX | 3.3V | 0mA | GPIO3 | Debug console input |
| 53 | `UART_GPS_TX` | GPS UART TX | 3.3V | 0mA | GPIO17 | GPS module TX UART2 (shared GPIO17 with LORA_AUX, LORA_TX) |
| 54 | `UART_GPS_RX` | GPS UART RX | 3.3V | 0mA | GPIO16 | GPS module RX UART2 (shared GPIO16 with LORA_RX, NRF24_IRQ) |
| 55 | `UART_LORA_TX` | LoRa UART TX | 3.3V | 0mA | GPIO17 | LoRa E22 TX (shared UART2, shared GPIO17 with GPS_TX, LORA_AUX) |
| 56 | `UART_LORA_RX` | LoRa UART RX | 3.3V | 0mA | GPIO16 | LoRa E22 RX (shared UART2, shared GPIO16 with GPS_RX, NRF24_IRQ) |

## I2S Audio

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 59 | `I2S_BCK` | I2S bit clock | 3.3V | 0mA | GPIO26 | Audio bit clock (shared GPIO26 with LORA_M1, MOD1_GPIO2) |
| 60 | `I2S_WS` | I2S word select | 3.3V | 0mA | GPIO25 | Audio L/R select (shared GPIO25 with LORA_M0, MOD1_GPIO1) |
| 61 | `I2S_DATA_IN` | I2S mic data | 3.3V | 0mA | GPIO22 | Microphone input (shared GPIO22 with I2C_SCL, MOD1_SCL) |
| 62 | `I2S_DATA_OUT` | I2S speaker data | 3.3V | 0mA | GPIO27 | Speaker amplifier out (shared GPIO27 with SD_CD) |

## GPIO / ADC / PWM

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 30 | `SD_CD` | SD card detect | 3.3V | 0mA | GPIO27 | Card detect active low (shared GPIO27 with I2S_DATA_OUT) |
| 35 | `I2C_INT1` | I2C interrupt 1 | 3.3V | 0mA | GPIO35 | Sensor interrupt IMU (shared GPIO35 with ADC3) |
| 36 | `I2C_INT2` | I2C interrupt 2 | 3.3V | 0mA | GPIO34 | Sensor interrupt (shared GPIO34 with ADC4) |
| 46 | `GPS_PPS` | GPS pulse per second | 3.3V | 0mA | GPIO36 | 1Hz timing pulse (shared GPIO36 with ADC2) |
| 67 | `FZ_GPIO1` | GPIO 1 | 3.3V | 0mA | GPIO2 | General purpose I/O (shared GPIO2 with LED_STATUS, PWM1) |
| 68 | `FZ_GPIO2` | GPIO 2 | 3.3V | 0mA | GPIO0 | General purpose I/O (shared GPIO0 with LED_POWER, BOOT) |
| 69 | `FZ_GPIO3` | GPIO 3 / ADC1 | 3.3V | 0mA | GPIO39 | ADC capable (input only) |
| 70 | `FZ_GPIO4` | GPIO 4 / ADC2 | 3.3V | 0mA | GPIO36 | ADC capable input only (shared GPIO36 with GPS_PPS) |
| 71 | `FZ_GPIO5` | GPIO 5 / ADC3 | 3.3V | 0mA | GPIO35 | ADC capable input only (shared GPIO35 with I2C_INT1) |
| 72 | `FZ_GPIO6` | GPIO 6 / ADC4 | 3.3V | 0mA | GPIO34 | ADC capable input only (shared GPIO34 with I2C_INT2) |
| 73 | `FZ_GPIO7` | GPIO 7 / PWM1 | 3.3V | 0mA | GPIO2 | PWM capable boot strapping (shared GPIO2 with FZ_GPIO1, LED_STATUS) |
| 74 | `FZ_GPIO8` | GPIO 8 / PWM2 | 3.3V | 0mA | GPIO4 | PWM capable (shared GPIO4 with NRF24_CE) |
| 75 | `FZ_GPIO9` | GPIO 9 / PWM3 | 3.3V | 0mA | GPIO5 | PWM capable boot strapping (shared GPIO5 with SPI_CS_CC1101) |
| 76 | `FZ_GPIO10` | GPIO 10 / PWM4 | 3.3V | 0mA | GPIO15 | PWM capable boot strapping (shared GPIO15 with SPI_CS_NRF24) |
| 77 | `FZ_GPIO11` | GPIO 11 | 3.3V | 0mA | GPIO33 | General purpose I/O (shared GPIO33 with CC1101_GDO2) |
| 78 | `FZ_GPIO12` | GPIO 12 | 3.3V | 0mA | GPIO32 | General purpose I/O (shared GPIO32 with CC1101_GDO0) |
| 79 | `FZ_GPIO13` | GPIO 13 / IR_TX | 3.3V | 0mA | GPIO18 | IR transmitter 940nm LED (shared GPIO18 with SPI_SCK) |
| 80 | `FZ_GPIO14` | GPIO 14 / IR_RX | 3.3V | 0mA | GPIO23 | IR receiver 38kHz demod (shared GPIO23 with SPI_MOSI) |
| 91 | `LED_STATUS` | Status LED | 3.3V | 0mA | GPIO2 | User status LED (shared GPIO2 with FZ_GPIO1, PWM1) |
| 92 | `LED_POWER` | Power LED | 3.3V | 0mA | GPIO0 | Power indicator LED (shared GPIO0 with FZ_GPIO2, BOOT) |

## Module Slots

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 83 | `MOD1_5V` | Module 1 power 5V | 5V | 0mA | N/A | Module slot 1 power |
| 84 | `MOD1_3V3` | Module 1 power 3.3V | 3.3V | 0mA | N/A | Module slot 1 logic |
| 86 | `MOD1_SCL` | Module 1 I2C clock | 3.3V | 0mA | GPIO22 | I2C bus access (shared GPIO22 with I2C_SCL, I2S_DATA_IN) |
| 87 | `MOD1_SDA` | Module 1 I2C data | 3.3V | 0mA | GPIO21 | I2C bus access (shared GPIO21 with I2C_SDA, USB_A_EN) |
| 88 | `MOD1_GPIO1` | Module 1 GPIO 1 | 3.3V | 0mA | GPIO25 | Module control/data (shared GPIO25 with I2S_WS, LORA_M0) |
| 89 | `MOD1_GPIO2` | Module 1 GPIO 2 | 3.3V | 0mA | GPIO26 | Module control/data (shared GPIO26 with I2S_BCK, LORA_M1) |

## Control & Status

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 21 | `USB_A_EN` | USB-A enable | 3.3V | 0mA | GPIO21 | Enable USB-A power (shared GPIO21 with I2C_SDA) |
| 47 | `GPS_RESET` | GPS reset | 3.3V | 0mA | GPIO12 | GPS module reset |
| 63 | `AMP_ENABLE` | Amplifier enable | 3.3V | 0mA | GPIO14 | Speaker amp enable (shared GPIO14 with SPI_CS_SD) |
| 64 | `HAPTIC_EN` | Haptic enable | 3.3V | 0mA | GPIO13 | Vibration motor enable (shared GPIO13 with SPI_CS_LORA) |
| 93 | `BOOT` | Boot mode | 3.3V | 0mA | GPIO0 | ESP32 boot mode pull low (shared GPIO0 with FZ_GPIO2, LED_POWER) |
| 94 | `RESET` | System reset | 3.3V | 0mA | EN | ESP32 reset (active low) |

## Reserved

| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |
|-----|-----|----------|---------|-------------|------------|-------|
| 95 | `RESERVED1` | Reserved 1 | 3.3V | 0mA | N/A | Future expansion |
| 96 | `RESERVED2` | Reserved 2 | 3.3V | 0mA | N/A | Future expansion |
| 97 | `RESERVED3` | Reserved 3 | 3.3V | 0mA | N/A | Future expansion |

