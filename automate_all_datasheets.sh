#!/bin/bash

echo "🤖 VikingBoard Datasheet Automation"
echo "===================================="
echo ""
echo "Velg handling:"
echo "1) Last ned alle datablader (åpner i nettleser)"
echo "2) Organiser nedlastede datablader"
echo "3) Commit og push til GitHub"
echo "4) Gjør alt (last ned, vent, organiser, commit)"
echo ""
read -p "Ditt valg (1-4): " choice

case $choice in
    1)
        echo "📥 Åpner alle datablad-URLer..."
        # [alle open-kommandoene her]
        ;;
    2)
        echo "📁 Organiserer filer..."
        # [alle mv-kommandoene her]
        ;;
    3)
        echo "📝 Committer og pusher..."
        # [git-kommandoene her]
        ;;
    4)
        echo "🚀 Kjører full automatisering..."
        echo "Steg 1/4: Åpner URLer..."
        # [open-kommandoer]
        echo "Steg 2/4: Venter 120 sekunder..."
        sleep 120
        echo "Steg 3/4: Organiserer filer..."
        # [mv-kommandoer]
        echo "Steg 4/4: Committer og pusher..."
        # [git-kommandoer]
        ;;
    *)
        echo "❌ Ugyldig valg"
        exit 1
        ;;
esac
