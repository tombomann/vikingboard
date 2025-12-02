#!/usr/bin/env python3
"""
VikingBoard connectivity specification.

Single source of truth for:
- Components U1..U8
- Connectors J1, J3
- Ref / Pad / Net mapping
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class NetEntry:
    ref: str
    pad: str
    net: str


VIKINGBOARD_NET_TABLE: List[NetEntry] = [
    # J1 – Flipper header (2x9)
    NetEntry("J1", "1",  "+5V_SYS"),
    NetEntry("J1", "2",  "+3V3_IO"),
    NetEntry("J1", "3",  "GND"),
    NetEntry("J1", "4",  "GPS_RX"),
    NetEntry("J1", "5",  "I2C_SCL"),
    NetEntry("J1", "6",  "I2C_SDA"),
    NetEntry("J1", "7",  "SPI_SCK"),
    NetEntry("J1", "8",  "SPI_MOSI"),
    NetEntry("J1", "9",  "SPI_MISO"),
    NetEntry("J1", "10", "GPS_TX"),
    NetEntry("J1", "11", "FZ_GPIO1"),
    NetEntry("J1", "12", "FZ_GPIO2"),
    NetEntry("J1", "13", "FZ_GPIO3"),
    NetEntry("J1", "14", "FZ_GPIO4"),
    NetEntry("J1", "15", "FZ_GPIO5"),
    NetEntry("J1", "16", "EN"),
    NetEntry("J1", "17", "GND"),
    NetEntry("J1", "18", "+5V_SYS"),

    # J3 – Qwiic connector
    NetEntry("J3", "1", "GND"),
    NetEntry("J3", "2", "+3V3_IO"),
    NetEntry("J3", "3", "I2C_SDA"),
    NetEntry("J3", "4", "I2C_SCL"),

    # U1 – WT32-SC01 Plus baseboard header abstraction
    NetEntry("U1", "10", "SPI_SCK"),
    NetEntry("U1", "11", "SPI_MOSI"),
    NetEntry("U1", "12", "SPI_MISO"),
    NetEntry("U1", "13", "I2C_SCL"),
    NetEntry("U1", "14", "I2C_SDA"),
    NetEntry("U1", "21", "MCP_INT"),
    NetEntry("U1", "5V", "+5V_SYS"),
    NetEntry("U1", "GND", "GND"),
    NetEntry("U1", "EN", "EN"),
    NetEntry("U1", "43", "GPS_RX"),
    NetEntry("U1", "44", "GPS_TX"),

    # U2 – MCP23017
    NetEntry("U2", "10", "GND"),
    NetEntry("U2", "9",  "+3V3_IO"),
    NetEntry("U2", "12", "I2C_SCL"),
    NetEntry("U2", "13", "I2C_SDA"),
    NetEntry("U2", "20", "MCP_INT"),
    NetEntry("U2", "18", "EN"),
    NetEntry("U2", "15", "GND"),
    NetEntry("U2", "16", "GND"),
    NetEntry("U2", "17", "GND"),
    NetEntry("U2", "21", "LORA_CS"),
    NetEntry("U2", "22", "LORA_BUSY"),
    NetEntry("U2", "23", "LORA_DIO1"),
    NetEntry("U2", "24", "GPS_PPS"),
    NetEntry("U2", "25", "CC1101_CS"),
    NetEntry("U2", "26", "CC1101_GDO0"),
    NetEntry("U2", "27", "NRF24_CS"),
    NetEntry("U2", "28", "NRF24_CE"),
    NetEntry("U2", "1",  "NRF24_IRQ"),
    NetEntry("U2", "2",  "KBD_RST"),
    NetEntry("U2", "3",  "KBD_INT"),
    NetEntry("U2", "4",  "FZ_GPIO1"),
    NetEntry("U2", "5",  "FZ_GPIO2"),
    NetEntry("U2", "6",  "FZ_GPIO3"),
    NetEntry("U2", "7",  "FZ_GPIO4"),
    NetEntry("U2", "8",  "FZ_GPIO5"),

    # U3 – LoRa E22 header (1x10)
    NetEntry("U3", "1",  "+3V3_RF"),
    NetEntry("U3", "2",  "GND"),
    NetEntry("U3", "3",  "EN"),
    NetEntry("U3", "4",  "LORA_BUSY"),
    NetEntry("U3", "5",  "LORA_DIO1"),
    NetEntry("U3", "6",  "LORA_CS"),
    NetEntry("U3", "7",  "SPI_SCK"),
    NetEntry("U3", "8",  "SPI_MOSI"),
    NetEntry("U3", "9",  "SPI_MISO"),
    NetEntry("U3", "10", "LORA_ANT"),

    # U4 – CC1101
    NetEntry("U4", "1", "+3V3_RF"),
    NetEntry("U4", "2", "GND"),
    NetEntry("U4", "3", "CC1101_CS"),
    NetEntry("U4", "4", "SPI_SCK"),
    NetEntry("U4", "5", "SPI_MOSI"),
    NetEntry("U4", "6", "SPI_MISO"),
    NetEntry("U4", "7", "CC1101_GDO0"),

    # U5 – NRF24L01+
    NetEntry("U5", "1", "+3V3_RF"),
    NetEntry("U5", "2", "GND"),
    NetEntry("U5", "3", "SPI_SCK"),
    NetEntry("U5", "4", "SPI_MOSI"),
    NetEntry("U5", "5", "SPI_MISO"),
    NetEntry("U5", "6", "NRF24_CS"),
    NetEntry("U5", "7", "NRF24_CE"),
    NetEntry("U5", "8", "NRF24_IRQ"),

    # U6 – TCA8418
    NetEntry("U6", "1",  "KBD_INT"),
    NetEntry("U6", "12", "I2C_SCL"),
    NetEntry("U6", "13", "I2C_SDA"),
    NetEntry("U6", "19", "KBD_RST"),
    NetEntry("U6", "21", "GND"),
    NetEntry("U6", "24", "+3V3_KBD"),

    # U7 – GPS header (1x5)
    NetEntry("U7", "1", "+3V3_IO"),
    NetEntry("U7", "2", "GND"),
    NetEntry("U7", "3", "GPS_RX"),
    NetEntry("U7", "4", "GPS_TX"),
    NetEntry("U7", "5", "GPS_PPS"),

    # U8 – DRV2605L
    NetEntry("U8", "1", "+3V3_IO"),
    NetEntry("U8", "2", "GND"),
    NetEntry("U8", "3", "I2C_SCL"),
    NetEntry("U8", "4", "I2C_SDA"),
]


def iter_net_rows():
    """Helper for tools that want plain dicts."""
    for entry in VIKINGBOARD_NET_TABLE:
        yield {
            "Ref": entry.ref,
            "Pad": entry.pad,
            "Net": entry.net,
        }
