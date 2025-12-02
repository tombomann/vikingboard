#!/bin/bash
set -e

PROJECT_DIR="$HOME/vikingboard"
KICAD_DIR="$PROJECT_DIR/kicad"
PROJECT_NAME="Vikingboard"

echo "⚙️ Starter VikingBoard automasjon via KiCad CLI..."

# Opprett mapper
mkdir -p "$KICAD_DIR"

# 1. Opprett prosjekt dersom det ikke finnes
if [ ! -f "$KICAD_DIR/$PROJECT_NAME.kicad_pro" ]; then
    echo "📁 Oppretter nytt KiCad-prosjekt..."
    kicad-cli project create "$KICAD_DIR/$PROJECT_NAME"
else
    echo "📁 KiCad-prosjekt finnes allerede."
fi

# 2. Legg til symbols i schematic
echo "➕ Legger til symbols U1..U8, J1, J3..."
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Connector:Conn_02x18" --ref U1
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Interface_Expansion:MCP23017" --ref U2
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Connector:Conn_01x10" --ref U3
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Connector:Conn_01x07" --ref U4
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Connector:Conn_02x04" --ref U5
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Generic:U_Generic_IC" --ref U6
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Connector:Conn_01x05" --ref U7
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Generic:U_Generic_IC" --ref U8
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Connector:Conn_02x09" --ref J1
kicad-cli sch add-symbol "$KICAD_DIR/$PROJECT_NAME.kicad_sch" --symbol "Connector:Conn_01x04" --ref J3

# 3. Import nett fra vår python-net-generator
echo "🔌 Genererer nett..."
python3 $PROJECT_DIR/pcb_scripts/vikingboard_nets.py

# 4. Import netlist til PCB
echo "📡 Oppdaterer PCB-nett..."
kicad-cli pcb import-netlist "$KICAD_DIR/$PROJECT_NAME.kicad_pcb" \
    --netlist "$PROJECT_DIR/docs/vikingboard_nets.net"

# 5. Eksporter dokumenter
echo "📝 Lager PDF, BOM, Gerber, STEP..."
kicad-cli sch export pdf "$KICAD_DIR/$PROJECT_NAME.kicad_sch" \
    --output "$PROJECT_DIR/docs/Vikingboard_schematic.pdf"

kicad-cli bom export "$KICAD_DIR/$PROJECT_NAME.kicad_sch" \
    --output "$PROJECT_DIR/docs/Vikingboard_bom.csv"

kicad-cli pcb export gerber "$KICAD_DIR/$PROJECT_NAME.kicad_pcb" \
    --output "$PROJECT_DIR/gerber"

kicad-cli pcb export step "$KICAD_DIR/$PROJECT_NAME.kicad_pcb" \
    --output "$PROJECT_DIR/3d/Vikingboard.step"

echo "🎉 Full automasjon ferdig!"

