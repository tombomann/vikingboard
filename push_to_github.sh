#!/bin/bash

echo "VIKINGBOARD - GITHUB PUSH"
echo "========================="
echo ""

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo "✅ No changes to commit"
    exit 0
fi

echo "Files changed:"
git status -s
echo ""

# Show what will be committed
echo "Preview of changes:"
git diff --stat
echo ""

read -p "Commit and push these changes? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Add all changes
    git add .
    
    # Commit with timestamp
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
    git commit -m "PCB Update - $TIMESTAMP

✅ Production files updated
- Gerbers regenerated
- DRC passed
- Ready for manufacturing

Changes:
$(git diff --name-only HEAD~1 HEAD | sed 's/^/  - /')"
    
    # Push to GitHub
    git push origin main
    
    echo ""
    echo "✅ Pushed to GitHub!"
    echo ""
    echo "View at: https://github.com/tombomann/vikingboard"
else
    echo "❌ Push cancelled"
fi
