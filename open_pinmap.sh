#!/usr/bin/env bash
set -euo pipefail

FILE="$HOME/vikingboard/docs/esp32_pinmap.md"

if [ ! -f "$FILE" ]; then
  echo "Fant ikke $FILE. Kjør KiCad og 'vikingboard_nets.export_esp32_pinmap_markdown()' først."
  exit 1
fi

# På macOS:
open "$FILE"
