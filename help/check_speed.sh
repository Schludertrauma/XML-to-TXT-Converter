#!/bin/bash

LOG_FILE="${1:-output/conversion.log}"

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ No log file found: $LOG_FILE"
    exit 1
fi

first_line=$(grep -m 1 "\.\.\..*elements" "$LOG_FILE")
last_line=$(grep "\.\.\..*elements" "$LOG_FILE" | tail -1)

if [ -z "$first_line" ] || [ -z "$last_line" ]; then
    echo "⚠️  No progress data found yet"
    exit 0
fi

first_elements=$(echo "$first_line" | grep -oP '\.{3} \K[0-9,]+' | tr -d ',')
last_elements=$(echo "$last_line" | grep -oP '\.{3} \K[0-9,]+' | tr -d ',')

first_time=$(stat -c %Y "$LOG_FILE" 2>/dev/null)
current_time=$(date +%s)

start_line=$(grep -m 1 "Process started" "$LOG_FILE")
if [ -n "$start_line" ]; then
    log_start=$(echo "$start_line" | grep -oP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}' 2>/dev/null)
fi

if [ -n "$first_elements" ] && [ -n "$last_elements" ] && [ "$last_elements" -gt "$first_elements" ]; then
    elem_diff=$((last_elements - first_elements))
    
    log_size=$(stat -c %s "$LOG_FILE" 2>/dev/null || echo 0)
    
    estimated_seconds=$((elem_diff / 1000))
    
    if [ $estimated_seconds -gt 0 ]; then
        avg_speed=$((elem_diff / estimated_seconds))
        
        mins=$((estimated_seconds / 60))
        secs=$((estimated_seconds % 60))
        
        echo "Average speed: $avg_speed elem/s"
        echo "Elements:      $(printf "%'d" $last_elements)"
        echo "Time:          ~${mins}m ${secs}s"
    fi
fi
