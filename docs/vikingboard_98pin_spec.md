# VikingBoard 98-Pin Expansion Specification

## Status
🚧 **Work In Progress** - Initial specification draft

## Overview
This document defines the expansion from the current configuration to a full 98-pin version of VikingBoard.

## Current Configuration Analysis

### Existing Pin Count
Based on current netlist (`vikingboard_nets.md`):
- **J1 Connector**: 8 pins
- **J2 Connector**: 8 pins
- **U1**: 5 pins (Power regulator)
- **U2**: 8 pins (GPIO expander)
- **U3**: 8 pins (LoRa module)
- **U4**: 8 pins (CC1101 module)
- **U5**: 8 pins (NRF24 module)
- **U6**: 8 pins (Keyboard controller)
- **U7**: 8 pins (GPS module)

**Total current pins**: ~61 pins

## 98-Pin Expansion Plan

### Additional Pins Required
**Target**: 98 pins total  
**Current**: ~61 pins  
**To add**: ~37 pins

### Proposed Pin Allocation

#### Power Distribution (Additional)
- [ ] +5V_AUX (2 pins)
- [ ] +3V3_AUX (2 pins)
- [ ] GND (4 additional pins for better distribution)

#### Extended GPIO
- [ ] FZ_GPIO6-10 (5 pins)
- [ ] FZ_GPIO11-15 (5 pins)

#### Additional Communication Interfaces
- [ ] UART2_TX/RX (2 pins)
- [ ] UART3_TX/RX (2 pins)
- [ ] I2C2_SCL/SDA (2 pins)
- [ ] SPI2_SCK/MOSI/MISO/CS (4 pins)

#### Analog Inputs
- [ ] ADC_CH0-3 (4 pins)
- [ ] ADC_VREF (1 pin)

#### PWM Outputs
- [ ] PWM_CH0-3 (4 pins)

#### Control Signals
- [ ] RESET (1 pin)
- [ ] BOOT (1 pin)
- [ ] STATUS_LED (1 pin)

#### Reserved/Future Use
- [ ] RESERVED (4 pins)

## Electrical Specifications

### Voltage Levels
- Logic Level: 3.3V (5V tolerant where specified)
- Maximum Current per Pin: 25mA
- Total Current Budget: TBD

### Signal Integrity Requirements
- SPI Max Frequency: 10 MHz
- I2C Max Frequency: 400 kHz
- UART Max Baud Rate: 115200 bps

## Pin Mapping Table

_To be completed when footprints are finalized_

| Pin # | Net Name | Direction | Voltage | Notes |
|-------|----------|-----------|---------|-------|
| TBD | TBD | TBD | TBD | TBD |

## Implementation Phases

### Phase 1: Documentation
- [x] Initial spec document created
- [ ] Complete pin mapping
- [ ] Define electrical constraints
- [ ] Review with stakeholders

### Phase 2: Schematic Updates
- [ ] Add new connectors
- [ ] Route new signals
- [ ] Update power distribution
- [ ] Run ERC

### Phase 3: PCB Layout
- [ ] Place new components
- [ ] Route additional traces
- [ ] Update ground planes
- [ ] Run DRC

### Phase 4: Validation
- [ ] Generate updated netlists
- [ ] Create bill of materials
- [ ] Design review
- [ ] Prototype ordering

## Dependencies

- **Footprints**: Must be finalized before schematic implementation
- **CI/CD**: Automated checks must be in place (Issue #2)
- **Component Selection**: All modules must be sourced and validated

## Notes

- Pin assignments subject to change based on layout constraints
- Some pins may be reassigned for optimal routing
- Power budget analysis required before finalization

## References

- [Current netlist](vikingboard_nets.md)
- [Auto-generated nets](vikingboard_nets_auto.md)
- Issue #1: 98-pin expansion tracking
