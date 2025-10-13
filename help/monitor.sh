#!/bin/bash

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

LOG_FILE="${1:-output/conversion.log}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  ${GREEN}� XML CONVERTER - SPEED MONITOR${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Monitoring: $LOG_FILE"
echo "Press Ctrl+C to stop"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "%-8s | %-12s | %-12s | %-10s | %s\n" "TIME" "ELEMENTS" "SPEED" "TREND" "STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

last_elements=0
last_time=0
last_speed=0
start_time=$(date +%s)
speed_history=()
history_size=3
first_measurement=true

while true; do
    sleep 10
    
    if [ ! -f "$LOG_FILE" ]; then
        echo "Waiting for log file..."
        continue
    fi
    
    current_elements=$(grep -oP '\.{3} \K[0-9,]+(?= elements)' "$LOG_FILE" | tail -1 | tr -d ',')
    
    if [ -z "$current_elements" ]; then
        continue
    fi
    
    current_time=$(date +%s)
    if [ "$first_measurement" = true ]; then
        last_elements=$current_elements
        last_time=$current_time
        first_measurement=false
        continue
    fi
    
    time_diff=$((current_time - last_time))
    
    if [ $time_diff -gt 0 ] && [ $current_elements -gt $last_elements ]; then
        elem_diff=$((current_elements - last_elements))
        instant_speed=$((elem_diff / time_diff))
        
        speed_history+=($instant_speed)
        if [ ${#speed_history[@]} -gt $history_size ]; then
            speed_history=("${speed_history[@]:1}")
        fi
        
        speed=0
        for s in "${speed_history[@]}"; do
            speed=$((speed + s))
        done
        speed=$((speed / ${#speed_history[@]}))
        
        elapsed=$((current_time - start_time))
        hours=$((elapsed / 3600))
        mins=$(((elapsed % 3600) / 60))
        secs=$((elapsed % 60))
        time_str=$(printf "%02d:%02d:%02d" $hours $mins $secs)
        
        elements_formatted=$(printf "%'d" $current_elements)
        
        if [ $last_speed -eq 0 ]; then
            trend="━━━"
            trend_color=$NC
        elif [ $speed -gt $last_speed ]; then
            trend_diff=$((speed - last_speed))
            trend=$(printf "+%d" $trend_diff)
            trend_color=$GREEN
        elif [ $speed -lt $last_speed ]; then
            trend_diff=$((last_speed - speed))
            trend=$(printf -- "-%d" $trend_diff)
            trend_color=$RED
        else
            trend="═══"
            trend_color=$NC
        fi
        
        if [ $speed -gt 2500 ]; then
            status="🚀 EXCELLENT"
            status_color=$GREEN
        elif [ $speed -gt 1000 ]; then
            status="✅ GOOD"
            status_color=$GREEN
        elif [ $speed -gt 500 ]; then
            status="⚠️  OK"
            status_color=$YELLOW
        elif [ $speed -gt 200 ]; then
            status="⚠️  SLOW"
            status_color=$YELLOW
        elif [ $speed -gt 100 ]; then
            status="🚨 VERY SLOW"
            status_color=$RED
        else
            status="🔥 CRITICAL!"
            status_color=$RED
        fi
        
        smooth_indicator=""
        if [ ${#speed_history[@]} -ge $history_size ]; then
            smooth_indicator=" (avg)"
        fi
        printf "%-8s | %12s | ${CYAN}%8d e/s${NC} | ${trend_color}%10s${NC} | ${status_color}%s${NC}%s\n" \
            "$time_str" "$elements_formatted" "$speed" "$trend" "$status" "$smooth_indicator"
        
        if [ $last_speed -gt 0 ] && [ $speed -lt 500 ] && [ $last_speed -gt 1000 ]; then
            echo ""
            echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${RED}⚠️  WARNING: Speed dropped from ${last_speed} to ${speed} elem/s!${NC}"
            echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo ""
        fi
        
        last_elements=$current_elements
        last_time=$current_time
        last_speed=$speed
    fi
done
