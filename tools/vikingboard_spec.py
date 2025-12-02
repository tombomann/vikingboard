#!/usr/bin/env python3
"""
vikingboard_spec.py - Single source of truth for VikingBoard nets.

Denne versjonen er enkel: én Pin per linje, matchet til tabellen du allerede har
(i vikingboard_nets.md / CSV). Juster senere hvis du vil ha mer struktur.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Pin:
    ref: str   # Reference designator, e.g. "J1"
    pad: str   # Pad number/name, e.g. "1" eller "5V"
    net: str   # Net name, e.g. "+3V3_IO"


def get_all_pins() -> List[Pin]:
    """Returnerer alle pinner som en liste av Pin-objekter."""
    pins: List[Pin] = []

    # J1 (hovedheader)
    pins.append(Pin("J1", "1", "+5V_SYS"))
    pins.append(Pin("J1", "2", "+3V3_IO"))
    pins.append(Pin("J1", "3", "GND"))
    pins.append(Pin("J1", "4", "GPS_RX"))
    pins.append(Pin("J1", "5", "I2C_SCL"))
    pins.append(Pin("J1", "6", "I2C_SDA"))
    pins.append(Pin("J1", "7", "SPI_SCK"))
    pins.append(Pin("J1", "8", "SPI_MOSI"))
    pins.append(Pin("J1", "9", "SPI_MISO"))
    pins.append(Pin("J1", "10", "GPS_TX"))
    pins.append(Pin("J1", "11", "FZ_GPIO1"))
    pins.append(Pin("J1", "12", "FZ_GPIO2"))
    pins.append(Pin("J1", "13", "FZ_GPIO3"))
    pins.append(Pin("J1", "14", "FZ_GPIO4"))
    pins.append(Pin("J1", "15", "FZ_GPIO5"))
    pins.append(Pin("J1", "16", "EN"))
    pins.append(Pin("J1", "17", "GND"))
    pins.append(Pin("J1", "18", "+5V_SYS"))

    # J3 (Flipper-header)
    pins.append(Pin("J3", "1", "GND"))
    pins.append(Pin("J3", "2", "+3V3_IO"))
    pins.append(Pin("J3", "3", "I2C_SDA"))
    pins.append(Pin("J3", "4", "I2C_SCL"))

    # U1 (WT32-SC01 / ESP32-S3 modul)
    pins.append(Pin("U1", "10", "SPI_SCK"))
    pins.append(Pin("U1", "11", "SPI_MOSI"))
    pins.append(Pin("U1", "12", "SPI_MISO"))
    pins.append(Pin("U1", "13", "I2C_SCL"))
    pins.append(Pin("U1", "14", "I2C_SDA"))
    pins.append(Pin("U1", "21", "MCP_INT"))
    pins.append(Pin("U1", "43", "GPS_RX"))
    pins.append(Pin("U1", "44", "GPS_TX"))
    pins.append(Pin("U1", "5V", "+5V_SYS"))
    pins.append(Pin("U1", "EN", "EN"))
    pins.append(Pin("U1", "GND", "GND"))

    # U2 (MCP23017 + ekstra funksjoner)
    pins.append(Pin("U2", "1", "NRF24_IRQ"))
    pins.append(Pin("U2", "2", "KBD_RST"))
    pins.append(Pin("U2", "3", "KBD_INT"))
    pins.append(Pin("U2", "4", "FZ_GPIO1"))
    pins.append(Pin("U2", "5", "FZ_GPIO2"))
    pins.append(Pin("U2", "6", "FZ_GPIO3"))
    pins.append(Pin("U2", "7", "FZ_GPIO4"))
    pins.append(Pin("U2", "8", "FZ_GPIO5"))
    pins.append(Pin("U2", "9", "+3V3_IO"))
    pins.append(Pin("U2", "10", "GND"))
    pins.append(Pin("U2", "12", "I2C_SCL"))
    pins.append(Pin("U2", "13", "I2C_SDA"))
    pins.append(Pin("U2", "15", "GND"))
    pins.append(Pin("U2", "16", "GND"))
    pins.append(Pin("U2", "17", "GND"))
    pins.append(Pin("U2", "18", "EN"))
    pins.append(Pin("U2", "20", "MCP_INT"))
    pins.append(Pin("U2", "21", "LORA_CS"))
    pins.append(Pin("U2", "22", "LORA_BUSY"))
    pins.append(Pin("U2", "23", "LORA_DIO1"))
    pins.append(Pin("U2", "24", "GPS_PPS"))
    pins.append(Pin("U2", "25", "CC1101_CS"))
    pins.append(Pin("U2", "26", "CC1101_GDO0"))
    pins.append(Pin("U2", "27", "NRF24_CS"))
    pins.append(Pin("U2", "28", "NRF24_CE"))

    # U3 (LoRa E22)
    pins.append(Pin("U3", "1", "+3V3_RF"))
    pins.append(Pin("U3", "2", "GND"))
    pins.append(Pin("U3", "3", "EN"))
    pins.append(Pin("U3", "4", "LORA_BUSY"))
    pins.append(Pin("U3", "5", "LORA_DIO1"))
    pins.append(Pin("U3", "6", "LORA_CS"))
    pins.append(Pin("U3", "7", "SPI_SCK"))
    pins.append(Pin("U3", "8", "SPI_MOSI"))
    pins.append(Pin("U3", "9", "SPI_MISO"))
    pins.append(Pin("U3", "10", "LORA_ANT"))

    # U4 (CC1101)
    pins.append(Pin("U4", "1", "+3V3_RF"))
    pins.append(Pin("U4", "2", "GND"))
    pins.append(Pin("U4", "3", "CC1101_CS"))
    pins.append(Pin("U4", "4", "SPI_SCK"))
    pins.append(Pin("U4", "5", "SPI_MOSI"))
    pins.append(Pin("U4", "6", "SPI_MISO"))
    pins.append(Pin("U4", "7", "CC1101_GDO0"))

    # U5 (NRF24L01+ modul)
    pins.append(Pin("U5", "1", "+3V3_RF"))
    pins.append(Pin("U5", "2", "GND"))
    pins.append(Pin("U5", "3", "SPI_SCK"))
    pins.append(Pin("U5", "4", "SPI_MOSI"))
    pins.append(Pin("U5", "5", "SPI_MISO"))
    pins.append(Pin("U5", "6", "NRF24_CS"))
    pins.append(Pin("U5", "7", "NRF24_CE"))
    pins.append(Pin("U5", "8", "NRF24_IRQ"))

    # U6 (TCA8418 keypad controller)
    pins.append(Pin("U6", "1", "KBD_INT"))
    pins.append(Pin("U6", "12", "I2C_SCL"))
    pins.append(Pin("U6", "13", "I2C_SDA"))
    pins.append(Pin("U6", "19", "KBD_RST"))
    pins.append(Pin("U6", "21", "GND"))
    pins.append(Pin("U6", "24", "+3V3_KBD"))

    # U7 (GPS)
    pins.append(Pin("U7", "1", "+3V3_IO"))
    pins.append(Pin("U7", "2", "GND"))
    pins.append(Pin("U7", "3", "GPS_RX"))
    pins.append(Pin("U7", "4", "GPS_TX"))
    pins.append(Pin("U7", "5", "GPS_PPS"))

    # U8 (DRV2605L / Qwiic/I2C periferi)
    pins.append(Pin("U8", "1", "+3V3_IO"))
    pins.append(Pin("U8", "2", "GND"))
    pins.append(Pin("U8", "3", "I2C_SCL"))
    pins.append(Pin("U8", "4", "I2C_SDA"))

    return pins
