#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  � XML to TXT Converter - OPTIMIZED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Features:"
echo "  ✅ Streaming parser (low memory)"
echo "  ✅ Batch writing (50 elements)"
echo "  ✅ Optimized GC (every 50/200/500 elements)"
echo "  ✅ 4 MB I/O buffer"
echo "  ✅ Multi-file output (2 GB chunks)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

shopt -s nullglob
xml_files=(input/*.xml)
shopt -u nullglob

if [ ${#xml_files[@]} -eq 0 ]; then
    echo "❌ No XML files found in input/ folder"
    echo ""
    echo "Please place your XML files in: input/"
    exit 1
fi

if [ ${#xml_files[@]} -eq 1 ]; then
    INPUT_FILE="${xml_files[0]}"
    echo "📄 Found 1 XML file: $(basename "$INPUT_FILE")"
    echo ""
else
    echo "📁 Found ${#xml_files[@]} XML files:"
    echo ""
    for i in "${!xml_files[@]}"; do
        file="${xml_files[$i]}"
        size=$(du -h "$file" | cut -f1)
        printf "  %2d) %-50s [%s]\n" $((i+1)) "$(basename "$file")" "$size"
    done
    echo ""
    
    while true; do
        read -p "Select file (1-${#xml_files[@]}) or 'q' to quit: " choice
        
        if [ "$choice" = "q" ] || [ "$choice" = "Q" ]; then
            echo "Cancelled."
            exit 0
        fi
        
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#xml_files[@]} ]; then
            INPUT_FILE="${xml_files[$((choice-1))]}"
            break
        else
            echo "❌ Invalid choice. Please enter a number between 1 and ${#xml_files[@]}"
        fi
    done
    echo ""
fi

BASENAME=$(basename "$INPUT_FILE" .xml)
OUTPUT_DIR="output/${BASENAME}_converted"
LOG_FILE="output/conversion.log"

mkdir -p "$OUTPUT_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Input:  $INPUT_FILE"
echo "Output: $OUTPUT_DIR"
echo "Log:    $LOG_FILE"
echo ""
echo "To monitor in another terminal:"
echo "  ./monitor.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Starting conversion..."
echo "(Press Ctrl+C to stop)"
echo ""

python3 src/xml_converter.py \
    "$INPUT_FILE" \
    "$OUTPUT_DIR/wiki" \
    --chunk-gb 2 \
    2>&1 | tee "$LOG_FILE"
