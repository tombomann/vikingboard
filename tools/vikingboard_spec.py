#!/usr/bin/env python3
"""
vikingboard_spec.py - Prototype spec for VikingBoard.

Denne versjonen er tilpasset footprints med pads 1-8 (PinHeader_1x08).
Brukes for å teste automasjonen. Byttes ut med fullverdig spec når
riktige symboler/footprints er på plass.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Pin:
    ref: str
    pad: str
    net: str


def get_all_pins() -> List[Pin]:
    """Returnerer alle pinner (tilpasset PinHeader_1x08 footprints)."""
    pins: List[Pin] = []

    # J1 (hovedheader, pads 1-8)
    pins.append(Pin("J1", "1", "+5V_SYS"))
    pins.append(Pin("J1", "2", "+3V3_IO"))
    pins.append(Pin("J1", "3", "GND"))
    pins.append(Pin("J1", "4", "GPS_RX"))
    pins.append(Pin("J1", "5", "I2C_SCL"))
    pins.append(Pin("J1", "6", "I2C_SDA"))
    pins.append(Pin("J1", "7", "SPI_SCK"))
    pins.append(Pin("J1", "8", "SPI_MOSI"))

    # J2 (ekstra header, pads 1-8)
    pins.append(Pin("J2", "1", "SPI_MISO"))
    pins.append(Pin("J2", "2", "GPS_TX"))
    pins.append(Pin("J2", "3", "FZ_GPIO1"))
    pins.append(Pin("J2", "4", "FZ_GPIO2"))
    pins.append(Pin("J2", "5", "FZ_GPIO3"))
    pins.append(Pin("J2", "6", "FZ_GPIO4"))
    pins.append(Pin("J2", "7", "FZ_GPIO5"))
    pins.append(Pin("J2", "8", "EN"))

    # U1 (ESP/WT32, pads 1-5 prototype mapping)
    pins.append(Pin("U1", "1", "+5V_SYS"))
    pins.append(Pin("U1", "2", "GND"))
    pins.append(Pin("U1", "3", "EN"))
    pins.append(Pin("U1", "4", "SPI_SCK"))
    pins.append(Pin("U1", "5", "SPI_MOSI"))

    # U2 (MCP23017, pads 1-8)
    pins.append(Pin("U2", "1", "NRF24_IRQ"))
    pins.append(Pin("U2", "2", "KBD_RST"))
    pins.append(Pin("U2", "3", "KBD_INT"))
    pins.append(Pin("U2", "4", "FZ_GPIO1"))
    pins.append(Pin("U2", "5", "FZ_GPIO2"))
    pins.append(Pin("U2", "6", "FZ_GPIO3"))
    pins.append(Pin("U2", "7", "FZ_GPIO4"))
    pins.append(Pin("U2", "8", "FZ_GPIO5"))

    # U3 (LoRa E22, pads 1-8)
    pins.append(Pin("U3", "1", "+3V3_RF"))
    pins.append(Pin("U3", "2", "GND"))
    pins.append(Pin("U3", "3", "EN"))
    pins.append(Pin("U3", "4", "LORA_BUSY"))
    pins.append(Pin("U3", "5", "LORA_DIO1"))
    pins.append(Pin("U3", "6", "LORA_CS"))
    pins.append(Pin("U3", "7", "SPI_SCK"))
    pins.append(Pin("U3", "8", "SPI_MOSI"))

    # U4 (CC1101, pads 1-8)
    pins.append(Pin("U4", "1", "+3V3_RF"))
    pins.append(Pin("U4", "2", "GND"))
    pins.append(Pin("U4", "3", "CC1101_CS"))
    pins.append(Pin("U4", "4", "SPI_SCK"))
    pins.append(Pin("U4", "5", "SPI_MOSI"))
    pins.append(Pin("U4", "6", "SPI_MISO"))
    pins.append(Pin("U4", "7", "CC1101_GDO0"))
    pins.append(Pin("U4", "8", "GND"))

    # U5 (NRF24L01+, pads 1-8)
    pins.append(Pin("U5", "1", "+3V3_RF"))
    pins.append(Pin("U5", "2", "GND"))
    pins.append(Pin("U5", "3", "SPI_SCK"))
    pins.append(Pin("U5", "4", "SPI_MOSI"))
    pins.append(Pin("U5", "5", "SPI_MISO"))
    pins.append(Pin("U5", "6", "NRF24_CS"))
    pins.append(Pin("U5", "7", "NRF24_CE"))
    pins.append(Pin("U5", "8", "NRF24_IRQ"))

    # U6 (TCA8418, pads 1-8)
    pins.append(Pin("U6", "1", "KBD_INT"))
    pins.append(Pin("U6", "2", "I2C_SCL"))
    pins.append(Pin("U6", "3", "I2C_SDA"))
    pins.append(Pin("U6", "4", "KBD_RST"))
    pins.append(Pin("U6", "5", "GND"))
    pins.append(Pin("U6", "6", "+3V3_KBD"))
    pins.append(Pin("U6", "7", "GND"))
    pins.append(Pin("U6", "8", "GND"))

    # U7 (GPS, pads 1-8)
    pins.append(Pin("U7", "1", "+3V3_IO"))
    pins.append(Pin("U7", "2", "GND"))
    pins.append(Pin("U7", "3", "GPS_RX"))
    pins.append(Pin("U7", "4", "GPS_TX"))
    pins.append(Pin("U7", "5", "GPS_PPS"))
    pins.append(Pin("U7", "6", "GND"))
    pins.append(Pin("U7", "7", "GND"))
    pins.append(Pin("U7", "8", "GND"))

    return pins
