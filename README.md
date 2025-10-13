🧩 XML to TXT Converter

High-performance XML to TXT converter optimized for large files (100+ GB) with low memory usage.
Designed for efficient preprocessing of XML data for LLM (Large Language Model) pipelines.

🚀 Features

Streaming Parser – Processes files of any size with only ~2–5 MB RAM

Batch Writing – 50-element batches for optimal I/O performance

Optimized GC – Balanced garbage collection (every 50/200/500 elements)

4 MB I/O Buffer – Fast disk operations

Multi-file Output – Automatically splits into 2 GB chunks

File Selection Menu – Easy interface for multiple XML files

Cross-Platform – Works on Linux, macOS, and Windows

⚙️ Quick Start
Linux/macOS
# 1. Place XML file in input folder
cp your_file.xml input/

# 2. Start conversion
./start.sh

# 3. Monitor progress (in another terminal)
./help/monitor.sh

Windows
REM 1. Place XML file in input folder
copy your_file.xml input\

REM 2. Start conversion
start.bat

REM 3. Monitor progress
help\monitor.bat

📁 Project Structure
XMLconverter/
├── start.sh / start.bat      # Start conversion
├── src/
│   └── xml_converter.py      # Main converter script
├── input/                    # Input XML files
├── output/                   # TXT output files
└── help/                     # Helper scripts
    ├── monitor.sh/.bat       # Speed monitoring
    ├── status.sh/.bat        # Status check
    ├── clean.sh/.bat         # Clean output
    └── check_speed.sh/.bat   # Speed calculation

🧠 Usage
Basic Commands

Linux/macOS:

./start.sh              # Start conversion
./help/monitor.sh       # Monitor live
./help/status.sh        # Check status
./help/clean.sh         # Clean output files


Windows:

start.bat               # Start conversion
help\monitor.bat        # Monitor live
help\status.bat         # Check status
help\clean.bat          # Clean output files

Advanced Usage
python3 src/xml_converter.py input/file.xml output/result --chunk-gb 2


Options:

--chunk-gb N – Size per output file (default: 2)

--batch-size N – Elements per batch (default: 100)

--no-parallel – Disable multiprocessing

--no-attributes – Exclude XML attributes

--no-path – Exclude element paths

⚡ Performance

Speed: 4,000–6,000 elements/s

Memory: ~2–5 GB RAM (independent of file size)

Tested on: 105 GB Wikipedia XML dump

🧩 How It Works

Streams XML with ET.iterparse() for minimal memory usage

Batches elements before writing to disk

Triggers garbage collection periodically

Clears processed XML nodes immediately

Splits output files automatically every 2 GB

🩺 Troubleshooting

Conversion slows down over time?

Check RAM usage with htop (Linux/macOS) or Task Manager (Windows)

Monitor progress with ./help/monitor.sh or help\monitor.bat

Restart conversion if necessary

Conversion stopped?

Check log:

Linux/macOS: tail -50 output/conversion.log

Windows: powershell Get-Content output\conversion.log -Tail 50

🧰 Requirements

Python 3.6+

psutil (optional, for memory monitoring)

Install dependencies:

pip install -r requirements.txt

💻 Platform Notes
Linux/macOS

Uses Bash scripts (.sh)

Run with ./script.sh

Use / for file paths

Windows

Uses Batch scripts (.bat)

Run with script.bat or double-click

Use \ for file paths

🤝 Contributing

Contributions are welcome!
Feel free to open issues or submit pull requests for new features or optimizations.

📄 License

MIT License – Free to use, modify, and distribute.
