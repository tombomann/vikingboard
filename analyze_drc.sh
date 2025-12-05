#!/bin/bash
echo "DRC VIOLATION ANALYSE"
echo "====================="
echo ""
echo "Total violations: $(grep -c '\[' production/drc.txt)"
echo ""
echo "Top violation types:"
grep '\[.*\]:' production/drc.txt | cut -d'[' -f2 | cut -d']' -f1 | sort | uniq -c | sort -rn
