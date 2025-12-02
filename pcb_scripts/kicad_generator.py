#!/usr/bin/env python3
"""
kicad_generator.py - Generate KiCad symbols and footprints from VikingBoard spec

Generates:
- vikingboard_connector.kicad_sym (98-pin edge connector symbol)
- vikingboard.kicad_mod (footprints for the board)
- component_symbols.kicad_sym (all component symbols)

Usage:
    python3 kicad_generator.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Import the spec
sys.path.append(str(Path(__file__).parent))
from vikingboard_spec import VikingBoardSpec, PinType


class KiCadGenerator:
    """Generate KiCad library files from VikingBoard specification"""
    
    def __init__(self, spec):
        self.spec = spec
        self.output_dir = Path(__file__).parent.parent / "kicad" / "libraries"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all(self):
        """Generate all KiCad files"""
        print(f"\n{'='*60}")
        print(f"  KiCad Library Generator for {self.spec.BOARD_NAME}")
        print(f"{'='*60}\n")
        
        self.generate_connector_symbol()
        self.generate_connector_footprint()
        self.generate_component_symbols()
        
        print(f"\n{'='*60}")
        print(f"✅ KiCad library generation complete!")
        print(f"{'='*60}\n")
        print(f"Generated files in: {self.output_dir}\n")
        print(f"Next steps:")
        print(f"  1. Open KiCad project: kicad/Vikingboard.kicad_pro")
        print(f"  2. Add library path: Preferences > Manage Symbol Libraries")
        print(f"  3. Add: {self.output_dir}")
        print(f"  4. Use symbols in schematic\n")
    
    def generate_connector_symbol(self):
        """Generate 98-pin connector symbol for schematic"""
        filename = self.output_dir / "vikingboard_connector.kicad_sym"
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Header
            f.write("(kicad_symbol_lib (version 20231120) (generator kicad_generator.py)\n")
            f.write(f"  (symbol \"VIKINGBOARD_98PIN\" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n")
            f.write(f"    (property \"Reference\" \"J\" (at 0 130 0)\n")
            f.write(f"      (effects (font (size 1.27 1.27)))\n")
            f.write(f"    )\n")
            f.write(f"    (property \"Value\" \"VIKINGBOARD_98PIN\" (at 0 -130 0)\n")
            f.write(f"      (effects (font (size 1.27 1.27)))\n")
            f.write(f"    )\n")
            f.write(f"    (property \"Footprint\" \"vikingboard:EDGE_CONNECTOR_98PIN\" (at 0 0 0)\n")
            f.write(f"      (effects (font (size 1.27 1.27)) hide)\n")
            f.write(f"    )\n")
            f.write(f"    (property \"Datasheet\" \"~\" (at 0 0 0)\n")
            f.write(f"      (effects (font (size 1.27 1.27)) hide)\n")
            f.write(f"    )\n")
            
            # Symbol body - draw a rectangle
            f.write(f"    (symbol \"VIKINGBOARD_98PIN_0_1\"\n")
            f.write(f"      (rectangle (start -12.7 127) (end 12.7 -127)\n")
            f.write(f"        (stroke (width 0.254) (type default))\n")
            f.write(f"        (fill (type background))\n")
            f.write(f"      )\n")
            f.write(f"    )\n")
            
            # Pins - split into left and right sides
            f.write(f"    (symbol \"VIKINGBOARD_98PIN_1_1\"\n")
            
            left_pins = self.spec.pins[:49]  # Pins 1-49 on left
            right_pins = self.spec.pins[49:]  # Pins 50-98 on right
            
            # Left side pins
            y_pos = 124
            for pin in left_pins:
                pin_type = self._get_kicad_pin_type(pin.pin_type)
                f.write(f"      (pin {pin_type} line (at -15.24 {y_pos:.2f} 0) (length 2.54)\n")
                f.write(f"        (name \"{pin.net_name}\" (effects (font (size 1.016 1.016))))\n")
                f.write(f"        (number \"{pin.number}\" (effects (font (size 1.016 1.016))))\n")
                f.write(f"      )\n")
                y_pos -= 2.54
            
            # Right side pins
            y_pos = 124
            for pin in right_pins:
                pin_type = self._get_kicad_pin_type(pin.pin_type)
                f.write(f"      (pin {pin_type} line (at 15.24 {y_pos:.2f} 180) (length 2.54)\n")
                f.write(f"        (name \"{pin.net_name}\" (effects (font (size 1.016 1.016))))\n")
                f.write(f"        (number \"{pin.number}\" (effects (font (size 1.016 1.016))))\n")
                f.write(f"      )\n")
                y_pos -= 2.54
            
            f.write(f"    )\n")  # Close symbol
            f.write(f"  )\n")  # Close VIKINGBOARD_98PIN
            f.write(f")\n")  # Close kicad_symbol_lib
        
        print(f"✅ Generated connector symbol: {filename}")
        print(f"   - 98 pins defined")
        print(f"   - Split into left (1-49) and right (50-98) sides\n")
    
    def generate_connector_footprint(self):
        """Generate 98-pin edge connector footprint"""
        filename = self.output_dir / "vikingboard_edge_connector.kicad_mod"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("(footprint \"EDGE_CONNECTOR_98PIN\" (version 20231120) (generator kicad_generator.py)\n")
            f.write(f"  (layer \"F.Cu\")\n")
            f.write(f"  (descr \"98-pin edge connector, 2.54mm pitch\")\n")
            f.write(f"  (tags \"edge connector vikingboard\")\n")
            
            # Generate pads
            # 98 pins, 2.54mm (100mil) pitch
            # Pads on edge of board
            x_pos = 0
            for i, pin in enumerate(self.spec.pins, start=1):
                f.write(f"  (pad \"{i}\" smd rect (at {x_pos:.3f} 0) (size 1.5 5)\n")
                f.write(f"    (layers \"F.Cu\" \"F.Paste\" \"F.Mask\")\n")
                f.write(f"  )\n")
                x_pos += 2.54
            
            # Outline
            f.write(f"  (fp_line (start 0 -3) (end {x_pos:.3f} -3) (stroke (width 0.15) (type solid)) (layer \"F.SilkS\"))\n")
            f.write(f"  (fp_line (start 0 3) (end {x_pos:.3f} 3) (stroke (width 0.15) (type solid)) (layer \"F.SilkS\"))\n")
            
            # Courtyard
            f.write(f"  (fp_rect (start -1 -4) (end {x_pos + 1:.3f} 4) (stroke (width 0.05) (type solid)) (layer \"F.CrtYd\") (fill none))\n")
            
            f.write(f")\n")
        
        print(f"✅ Generated connector footprint: {filename}")
        print(f"   - 98 SMD pads, 2.54mm pitch")
        print(f"   - Total length: {98 * 2.54:.1f}mm\n")
    
    def generate_component_symbols(self):
        """Generate symbols for all components"""
        filename = self.output_dir / "vikingboard_components.kicad_sym"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("(kicad_symbol_lib (version 20231120) (generator kicad_generator.py)\n")
            
            # ESP32-WROOM-32E
            f.write(self._generate_esp32_symbol())
            
            # Power regulators
            f.write(self._generate_ldo_symbol("AMS1117-3.3", "U", "IO_3V3"))
            f.write(self._generate_ldo_symbol("XC6206P332MR", "U", "RF_3V3"))
            
            # USB-C PD controller
            f.write(self._generate_usb_pd_symbol())
            
            # Sensors
            f.write(self._generate_i2c_sensor_symbol("MPU-6050", "IMU"))
            f.write(self._generate_i2c_sensor_symbol("BME280", "ENV"))
            f.write(self._generate_i2c_sensor_symbol("BH1750FVI", "LIGHT"))
            
            # RF modules
            f.write(self._generate_rf_module_symbol("CC1101", "U", "SPI"))
            f.write(self._generate_rf_module_symbol("NRF24L01", "U", "SPI"))
            f.write(self._generate_lora_symbol())
            
            f.write(")\n")  # Close library
        
        print(f"✅ Generated component symbols: {filename}")
        print(f"   - ESP32-WROOM-32E")
        print(f"   - Power regulators (AMS1117, XC6206)")
        print(f"   - Sensors (MPU-6050, BME280, BH1750)")
        print(f"   - RF modules (CC1101, NRF24, LoRa E22)\n")
    
    def _get_kicad_pin_type(self, pin_type: PinType) -> str:
        """Convert PinType to KiCad pin type"""
        mapping = {
            PinType.POWER: "power_in",
            PinType.GROUND: "power_in",
            PinType.GPIO: "bidirectional",
            PinType.SPI: "bidirectional",
            PinType.I2C: "bidirectional",
            PinType.UART: "bidirectional",
            PinType.I2S: "bidirectional",
            PinType.RF: "bidirectional",
            PinType.USB: "bidirectional",
            PinType.ADC: "input",
            PinType.PWM: "output",
            PinType.CONTROL: "input",
            PinType.MODULE_SLOT: "passive",
            PinType.RESERVED: "no_connect",
        }
        return mapping.get(pin_type, "passive")
    
    def _generate_esp32_symbol(self) -> str:
        """Generate ESP32-WROOM-32E symbol (simplified)"""
        # Simplified version - full symbol would be very long
        return (
            '  (symbol "ESP32-WROOM-32E" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n'
            '    (property "Reference" "U" (at 0 20 0)\n'
            '      (effects (font (size 1.27 1.27)))\n'
            '    )\n'
            '    (property "Value" "ESP32-WROOM-32E" (at 0 -20 0)\n'
            '      (effects (font (size 1.27 1.27)))\n'
            '    )\n'
            '    (property "Footprint" "RF_Module:ESP32-WROOM-32E" (at 0 0 0)\n'
            '      (effects (font (size 1.27 1.27)) hide)\n'
            '    )\n'
            '    (symbol "ESP32-WROOM-32E_0_1"\n'
            '      (rectangle (start -15.24 17.78) (end 15.24 -17.78)\n'
            '        (stroke (width 0.254) (type default))\n'
            '        (fill (type background))\n'
            '      )\n'
            '    )\n'
            '    (symbol "ESP32-WROOM-32E_1_1"\n'
            '      (pin power_in line (at 0 -20.32 90) (length 2.54)\n'
            '        (name "GND" (effects (font (size 1.016 1.016))))\n'
            '        (number "1" (effects (font (size 1.016 1.016))))\n'
            '      )\n'
            '      (pin power_in line (at 0 20.32 270) (length 2.54)\n'
            '        (name "3V3" (effects (font (size 1.016 1.016))))\n'
            '        (number "2" (effects (font (size 1.016 1.016))))\n'
            '      )\n'
            '      (pin input line (at -17.78 0 0) (length 2.54)\n'
            '        (name "EN" (effects (font (size 1.016 1.016))))\n'
            '        (number "3" (effects (font (size 1.016 1.016))))\n'
            '      )\n'
            '      (pin bidirectional line (at 17.78 15.24 180) (length 2.54)\n'
            '        (name "GPIO0" (effects (font (size 0.762 0.762))))\n'
            '        (number "25" (effects (font (size 0.762 0.762))))\n'
            '      )\n'
            '      (pin bidirectional line (at 17.78 12.7 180) (length 2.54)\n'
            '        (name "GPIO1" (effects (font (size 0.762 0.762))))\n'
            '        (number "35" (effects (font (size 0.762 0.762))))\n'
            '      )\n'
            '      (pin bidirectional line (at 17.78 10.16 180) (length 2.54)\n'
            '        (name "GPIO2" (effects (font (size 0.762 0.762))))\n'
            '        (number "24" (effects (font (size 0.762 0.762))))\n'
            '      )\n'
            '    )\n'
            '  )\n'
        )
    
    def _generate_ldo_symbol(self, part: str, ref: str, net: str) -> str:
        """Generate LDO regulator symbol"""
        return (
            f'  (symbol "{part}" (pin_names (offset 0.254)) (in_bom yes) (on_board yes)\n'
            f'    (property "Reference" "{ref}" (at 0 7.62 0)\n'
            f'      (effects (font (size 1.27 1.27)))\n'
            f'    )\n'
            f'    (property "Value" "{part}" (at 0 -7.62 0)\n'
            f'      (effects (font (size 1.27 1.27)))\n'
            f'    )\n'
            f'    (symbol "{part}_0_1"\n'
            f'      (rectangle (start -7.62 5.08) (end 7.62 -5.08)\n'
            f'        (stroke (width 0.254) (type default))\n'
            f'        (fill (type background))\n'
            f'      )\n'
            f'    )\n'
            f'    (symbol "{part}_1_1"\n'
            f'      (pin power_in line (at -10.16 2.54 0) (length 2.54)\n'
            f'        (name "VIN" (effects (font (size 1.016 1.016))))\n'
            f'        (number "1" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'      (pin power_in line (at 0 -7.62 90) (length 2.54)\n'
            f'        (name "GND" (effects (font (size 1.016 1.016))))\n'
            f'        (number "2" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'      (pin power_out line (at 10.16 2.54 180) (length 2.54)\n'
            f'        (name "VOUT" (effects (font (size 1.016 1.016))))\n'
            f'        (number "3" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'    )\n'
            f'  )\n'
        )
    
    def _generate_usb_pd_symbol(self) -> str:
        """Generate USB-C PD controller symbol (IP2721)"""
        return (
            '  (symbol "IP2721" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n'
            '    (property "Reference" "U" (at 0 12.7 0)\n'
            '      (effects (font (size 1.27 1.27)))\n'
            '    )\n'
            '    (property "Value" "IP2721" (at 0 -12.7 0)\n'
            '      (effects (font (size 1.27 1.27)))\n'
            '    )\n'
            '    (symbol "IP2721_0_1"\n'
            '      (rectangle (start -10.16 10.16) (end 10.16 -10.16)\n'
            '        (stroke (width 0.254) (type default))\n'
            '        (fill (type background))\n'
            '      )\n'
            '    )\n'
            '    (symbol "IP2721_1_1"\n'
            '      (pin bidirectional line (at -12.7 5.08 0) (length 2.54)\n'
            '        (name "CC1" (effects (font (size 1.016 1.016))))\n'
            '        (number "1" (effects (font (size 1.016 1.016))))\n'
            '      )\n'
            '      (pin bidirectional line (at -12.7 2.54 0) (length 2.54)\n'
            '        (name "CC2" (effects (font (size 1.016 1.016))))\n'
            '        (number "2" (effects (font (size 1.016 1.016))))\n'
            '      )\n'
            '      (pin power_out line (at 12.7 5.08 180) (length 2.54)\n'
            '        (name "VBUS" (effects (font (size 1.016 1.016))))\n'
            '        (number "3" (effects (font (size 1.016 1.016))))\n'
            '      )\n'
            '      (pin power_in line (at 0 -12.7 90) (length 2.54)\n'
            '        (name "GND" (effects (font (size 1.016 1.016))))\n'
            '        (number "4" (effects (font (size 1.016 1.016))))\n'
            '      )\n'
            '    )\n'
            '  )\n'
        )
    
    def _generate_i2c_sensor_symbol(self, part: str, ref: str) -> str:
        """Generate generic I2C sensor symbol"""
        return (
            f'  (symbol "{part}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n'
            f'    (property "Reference" "{ref}" (at 0 10.16 0)\n'
            f'      (effects (font (size 1.27 1.27)))\n'
            f'    )\n'
            f'    (property "Value" "{part}" (at 0 -10.16 0)\n'
            f'      (effects (font (size 1.27 1.27)))\n'
            f'    )\n'
            f'    (symbol "{part}_0_1"\n'
            f'      (rectangle (start -7.62 7.62) (end 7.62 -7.62)\n'
            f'        (stroke (width 0.254) (type default))\n'
            f'        (fill (type background))\n'
            f'      )\n'
            f'    )\n'
            f'    (symbol "{part}_1_1"\n'
            f'      (pin power_in line (at 0 10.16 270) (length 2.54)\n'
            f'        (name "VCC" (effects (font (size 1.016 1.016))))\n'
            f'        (number "1" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'      (pin power_in line (at 0 -10.16 90) (length 2.54)\n'
            f'        (name "GND" (effects (font (size 1.016 1.016))))\n'
            f'        (number "2" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'      (pin bidirectional line (at -10.16 2.54 0) (length 2.54)\n'
            f'        (name "SCL" (effects (font (size 1.016 1.016))))\n'
            f'        (number "3" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'      (pin bidirectional line (at -10.16 0 0) (length 2.54)\n'
            f'        (name "SDA" (effects (font (size 1.016 1.016))))\n'
            f'        (number "4" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'    )\n'
            f'  )\n'
        )
    
    def _generate_rf_module_symbol(self, part: str, ref: str, interface: str) -> str:
        """Generate RF module symbol"""
        return (
            f'  (symbol "{part}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n'
            f'    (property "Reference" "{ref}" (at 0 12.7 0)\n'
            f'      (effects (font (size 1.27 1.27)))\n'
            f'    )\n'
            f'    (property "Value" "{part}" (at 0 -12.7 0)\n'
            f'      (effects (font (size 1.27 1.27)))\n'
            f'    )\n'
            f'    (symbol "{part}_0_1"\n'
            f'      (rectangle (start -10.16 10.16) (end 10.16 -10.16)\n'
            f'        (stroke (width 0.254) (type default))\n'
            f'        (fill (type background))\n'
            f'      )\n'
            f'    )\n'
            f'    (symbol "{part}_1_1"\n'
            f'      (pin power_in line (at 0 12.7 270) (length 2.54)\n'
            f'        (name "VCC" (effects (font (size 1.016 1.016))))\n'
            f'        (number "1" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'      (pin power_in line (at 0 -12.7 90) (length 2.54)\n'
            f'        (name "GND" (effects (font (size 1.016 1.016))))\n'
            f'        (number "2" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'      (pin output line (at 12.7 5.08 180) (length 2.54)\n'
            f'        (name "ANT" (effects (font (size 1.016 1.016))))\n'
            f'        (number "3" (effects (font (size 1.016 1.016))))\n'
            f'      )\n'
            f'    )\n'
            f'  )\n'
        )
    
    def _generate_lora_symbol(self) -> str:
        """Generate LoRa E22 module symbol"""
        return self._generate_rf_module_symbol("E22-900M30S", "U", "UART")


def main():
    """Main execution"""
    generator = KiCadGenerator(VikingBoardSpec)
    generator.generate_all()


if __name__ == "__main__":
    main()
