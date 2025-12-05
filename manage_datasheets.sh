#!/bin/bash

show_status() {
    echo ""
    echo "📊 Nåværende status:"
    echo "===================="
    RF=$(ls docs/datasheets/RF/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
    SENSORS=$(ls docs/datasheets/Sensors/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
    AUDIO=$(ls docs/datasheets/Audio/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
    POWER=$(ls docs/datasheets/Power/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
    CONNECTORS=$(ls docs/datasheets/Connectors/*.pdf 2>/dev/null | grep -v ".gitkeep" | wc -l | xargs)
    
    [ $RF -eq 4 ] && echo "✅ RF: $RF/4 KOMPLETT" || echo "⏳ RF: $RF/4"
    [ $SENSORS -eq 3 ] && echo "✅ Sensors: $SENSORS/3 KOMPLETT" || echo "⏳ Sensors: $SENSORS/3"
    [ $AUDIO -eq 2 ] && echo "✅ Audio: $AUDIO/2 KOMPLETT" || echo "⏳ Audio: $AUDIO/2"
    [ $POWER -eq 5 ] && echo "✅ Power: $POWER/5 KOMPLETT" || echo "⏳ Power: $POWER/5"
    [ $CONNECTORS -eq 3 ] && echo "✅ Connectors: $CONNECTORS/3 KOMPLETT" || echo "⏳ Connectors: $CONNECTORS/3"
    
    TOTAL=$((RF + SENSORS + AUDIO + POWER + CONNECTORS))
    echo ""
    echo "Total: $TOTAL/17 datablader ($(( (TOTAL * 100) / 17 ))%)"
    echo ""
}

while true; do
    clear
    echo "🤖 VikingBoard Datasheet Manager"
    echo "================================"
    show_status
    
    echo "Velg handling:"
    echo "1) Last ned Sensors (3 datablader)"
    echo "2) Last ned Audio (2 datablader)"
    echo "3) Last ned Power (5 datablader)"
    echo "4) Last ned Connectors (3 datablader)"
    echo "5) Organiser nedlastede filer"
    echo "6) Commit og push til GitHub"
    echo "7) Vis Downloads-mappe"
    echo "8) Last ned ALT (10 datablader)"
    echo "0) Avslutt"
    echo ""
    read -p "Ditt valg: " choice
    
    case $choice in
        1)
            echo "📥 Åpner Sensors-datablader..."
            open "https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf"
            sleep 2
            open "https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf"
            sleep 2
            open "https://www.mouser.com/datasheet/2/348/bh1750fvi-e-186247.pdf"
            echo "✅ 3 URLer åpnet i nettleseren"
            read -p "Trykk Enter når nedlasting er ferdig..."
            ;;
        2)
            echo "📥 Åpner Audio-datablader..."
            open "https://www.knowles.com/docs/default-source/model-downloads/sph0645lm4h-b-datasheet-rev-c.pdf"
            sleep 2
            open "https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf"
            echo "✅ 2 URLer åpnet i nettleseren"
            read -p "Trykk Enter når nedlasting er ferdig..."
            ;;
        3)
            echo "📥 Åpner Power-datablader..."
            open "https://datasheet.lcsc.com/lcsc/2108111930_INJOINIC-IP2721_C3701536.pdf"
            sleep 2
            open "https://www.advanced-monolithic.com/pdf/ds1117.pdf"
            sleep 2
            open "https://www.lcsc.com/datasheet/lcsc_datasheet_1810191832_Torex-Semicon-XC6206P332MR_C5446.pdf"
            sleep 2
            open "https://www.ti.com/lit/ds/symlink/tps2051b.pdf"
            sleep 2
            open "https://www.st.com/resource/en/datasheet/usblc6-2.pdf"
            echo "✅ 5 URLer åpnet i nettleseren"
            read -p "Trykk Enter når nedlasting er ferdig..."
            ;;
        4)
            echo "📥 Åpner Connectors-datablader..."
            open "https://gct.co/files/drawings/usb4085.pdf"
            sleep 2
            open "https://www.hirose.com/product/en/download_file/key_name/U.FL-R-SMT-1/category/Catalog/doc_file_id/31662/"
            echo "✅ 2 URLer åpnet i nettleseren"
            read -p "Trykk Enter når nedlasting er ferdig..."
            ;;
        5)
            echo "📁 Organiserer datablader..."
            ./organize_datasheets.sh
            read -p "Trykk Enter for å fortsette..."
            ;;
        6)
            echo "📝 Committer og pusher..."
            ./commit_datasheets.sh
            read -p "Trykk Enter for å fortsette..."
            ;;
        7)
            echo "�� Siste 10 PDF-er i Downloads:"
            ls -lt ~/Downloads/*.pdf 2>/dev/null | head -10
            read -p "Trykk Enter for å fortsette..."
            ;;
        8)
            echo "📥 Åpner ALLE gjenværende datablader..."
            echo "Dette vil åpne 10 faner i nettleseren"
            read -p "Fortsett? (y/n): " confirm
            if [ "$confirm" = "y" ]; then
                ./download_datasheets.sh
                echo "⏳ Vent 2 minutter på at alle nedlastingene fullføres"
                read -p "Trykk Enter når ferdig..."
            fi
            ;;
        0)
            echo "👋 Ha det!"
            exit 0
            ;;
        *)
            echo "❌ Ugyldig valg"
            sleep 2
            ;;
    esac
done
