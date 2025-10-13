#!/bin/bash

echo "🧹 Cleanup Output Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Will delete:"
echo ""

if [ -d "output" ]; then
    find output -type f -name "*.txt" -o -name "*.log" | while read file; do
        size=$(du -h "$file" | cut -f1)
        echo "  - $file ($size)"
    done
fi

echo ""
read -p "Continue? (y/N): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Cleaning..."

find output -type f \( -name "*.txt" -o -name "*.log" \) -delete

find output -type d -empty -delete

echo ""
echo "✅ Done!"
echo ""
echo "Output directory:"
ls -lh output/ 2>/dev/null || echo "  (empty)"
