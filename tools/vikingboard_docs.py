#!/usr/bin/env python3
from collections import OrderedDict

# Minimal kopi av nett-definisjonen vår – ren Python
MODULE_CONFIG = OrderedDict({
    "J1": [
        ("+5V_SYS", "1"), ("+3V3_IO", "2"), ("GND", "3"),
        ("GPS_RX", "4"), ("I2C_SCL", "5"), ("I2C_SDA", "6"),
        ("SPI_SCK", "7"), ("SPI_MOSI", "8"), ("SPI_MISO", "9"),
        ("GPS_TX", "10"),
        ("FZ_GPIO1", "11"), ("FZ_GPIO2", "12"), ("FZ_GPIO3", "13"),
        ("FZ_GPIO4", "14"), ("FZ_GPIO5", "15"), ("EN", "16"),
        ("GND", "17"), ("+5V_SYS", "18"),
    ],
    "J3": [
        ("GND", "1"), ("+3V3_IO", "2"), ("I2C_SDA", "3"), ("I2C_SCL", "4"),
    ],
    "U1": [
        ("SPI_SCK", "10"), ("SPI_MOSI", "11"), ("SPI_MISO", "12"),
        ("I2C_SCL", "13"), ("I2C_SDA", "14"), ("MCP_INT", "21"),
        ("+5V_SYS", "5V"), ("GND", "GND"), ("EN", "EN"),
        ("GPS_RX", "43"), ("GPS_TX", "44"),
    ],
    "U2": [
        ("GND", "10"), ("+3V3_IO", "9"),
        ("I2C_SCL", "12"), ("I2C_SDA", "13"),
        ("MCP_INT", "20"), ("EN", "18"),
        ("GND", "15"), ("GND", "16"), ("GND", "17"),
        ("LORA_CS", "21"), ("LORA_BUSY", "22"), ("LORA_DIO1", "23"),
        ("GPS_PPS", "24"),
        ("CC1101_CS", "25"), ("CC1101_GDO0", "26"),
        ("NRF24_CS", "27"), ("NRF24_CE", "28"),
        ("NRF24_IRQ", "1"),
        ("KBD_RST", "2"), ("KBD_INT", "3"),
        ("FZ_GPIO1", "4"), ("FZ_GPIO2", "5"), ("FZ_GPIO3", "6"),
        ("FZ_GPIO4", "7"), ("FZ_GPIO5", "8"),
    ],
    "U3": [
        ("+3V3_RF", "1"), ("GND", "2"), ("EN", "3"),
        ("LORA_BUSY", "4"), ("LORA_DIO1", "5"), ("LORA_CS", "6"),
        ("SPI_SCK", "7"), ("SPI_MOSI", "8"), ("SPI_MISO", "9"),
        ("LORA_ANT", "10"),
    ],
    "U4": [
        ("+3V3_RF", "1"), ("GND", "2"), ("CC1101_CS", "3"),
        ("SPI_SCK", "4"), ("SPI_MOSI", "5"), ("SPI_MISO", "6"),
        ("CC1101_GDO0", "7"),
    ],
    "U5": [
        ("+3V3_RF", "1"), ("GND", "2"),
        ("SPI_SCK", "3"), ("SPI_MOSI", "4"), ("SPI_MISO", "5"),
        ("NRF24_CS", "6"), ("NRF24_CE", "7"), ("NRF24_IRQ", "8"),
    ],
    "U6": [
        ("KBD_INT", "1"),
        ("I2C_SCL", "12"), ("I2C_SDA", "13"),
        ("KBD_RST", "19"),
        ("GND", "21"), ("+3V3_KBD", "24"),
    ],
    "U7": [
        ("+3V3_IO", "1"), ("GND", "2"),
        ("GPS_RX", "3"), ("GPS_TX", "4"), ("GPS_PPS", "5"),
    ],
    "U8": [
        ("+3V3_IO", "1"), ("GND", "2"),
        ("I2C_SCL", "3"), ("I2C_SDA", "4"),
    ],
})

MD_PATH = "docs/vikingboard_nets.md"
CSV_PATH = "docs/vikingboard_nets.csv"

def main():
    # Markdown
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("# VikingBoard nett-oversikt\n\n")
        f.write("| Ref | Pad | Net |\n")
        f.write("| :-- | :-- | :-- |\n")
        for ref, mappings in MODULE_CONFIG.items():
            for net, pad in mappings:
                f.write(f"| {ref} | {pad} | `{net}` |\n")

    # CSV
    with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write("Ref,Pad,Net\n")
        for ref, mappings in MODULE_CONFIG.items():
            for net, pad in mappings:
                f.write(f"{ref},{pad},{net}\n")

    print(f"✅ Skrev {MD_PATH} og {CSV_PATH}")

if __name__ == "__main__":
    main()
