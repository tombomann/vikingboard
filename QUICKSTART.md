# VikingBoard QuickStart

## Production Files
All files in: production_output/

## Upload to JLCPCB

### Option 1: JLCPCB Bundle (if available)
1. Go to: https://jlcpcb.com
2. Upload: jlcpcb_complete_*.zip
3. Everything auto-configured
4. Order

### Option 2: Manual Upload
1. Go to: https://jlcpcb.com
2. Upload: vikingboard_gerbers_*.zip
3. For SMT Assembly:
   - Click SMT Assembly
   - Upload vikingboard_bom.csv
   - Upload vikingboard_cpl.csv
4. Order

## Cost Estimate
- 5 PCBs: $2-5 USD
- With assembly: $20-50 USD

## Helper Commands
- ./MASTER.sh - Re-export everything
- ./make_jlcpcb.sh - Create JLCPCB bundle only
- ./quick_export.sh - Fast gerber export
- ./open_kicad.sh - Open PCB in KiCad
- ./check_status.sh - Check status

## Fix Unconnected Pads
1. ./open_kicad.sh
2. Tools → Plugin Manager → FreeRouting
3. Tools → FreeRouting → Start
4. Wait 2-5 minutes
5. ./MASTER.sh

Generated: $(date)
