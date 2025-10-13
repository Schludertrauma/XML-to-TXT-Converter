#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📊 XML Converter - Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

PIDS=$(ps aux | grep "xml_converter.py" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "Status: ⚪ Not running"
    echo ""
else
    echo "Status: 🟢 Running"
    echo ""
    for pid in $PIDS; do
        echo "Process ID: $pid"
        mem=$(ps -p $pid -o rss= | awk '{printf "%.1f MB", $1/1024}')
        echo "Memory:     $mem"
        cpu=$(ps -p $pid -o %cpu= | xargs)
        echo "CPU:        $cpu%"
    done
    echo ""
fi

if [ -f "output/conversion.log" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Latest progress:"
    echo ""
    tail -5 output/conversion.log | sed 's/^/  /'
    echo ""
    
    ./help/check_speed.sh 2>/dev/null
else
    echo "No log file found"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Commands:"
echo "  ./start.sh     - Start conversion"
echo "  ./monitor.sh   - Monitor speed"
echo "  ./clean.sh     - Clean output files"
echo ""
