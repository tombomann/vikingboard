#!/usr/bin/env python3
"""
vikingboard_spec.py - Single Source of Truth for VikingBoard 98-pin specification

This module defines the complete hardware specification for VikingBoard,
including pin assignments, power rails, RF modules, and component selections.

Usage:
    python3 vikingboard_spec.py
    
Outputs:
    - docs/vikingboard_nets.csv (KiCad netlist import)
    - docs/vikingboard_98pin_pinout.md (human-readable documentation)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import csv
from pathlib import Path


class PinType(Enum):
    """Pin functional types"""
    POWER = "power"
    GROUND = "ground"
    GPIO = "gpio"
    SPI = "spi"
    I2C = "i2c"
    UART = "uart"
    I2S = "i2s"
    RF = "rf"
    USB = "usb"
    ADC = "adc"
    PWM = "pwm"
    SDIO = "sdio"
    MODULE_SLOT = "module_slot"
    CONTROL = "control"
    RESERVED = "reserved"


@dataclass
class Pin:
    """Pin specification"""
    number: int
    net_name: str
    function: str
    pin_type: PinType
    voltage: str  # "3.3V", "5V", "GND"
    max_current_ma: int  # For power/ground pins only
    notes: str = ""
    esp32_gpio: Optional[str] = None  # ESP32 GPIO mapping if applicable


@dataclass
class PowerRail:
    """Power rail specification"""
    name: str
    voltage: float
    max_current_a: float
    source: str
    regulator_ic: str = ""
    notes: str = ""


@dataclass
class RFModule:
    """RF module specification"""
    name: str
    ic_part_number: str
    frequency: str
    antenna_connector: str
    interface: str  # "SPI", "UART", "I2C", "Internal"
    cs_pin: str = ""
    control_pins: str = ""
    notes: str = ""


@dataclass
class Component:
    """Component selection"""
    category: str
    function: str
    part_number: str
    manufacturer: str
    interface: str
    voltage: str
    typ_current_ma: float
    max_current_ma: float
    price_usd: float
    rationale: str


class VikingBoardSpec:
    """
    VikingBoard 98-pin specification
    
    Complete hardware definition including:
    - Power distribution
    - RF modules
    - Sensors and peripherals
    - GPIO expansion
    - Module slots
    """
    
    VERSION = "1.0.1"
    BOARD_NAME = "VikingBoard"
    TOTAL_PINS = 98
    DATE = "2025-12-02"
    
    # ==================== POWER RAILS ====================
    
    power_rails = [
        PowerRail(
            name="USB_VBUS",
            voltage=5.0,
            max_current_a=3.0,
            source="USB-C PD",
            regulator_ic="IP2721 (USB-C PD controller)",
            notes="5V/3A via USB Power Delivery negotiation"
        ),
        PowerRail(
            name="SYS_5V",
            voltage=5.0,
            max_current_a=2.5,
            source="USB_VBUS",
            regulator_ic="Polyfuse 3A + ferrite bead",
            notes="Main 5V rail after protection"
        ),
        PowerRail(
            name="IO_3V3",
            voltage=3.3,
            max_current_a=1.0,
            source="SYS_5V",
            regulator_ic="AMS1117-3.3 (1A LDO, SOT-223)",
            notes="Digital I/O, sensors, MCU"
        ),
        PowerRail(
            name="RF_3V3",
            voltage=3.3,
            max_current_a=0.3,
            source="SYS_5V",
            regulator_ic="XC6206P332MR (300mA low-noise LDO, SOT-23-3)",
            notes="RF modules - separate rail for noise isolation"
        ),
        PowerRail(
            name="USB_A_5V",
            voltage=5.0,
            max_current_a=0.5,
            source="SYS_5V",
            regulator_ic="TPS2051BDBVR (500mA current-limited switch, SOT-23-5)",
            notes="USB-A host port output"
        ),
    ]
    
    # ==================== RF MODULES ====================
    
    rf_modules = [
        RFModule(
            name="LoRa_E22",
            ic_part_number="E22-900M30S (EBYTE)",
            frequency="868/915MHz",
            antenna_connector="U.FL J_ANT1",
            interface="UART",
            control_pins="M0, M1, AUX",
            notes="1W TX power, UART or SPI mode"
        ),
        RFModule(
            name="CC1101",
            ic_part_number="TI CC1101 module",
            frequency="433MHz",
            antenna_connector="U.FL J_ANT2",
            interface="SPI",
            cs_pin="CS_CC1101",
            control_pins="GDO0, GDO2",
            notes="Sub-1GHz transceiver"
        ),
        RFModule(
            name="NRF24",
            ic_part_number="NRF24L01+",
            frequency="2.4GHz",
            antenna_connector="U.FL J_ANT3",
            interface="SPI",
            cs_pin="CS_NRF24",
            control_pins="CE, IRQ",
            notes="2.4GHz transceiver"
        ),
        RFModule(
            name="GPS",
            ic_part_number="u-blox NEO-M8N",
            frequency="1575.42MHz (L1 band)",
            antenna_connector="U.FL J_ANT_GPS",
            interface="UART",
            control_pins="PPS, RESET",
            notes="GPS receiver with external active antenna"
        ),
        RFModule(
            name="ESP32_WiFi_BT",
            ic_part_number="ESP32-WROOM-32E",
            frequency="2.4GHz",
            antenna_connector="PCB trace antenna",
            interface="Internal",
            notes="WiFi/Bluetooth, PCB antenna with keep-out zone"
        ),
    ]
    
    # ==================== COMPONENT SELECTIONS ====================
    
    components = [
        Component("MCU", "Main microcontroller", "ESP32-WROOM-32E", "Espressif",
                  "WiFi/BT", "3.3V", 80, 240, 2.50,
                  "Mature, excellent support, WiFi/BT integrated"),
        Component("Sensor", "IMU", "MPU-6050", "InvenSense",
                  "I2C", "3.3V", 3.8, 3.8, 3.00,
                  "Gold standard IMU, massive Arduino support"),
        Component("Sensor", "Environment", "BME280", "Bosch",
                  "I2C", "3.3V", 0.3, 0.7, 5.00,
                  "Best-in-class temp/humidity/pressure sensor"),
        Component("Sensor", "Light", "BH1750FVI", "ROHM",
                  "I2C", "3.3V", 0.12, 0.12, 1.50,
                  "Simple, accurate ambient light sensor"),
        Component("Audio", "Microphone", "SPH0645LM4H", "Knowles",
                  "I2S", "3.3V", 1.5, 1.5, 4.00,
                  "MEMS I2S digital microphone, Adafruit lib exists"),
        Component("Audio", "Speaker Amp", "MAX98357A", "Maxim",
                  "I2S", "5V", 10, 800, 3.50,
                  "3W I2S amplifier, filter-free, Adafruit ref design"),
        Component("Haptic", "Vibration driver", "DRV2605L", "Texas Instruments",
                  "I2C", "3.3V", 5, 100, 3.00,
                  "Advanced haptic driver, 123 effects, I2C control"),
        Component("Power", "USB-C PD", "IP2721", "Injoinic",
                  "N/A", "5V", 0, 0, 0.80,
                  "Auto-negotiates 5V/3A, QFN-10 package"),
        Component("Power", "3.3V IO LDO", "AMS1117-3.3", "Advanced Monolithic",
                  "N/A", "3.3V", 0, 1000, 0.40,
                  "1A LDO, SOT-223, widely available"),
        Component("Power", "3.3V RF LDO", "XC6206P332MR", "Torex",
                  "N/A", "3.3V", 0, 300, 0.20,
                  "Low-noise 300mA LDO for RF modules"),
        Component("Power", "USB-A switch", "TPS2051BDBVR", "Texas Instruments",
                  "N/A", "5V", 0, 500, 0.60,
                  "500mA current limiter, overcurrent protection"),
        Component("Protection", "USB ESD", "USBLC6-2SC6", "STMicroelectronics",
                  "N/A", "N/A", 0, 0, 0.30,
                  "Dual-line ESD protection for USB"),
    ]
    
    # ==================== PIN MAPPING (98 pins) ====================
    # GPIO assignments carefully planned to avoid conflicts
    # ESP32 has 34 usable GPIOs (GPIO0-GPIO39)
    # Input-only: GPIO34-39 (ADC1)
    # Strapping pins: GPIO0, GPIO2, GPIO5, GPIO12, GPIO15 (use with caution)
    
    pins = [
        # ========== POWER SECTION (Pins 1-14) ==========
        Pin(1, "GND", "Ground", PinType.GROUND, "GND", 0, "Primary ground reference"),
        Pin(2, "GND", "Ground", PinType.GROUND, "GND", 0, "Primary ground reference"),
        Pin(3, "SYS_5V", "System 5V rail", PinType.POWER, "5V", 2500, "Main 5V from USB-C PD"),
        Pin(4, "SYS_5V", "System 5V rail", PinType.POWER, "5V", 2500, "Main 5V from USB-C PD"),
        Pin(5, "IO_3V3", "IO 3.3V rail", PinType.POWER, "3.3V", 1000, "Digital I/O and sensors"),
        Pin(6, "IO_3V3", "IO 3.3V rail", PinType.POWER, "3.3V", 1000, "Digital I/O and sensors"),
        Pin(7, "RF_3V3", "RF 3.3V rail", PinType.POWER, "3.3V", 300, "RF modules isolated rail"),
        Pin(8, "RF_3V3", "RF 3.3V rail", PinType.POWER, "3.3V", 300, "RF modules isolated rail"),
        Pin(9, "GND", "Ground", PinType.GROUND, "GND", 0, "Power ground"),
        Pin(10, "GND", "Ground", PinType.GROUND, "GND", 0, "Power ground"),
        Pin(11, "USB_A_5V", "USB-A Host 5V", PinType.POWER, "5V", 500, "USB-A output power"),
        Pin(12, "GND", "Ground", PinType.GROUND, "GND", 0, "USB ground"),
        Pin(13, "GND", "Ground", PinType.GROUND, "GND", 0, "Ground distribution"),
        Pin(14, "GND", "Ground", PinType.GROUND, "GND", 0, "Ground distribution"),
        
        # ========== USB SECTION (Pins 15-22) ==========
        Pin(15, "USB_C_DP", "USB-C D+ data", PinType.USB, "3.3V", 0, "USB 2.0 differential pair +"),
        Pin(16, "USB_C_DN", "USB-C D- data", PinType.USB, "3.3V", 0, "USB 2.0 differential pair -"),
        Pin(17, "USB_C_CC1", "USB-C CC1", PinType.USB, "3.3V", 0, "Configuration channel 1"),
        Pin(18, "USB_C_CC2", "USB-C CC2", PinType.USB, "3.3V", 0, "Configuration channel 2"),
        Pin(19, "USB_A_DP", "USB-A Host D+", PinType.USB, "3.3V", 0, "USB-A host data +", "GPIO19"),
        Pin(20, "USB_A_DN", "USB-A Host D-", PinType.USB, "3.3V", 0, "USB-A host data -", "GPIO20"),
        Pin(21, "USB_A_EN", "USB-A enable", PinType.CONTROL, "3.3V", 0, "Enable USB-A power", "GPIO21"),
        Pin(22, "GND", "Ground", PinType.GROUND, "GND", 0, "USB ground"),
        
        # ========== SPI BUS (Pins 23-32) ==========
        Pin(23, "SPI_SCK", "SPI clock", PinType.SPI, "3.3V", 0, "Shared SPI bus", "GPIO18"),
        Pin(24, "SPI_MOSI", "SPI MOSI", PinType.SPI, "3.3V", 0, "Master out slave in", "GPIO23"),
        Pin(25, "SPI_MISO", "SPI MISO", PinType.SPI, "3.3V", 0, "Master in slave out", "GPIO19"),
        Pin(26, "SPI_CS_CC1101", "CC1101 chip select", PinType.SPI, "3.3V", 0, "CC1101 CS active low", "GPIO5"),
        Pin(27, "SPI_CS_NRF24", "NRF24 chip select", PinType.SPI, "3.3V", 0, "NRF24 CS active low", "GPIO15"),
        Pin(28, "SPI_CS_LORA", "LoRa chip select", PinType.SPI, "3.3V", 0, "LoRa E22 CS (if SPI mode)", "GPIO13"),
        Pin(29, "SPI_CS_SD", "SD card chip select", PinType.SPI, "3.3V", 0, "SD card CS active low", "GPIO14"),
        Pin(30, "SD_CD", "SD card detect", PinType.GPIO, "3.3V", 0, "Card detect active low", "GPIO27"),
        Pin(31, "GND", "Ground", PinType.GROUND, "GND", 0, "SPI ground"),
        Pin(32, "GND", "Ground", PinType.GROUND, "GND", 0, "SPI ground"),
        
        # ========== I2C BUS (Pins 33-38) ==========
        Pin(33, "I2C_SCL", "I2C clock", PinType.I2C, "3.3V", 0, "Shared I2C bus, 4.7k pullup", "GPIO22"),
        Pin(34, "I2C_SDA", "I2C data", PinType.I2C, "3.3V", 0, "Shared I2C bus, 4.7k pullup", "GPIO21"),
        Pin(35, "I2C_INT1", "I2C interrupt 1", PinType.GPIO, "3.3V", 0, "Sensor interrupt (IMU)", "GPIO35"),
        Pin(36, "I2C_INT2", "I2C interrupt 2", PinType.GPIO, "3.3V", 0, "Sensor interrupt", "GPIO34"),
        Pin(37, "GND", "Ground", PinType.GROUND, "GND", 0, "I2C ground"),
        Pin(38, "GND", "Ground", PinType.GROUND, "GND", 0, "I2C ground"),
        
        # ========== RF CONTROL PINS (Pins 39-50) ==========
        Pin(39, "CC1101_GDO0", "CC1101 GDO0", PinType.RF, "3.3V", 0, "CC1101 data/interrupt", "GPIO32"),
        Pin(40, "CC1101_GDO2", "CC1101 GDO2", PinType.RF, "3.3V", 0, "CC1101 status", "GPIO33"),
        Pin(41, "NRF24_CE", "NRF24 chip enable", PinType.RF, "3.3V", 0, "NRF24 TX/RX mode", "GPIO4"),
        Pin(42, "NRF24_IRQ", "NRF24 interrupt", PinType.RF, "3.3V", 0, "NRF24 interrupt", "GPIO16"),
        Pin(43, "LORA_M0", "LoRa M0 mode", PinType.RF, "3.3V", 0, "LoRa E22 mode pin", "GPIO25"),
        Pin(44, "LORA_M1", "LoRa M1 mode", PinType.RF, "3.3V", 0, "LoRa E22 mode pin", "GPIO26"),
        Pin(45, "LORA_AUX", "LoRa auxiliary", PinType.RF, "3.3V", 0, "LoRa E22 status", "GPIO17"),
        Pin(46, "GPS_PPS", "GPS pulse per second", PinType.GPIO, "3.3V", 0, "1Hz timing pulse", "GPIO36"),
        Pin(47, "GPS_RESET", "GPS reset", PinType.CONTROL, "3.3V", 0, "GPS module reset", "GPIO12"),
        Pin(48, "GND", "Ground", PinType.GROUND, "GND", 0, "RF ground"),
        Pin(49, "GND", "Ground", PinType.GROUND, "GND", 0, "RF ground"),
        Pin(50, "GND", "Ground", PinType.GROUND, "GND", 0, "RF ground"),
        
        # ========== UART INTERFACES (Pins 51-58) ==========
        # Note: GPS and LoRa share UART2 (mutually exclusive in UART mode)
        Pin(51, "UART0_TX", "Debug UART TX", PinType.UART, "3.3V", 0, "Debug console output", "GPIO1"),
        Pin(52, "UART0_RX", "Debug UART RX", PinType.UART, "3.3V", 0, "Debug console input", "GPIO3"),
        Pin(53, "UART_GPS_TX", "GPS UART TX", PinType.UART, "3.3V", 0, "GPS module TX (UART2)", "GPIO17"),
        Pin(54, "UART_GPS_RX", "GPS UART RX", PinType.UART, "3.3V", 0, "GPS module RX (UART2)", "GPIO16"),
        Pin(55, "UART_LORA_TX", "LoRa UART TX", PinType.UART, "3.3V", 0, "LoRa E22 TX (shared UART2, use SPI for LoRa if GPS active)", "GPIO17"),
        Pin(56, "UART_LORA_RX", "LoRa UART RX", PinType.UART, "3.3V", 0, "LoRa E22 RX (shared UART2, use SPI for LoRa if GPS active)", "GPIO16"),
        Pin(57, "GND", "Ground", PinType.GROUND, "GND", 0, "UART ground"),
        Pin(58, "GND", "Ground", PinType.GROUND, "GND", 0, "UART ground"),
        
        # ========== I2S AUDIO (Pins 59-66) ==========
        Pin(59, "I2S_BCK", "I2S bit clock", PinType.I2S, "3.3V", 0, "Audio bit clock", "GPIO26"),
        Pin(60, "I2S_WS", "I2S word select", PinType.I2S, "3.3V", 0, "Audio L/R select", "GPIO25"),
        Pin(61, "I2S_DATA_IN", "I2S mic data", PinType.I2S, "3.3V", 0, "Microphone input", "GPIO22"),
        Pin(62, "I2S_DATA_OUT", "I2S speaker data", PinType.I2S, "3.3V", 0, "Speaker amplifier out", "GPIO27"),
        Pin(63, "AMP_ENABLE", "Amplifier enable", PinType.CONTROL, "3.3V", 0, "Speaker amp enable", "GPIO14"),
        Pin(64, "HAPTIC_EN", "Haptic enable", PinType.CONTROL, "3.3V", 0, "Vibration motor enable", "GPIO13"),
        Pin(65, "GND", "Ground", PinType.GROUND, "GND", 0, "Audio ground"),
        Pin(66, "GND", "Ground", PinType.GROUND, "GND", 0, "Audio ground"),
        
        # ========== GPIO EXPANSION (Pins 67-82) - Flipper Zero compatible ==========
        # Using remaining free GPIOs
        Pin(67, "FZ_GPIO1", "GPIO 1", PinType.GPIO, "3.3V", 0, "General purpose I/O", "GPIO2"),
        Pin(68, "FZ_GPIO2", "GPIO 2", PinType.GPIO, "3.3V", 0, "General purpose I/O", "GPIO0"),
        Pin(69, "FZ_GPIO3", "GPIO 3 / ADC1", PinType.ADC, "3.3V", 0, "ADC capable (input only)", "GPIO39"),
        Pin(70, "FZ_GPIO4", "GPIO 4 / ADC2", PinType.ADC, "3.3V", 0, "ADC capable (input only)", "GPIO36"),
        Pin(71, "FZ_GPIO5", "GPIO 5 / ADC3", PinType.ADC, "3.3V", 0, "ADC capable (input only)", "GPIO35"),
        Pin(72, "FZ_GPIO6", "GPIO 6 / ADC4", PinType.ADC, "3.3V", 0, "ADC capable (input only)", "GPIO34"),
        Pin(73, "FZ_GPIO7", "GPIO 7 / PWM1", PinType.PWM, "3.3V", 0, "PWM capable (boot strapping)", "GPIO2"),
        Pin(74, "FZ_GPIO8", "GPIO 8 / PWM2", PinType.PWM, "3.3V", 0, "PWM capable", "GPIO4"),
        Pin(75, "FZ_GPIO9", "GPIO 9 / PWM3", PinType.PWM, "3.3V", 0, "PWM capable (boot strapping)", "GPIO5"),
        Pin(76, "FZ_GPIO10", "GPIO 10 / PWM4", PinType.PWM, "3.3V", 0, "PWM capable (boot strapping)", "GPIO15"),
        Pin(77, "FZ_GPIO11", "GPIO 11", PinType.GPIO, "3.3V", 0, "General purpose I/O", "GPIO33"),
        Pin(78, "FZ_GPIO12", "GPIO 12", PinType.GPIO, "3.3V", 0, "General purpose I/O", "GPIO32"),
        Pin(79, "FZ_GPIO13", "GPIO 13 / IR_TX", PinType.GPIO, "3.3V", 0, "IR transmitter (940nm LED)", "GPIO18"),
        Pin(80, "FZ_GPIO14", "GPIO 14 / IR_RX", PinType.GPIO, "3.3V", 0, "IR receiver (38kHz demod)", "GPIO23"),
        Pin(81, "GND", "Ground", PinType.GROUND, "GND", 0, "GPIO ground"),
        Pin(82, "GND", "Ground", PinType.GROUND, "GND", 0, "GPIO ground"),
        
        # ========== MODULE SLOT 1 (Pins 83-90) ==========
        Pin(83, "MOD1_5V", "Module 1 power 5V", PinType.MODULE_SLOT, "5V", 0, "Module slot 1 power"),
        Pin(84, "MOD1_3V3", "Module 1 power 3.3V", PinType.MODULE_SLOT, "3.3V", 0, "Module slot 1 logic"),
        Pin(85, "MOD1_GND", "Module 1 ground", PinType.GROUND, "GND", 0, "Module slot 1 ground"),
        Pin(86, "MOD1_SCL", "Module 1 I2C clock", PinType.MODULE_SLOT, "3.3V", 0, "I2C bus access (shared GPIO22)", "GPIO22"),
        Pin(87, "MOD1_SDA", "Module 1 I2C data", PinType.MODULE_SLOT, "3.3V", 0, "I2C bus access (shared GPIO21)", "GPIO21"),
        Pin(88, "MOD1_GPIO1", "Module 1 GPIO 1", PinType.MODULE_SLOT, "3.3V", 0, "Module control/data (shared GPIO25)", "GPIO25"),
        Pin(89, "MOD1_GPIO2", "Module 1 GPIO 2", PinType.MODULE_SLOT, "3.3V", 0, "Module control/data (shared GPIO26)", "GPIO26"),
        Pin(90, "MOD1_GND", "Module 1 ground", PinType.GROUND, "GND", 0, "Module slot 1 ground"),
        
        # ========== RESERVED & STATUS (Pins 91-98) ==========
        Pin(91, "LED_STATUS", "Status LED", PinType.GPIO, "3.3V", 0, "User status LED (shared GPIO2)", "GPIO2"),
        Pin(92, "LED_POWER", "Power LED", PinType.GPIO, "3.3V", 0, "Power indicator LED (shared GPIO0)", "GPIO0"),
        Pin(93, "BOOT", "Boot mode", PinType.CONTROL, "3.3V", 0, "ESP32 boot mode (pull low, shared GPIO0)", "GPIO0"),
        Pin(94, "RESET", "System reset", PinType.CONTROL, "3.3V", 0, "ESP32 reset (active low)", "EN"),
        Pin(95, "RESERVED1", "Reserved 1", PinType.RESERVED, "3.3V", 0, "Future expansion"),
        Pin(96, "RESERVED2", "Reserved 2", PinType.RESERVED, "3.3V", 0, "Future expansion"),
        Pin(97, "RESERVED3", "Reserved 3", PinType.RESERVED, "3.3V", 0, "Future expansion"),
        Pin(98, "GND", "Ground", PinType.GROUND, "GND", 0, "Final ground pin"),
    ]
    
    # ==================== METHODS ====================
    
    @classmethod
    def get_pins_by_type(cls, pin_type: PinType) -> List[Pin]:
        """Filter pins by type"""
        return [p for p in cls.pins if p.pin_type == pin_type]
    
    @classmethod
    def get_pin_by_net(cls, net_name: str) -> Optional[Pin]:
        """Get pin by net name"""
        for p in cls.pins:
            if p.net_name == net_name:
                return p
        return None
    
    @classmethod
    def get_pin_by_number(cls, pin_num: int) -> Optional[Pin]:
        """Get pin by number"""
        for p in cls.pins:
            if p.number == pin_num:
                return p
        return None
    
    @classmethod
    def export_to_csv(cls, filename: str):
        """Export pin mapping to CSV for KiCad netlist import"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Pin', 'Net', 'Function', 'Type', 'Voltage', 'Max_Current_mA', 'ESP32_GPIO', 'Notes'])
            for pin in sorted(cls.pins, key=lambda p: p.number):
                writer.writerow([
                    pin.number,
                    pin.net_name,
                    pin.function,
                    pin.pin_type.value,
                    pin.voltage,
                    pin.max_current_ma,
                    pin.esp32_gpio or '',
                    pin.notes
                ])
        print(f"✅ Exported CSV: {filename}")
    
    @classmethod
    def export_to_markdown(cls, filename: str):
        """Export to markdown documentation"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {cls.BOARD_NAME} 98-Pin Specification\n\n")
            f.write(f"**Version:** {cls.VERSION}\n")
            f.write(f"**Date:** {cls.DATE}\n\n")
            f.write(f"**Total Pins:** {cls.TOTAL_PINS}\n\n")
            
            f.write("---\n\n")
            
            # Power Rails
            f.write("## Power Rails\n\n")
            f.write("| Rail | Voltage | Max Current | Source | Regulator | Notes |\n")
            f.write("|------|---------|-------------|--------|-----------|-------|\n")
            for rail in cls.power_rails:
                f.write(f"| {rail.name} | {rail.voltage}V | {rail.max_current_a}A | {rail.source} | {rail.regulator_ic} | {rail.notes} |\n")
            
            f.write("\n---\n\n")
            
            # RF Modules
            f.write("## RF Modules\n\n")
            f.write("| Module | Part Number | Frequency | Antenna | Interface | Notes |\n")
            f.write("|--------|-------------|-----------|---------|-----------|-------|\n")
            for rf in cls.rf_modules:
                f.write(f"| {rf.name} | {rf.ic_part_number} | {rf.frequency} | {rf.antenna_connector} | {rf.interface} | {rf.notes} |\n")
            
            f.write("\n---\n\n")
            
            # Component Selections
            f.write("## Component Selections\n\n")
            f.write("| Category | Function | Part Number | Manufacturer | Interface | Price | Rationale |\n")
            f.write("|----------|----------|-------------|--------------|-----------|-------|-----------|\n")
            for comp in cls.components:
                f.write(f"| {comp.category} | {comp.function} | {comp.part_number} | {comp.manufacturer} | {comp.interface} | ${comp.price_usd:.2f} | {comp.rationale} |\n")
            
            f.write("\n---\n\n")
            
            # Pin Mapping by Section
            sections = [
                ("Power", [PinType.POWER, PinType.GROUND]),
                ("USB", [PinType.USB]),
                ("SPI Bus", [PinType.SPI]),
                ("I2C Bus", [PinType.I2C]),
                ("RF Control", [PinType.RF]),
                ("UART", [PinType.UART]),
                ("I2S Audio", [PinType.I2S]),
                ("GPIO / ADC / PWM", [PinType.GPIO, PinType.ADC, PinType.PWM]),
                ("Module Slots", [PinType.MODULE_SLOT]),
                ("Control & Status", [PinType.CONTROL]),
                ("Reserved", [PinType.RESERVED]),
            ]
            
            for section_name, pin_types in sections:
                section_pins = [p for p in cls.pins if p.pin_type in pin_types]
                if section_pins:
                    f.write(f"## {section_name}\n\n")
                    f.write("| Pin | Net | Function | Voltage | Max Current | ESP32 GPIO | Notes |\n")
                    f.write("|-----|-----|----------|---------|-------------|------------|-------|\n")
                    for pin in sorted(section_pins, key=lambda p: p.number):
                        f.write(f"| {pin.number} | `{pin.net_name}` | {pin.function} | {pin.voltage} | {pin.max_current_ma}mA | {pin.esp32_gpio or 'N/A'} | {pin.notes} |\n")
                    f.write("\n")
        
        print(f"✅ Exported Markdown: {filename}")
    
    @classmethod
    def validate(cls) -> List[str]:
        """Validate spec for conflicts and errors"""
        errors = []
        
        # Check pin count
        if len(cls.pins) != cls.TOTAL_PINS:
            errors.append(f"❌ Pin count mismatch: {len(cls.pins)} defined, {cls.TOTAL_PINS} expected")
        
        # Check for duplicate pin numbers
        pin_numbers = [p.number for p in cls.pins]
        if len(pin_numbers) != len(set(pin_numbers)):
            duplicates = [num for num in pin_numbers if pin_numbers.count(num) > 1]
            errors.append(f"❌ Duplicate pin numbers: {set(duplicates)}")
        
        # Check pin number range
        for pin in cls.pins:
            if pin.number < 1 or pin.number > cls.TOTAL_PINS:
                errors.append(f"❌ Pin {pin.number} out of range (1-{cls.TOTAL_PINS})")
        
        # Check power budget for each rail (component-based, not pin-based)
        # IO_3V3 rail budget
        io_3v3_load = sum(comp.max_current_ma for comp in cls.components if comp.voltage == "3.3V" and comp.category != "Power") / 1000.0
        io_rail = next((r for r in cls.power_rails if r.name == "IO_3V3"), None)
        if io_rail and io_3v3_load > io_rail.max_current_a:
            errors.append(f"⚠️  IO_3V3 power budget exceeded: {io_3v3_load:.2f}A > {io_rail.max_current_a}A")
        
        # RF_3V3 rail budget (estimate from datasheets)
        rf_3v3_load = 0.12 + 0.03 + 0.012 + 0.03  # LoRa + CC1101 + NRF24 + GPS (max simultaneous)
        rf_rail = next((r for r in cls.power_rails if r.name == "RF_3V3"), None)
        if rf_rail and rf_3v3_load > rf_rail.max_current_a:
            errors.append(f"⚠️  RF_3V3 power budget exceeded: {rf_3v3_load:.2f}A > {rf_rail.max_current_a}A")
        
        # Check for GPIO conflicts (allow intentional sharing with note)
        esp32_gpios = [p.esp32_gpio for p in cls.pins if p.esp32_gpio and p.esp32_gpio != "EN"]
        gpio_counts = {gpio: esp32_gpios.count(gpio) for gpio in set(esp32_gpios)}
        duplicates = {gpio: count for gpio, count in gpio_counts.items() if count > 1}
        
        # Check if duplicates are intentional (noted as "shared")
        unintentional_dups = []
        for gpio in duplicates:
            pins_with_gpio = [p for p in cls.pins if p.esp32_gpio == gpio]
            if not all("shared" in p.notes.lower() for p in pins_with_gpio):
                unintentional_dups.append(gpio)
        
        if unintentional_dups:
            errors.append(f"⚠️  Unintentional duplicate ESP32 GPIO assignments: {set(unintentional_dups)}")
        
        return errors
    
    @classmethod
    def print_summary(cls):
        """Print specification summary"""
        print(f"\n{'='*60}")
        print(f"  {cls.BOARD_NAME} Specification v{cls.VERSION}")
        print(f"{'='*60}\n")
        
        print(f"📊 Statistics:")
        print(f"  • Total pins: {len(cls.pins)}")
        print(f"  • Power pins: {len(cls.get_pins_by_type(PinType.POWER))}")
        print(f"  • Ground pins: {len(cls.get_pins_by_type(PinType.GROUND))}")
        print(f"  • GPIO pins: {len(cls.get_pins_by_type(PinType.GPIO))}")
        print(f"  • RF modules: {len(cls.rf_modules)}")
        print(f"  • Power rails: {len(cls.power_rails)}")
        print(f"  • Components: {len(cls.components)}\n")
        
        # Power budget summary (component-based)
        print(f"⚡ Power Budget (Component-based):")
        io_3v3_load = sum(comp.max_current_ma for comp in cls.components if comp.voltage == "3.3V" and comp.category != "Power") / 1000.0
        print(f"  • IO_3V3 load: {io_3v3_load:.3f}A (LDO rated 1.0A)")
        rf_3v3_load = 0.12 + 0.03 + 0.012 + 0.03  # LoRa + CC1101 + NRF24 + GPS
        print(f"  • RF_3V3 load: {rf_3v3_load:.3f}A (LDO rated 0.3A)")
        for rail in cls.power_rails:
            print(f"  • {rail.name}: {rail.voltage}V / {rail.max_current_a}A ({rail.voltage * rail.max_current_a}W)")
        print()


# ==================== MAIN ====================

def main():
    """Main execution"""
    # Print summary
    VikingBoardSpec.print_summary()
    
    # Validate
    print("🔍 Validating specification...")
    errors = VikingBoardSpec.validate()
    if errors:
        print("\n⚠️  Validation warnings/errors:\n")
        for err in errors:
            print(f"  {err}")
    else:
        print("  ✅ No validation errors\n")
    
    # Export files
    print("📝 Exporting documentation...\n")
    
    # Ensure docs directory exists
    docs_dir = Path(__file__).parent.parent / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Export CSV
    csv_path = docs_dir / "vikingboard_nets.csv"
    VikingBoardSpec.export_to_csv(str(csv_path))
    
    # Export Markdown
    md_path = docs_dir / "vikingboard_98pin_pinout.md"
    VikingBoardSpec.export_to_markdown(str(md_path))
    
    print(f"\n{'='*60}")
    print(f"✅ VikingBoard specification complete!")
    print(f"{'='*60}\n")
    print(f"Next steps:")
    print(f"  1. Review generated files in docs/")
    print(f"  2. Order components from BOM")
    print(f"  3. Create KiCad symbols and footprints")
    print(f"  4. Start schematic entry\n")


if __name__ == "__main__":
    main()
