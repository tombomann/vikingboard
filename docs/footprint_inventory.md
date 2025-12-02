# VikingBoard Footprint Migration Inventory

## Status
🔄 **Active Migration** - Tracking footprint replacements

## Overview
This document tracks the migration from placeholder/generic footprints to actual module footprints.

## Footprint Migration Checklist

### Power Management
- [ ] **U1**: Voltage regulator
  - Current: Generic footprint
  - Target: TBD (specify exact part number)
  - Priority: High
  - Branch: `footprint/power-regulator`
  - Status: Not started

### RF Modules
- [ ] **U3**: LoRa Module
  - Current: Generic 8-pin
  - Target: TBD (e.g., RFM95W, SX1276)
  - Priority: High
  - Branch: `footprint/lora-module`
  - Status: Not started

- [ ] **U4**: CC1101 Module
  - Current: Generic 8-pin
  - Target: TI CC1101 module footprint
  - Priority: High
  - Branch: `footprint/cc1101-module`
  - Status: Not started

- [ ] **U5**: NRF24L01 Module
  - Current: Generic 8-pin
  - Target: NRF24L01+ module footprint
  - Priority: High
  - Branch: `footprint/nrf24-module`
  - Status: Not started

### Peripherals
- [ ] **U6**: Keyboard Controller
  - Current: Generic 8-pin
  - Target: TBD (specify I2C keyboard controller IC)
  - Priority: Medium
  - Branch: `footprint/keyboard-controller`
  - Status: Not started

- [ ] **U7**: GPS Module
  - Current: Generic 8-pin
  - Target: TBD (e.g., NEO-6M, NEO-M8N)
  - Priority: Medium
  - Branch: `footprint/gps-module`
  - Status: Not started

### GPIO Expander
- [ ] **U2**: GPIO Expander
  - Current: Generic 8-pin
  - Target: TBD (e.g., MCP23008, PCF8574)
  - Priority: Medium
  - Branch: `footprint/gpio-expander`
  - Status: Not started

### Connectors
- [ ] **J1**: Main Connector (8-pin)
  - Current: Generic header
  - Target: Specific connector type (e.g., JST-XH, Molex)
  - Priority: Low
  - Branch: `footprint/connector-j1`
  - Status: Not started

- [ ] **J2**: Secondary Connector (8-pin)
  - Current: Generic header
  - Target: Specific connector type
  - Priority: Low
  - Branch: `footprint/connector-j2`
  - Status: Not started

## Migration Process

For each footprint replacement:

1. **Research Phase**
   - Identify exact part number
   - Verify footprint availability in KiCad libraries
   - Check component availability and pricing

2. **Preparation**
   - Create feature branch: `footprint/<component-name>`
   - Document part number and supplier info
   - Download/create footprint if needed

3. **Implementation**
   - Update schematic symbol
   - Assign new footprint
   - Update PCB layout
   - Verify connections

4. **Validation**
   - Run ERC locally
   - Run DRC locally
   - Push to GitHub (triggers CI)
   - Review automated checks

5. **Documentation**
   - Update this inventory
   - Update BOM
   - Update netlists
   - Mark as complete

6. **Merge**
   - Create pull request
   - Review changes
   - Merge to main

## Priority Levels

- **High**: Critical for functionality, affects layout significantly
- **Medium**: Important but can be done after high priority items
- **Low**: Nice to have, minimal impact on design

## Dependencies

- CI/CD must be operational before starting migrations (Issue #2)
- Each footprint change requires ERC/DRC validation
- Some footprints may affect 98-pin expansion planning (Issue #1)

## Progress Tracking

- **Total Components**: 9
- **Completed**: 0
- **In Progress**: 0
- **Not Started**: 9
- **Progress**: 0%

## Notes

- One footprint replacement per branch/PR
- Test each change independently
- Keep commits atomic and focused
- Update documentation with each merge

---

_Last updated: 2025-12-02_  
_Related: Issue #3_
