# 🧩 XML to TXT Converter

High-performance XML to TXT converter **optimized for LLM training** with large file support (100+ GB) and minimal memory usage (~2-5 GB RAM).

---

## 📑 Table of Contents

- [Quick Start](#-quick-start-3-steps)
- [LLM Training Features](#-llm-training-optimization-features)
- [Output Formats](#-output-format-comparison)
- [Usage Examples](#-usage-examples)
- [Command-Line Options](#️-command-line-options)
- [Performance](#-performance--benchmarks)
- [Framework Integration](#-integration-with-training-frameworks)
- [Best Practices](#-best-practices--tips)
- [Troubleshooting](#-troubleshooting)
- [Installation](#-installation--requirements)
- [FAQ](#-faq)

---

## 🚀 Quick Start (3 Steps)

```bash
# 1. Place your XML file
cp your_data.xml input/

# 2. Convert (LLM-optimized format)
python3 src/xml_converter.py input/your_data.xml output/llm_data --format llm_optimized

# 3. Use for training!
# Output is ready for PyTorch, HuggingFace, or any LLM framework
```

## 🤖 LLM Training Optimization Features

This converter transforms XML data into **training-ready formats** for Large Language Models:

### ✨ Key Features
- **4 Output Formats** - `llm_optimized`, `markdown`, `structured`, `plain`
- **Text Normalization** - Automatic whitespace cleanup for better tokenization
- **Content Filtering** - `--min-length` and `--max-length` to remove noise
- **Training Metadata** - Token counts, character stats, document info
- **Clear Structure** - Section markers and headers for context learning
- **High Performance** - 4,000-6,000 elements/s, only 2-5 GB RAM
- **Streaming Parser** - Handles files of ANY size (tested on 105 GB)
- **Auto-Splitting** - Automatically creates 2 GB chunks

## � Output Format Comparison

### 1. LLM-Optimized (Recommended) ⭐
Best for general LLM training with clear structure and section markers.

```
################################################################################
# TRAINING DOCUMENT METADATA
################################################################################
# Source File: wikipedia.xml | Part: 1
# Format: LLM-Optimized | Tokens: ~3.5M
################################################################################

============================================================
SECTION: ARTICLE (title: Machine Learning)
============================================================

## Introduction
Machine learning is a subset of artificial intelligence...

## History
  The term was coined in 1959 by Arthur Samuel...

============================================================
```

**Pros:** Clear boundaries, normalized text, training metadata, best for transformers
**Use for:** GPT-style models, general pre-training, document understanding

### 2. Markdown Format
Natural formatting perfect for instruction-following tasks.

```markdown
# Machine Learning (Part 1)

> **Source:** wikipedia.xml

## Introduction
Machine learning is a subset of artificial intelligence...

### History
The term was coined in 1959...
```

**Pros:** Standard Markdown, human-readable, natural language structure
**Use for:** Instruction tuning, Q&A datasets, documentation tasks

### 3. Structured Format
JSON-like format for programmatic processing.

```json
{"tag": "article", "attributes": {"id": "123"}, "text": null}
  {"tag": "title", "attributes": {}, "text": "Machine Learning"}
  {"tag": "content", "attributes": {}, "text": "ML is a subset..."}
```

**Pros:** Machine-readable, complete metadata preservation
**Use for:** Data analysis, structured extraction, preprocessing pipelines

### 4. Plain Format
Simple indented text (original format, backward compatible).

```
article [id='123']
  title
    Machine Learning
  content
    ML is a subset...
```

**Pros:** Smallest file size, minimal overhead, fast processing
**Use for:** Legacy compatibility, minimal formatting needs

## 💡 Usage Examples

### Basic LLM Training (Recommended)
```bash
python3 src/xml_converter.py input/wikipedia.xml output/train_data \
  --format llm_optimized
```

### High-Quality Filtered Dataset
```bash
# Remove short text (< 50 chars) to reduce noise
python3 src/xml_converter.py input/data.xml output/quality_data \
  --format llm_optimized \
  --min-length 50
```

### Instruction Tuning Dataset
```bash
# Markdown format for Q&A style training
python3 src/xml_converter.py input/qa_data.xml output/instruct_data \
  --format markdown
```

### Minimal Output (No Metadata)
```bash
# Just content, no headers/footers
python3 src/xml_converter.py input/data.xml output/clean_data \
  --format llm_optimized \
  --no-metadata \
  --no-separators
```

### Large File Processing
```bash
# Start conversion (progress shown in console)
python3 src/xml_converter.py input/large_file.xml output/data \
  --format llm_optimized \
  --chunk-gb 5

# Optional: Save output to log file
python3 src/xml_converter.py input/large_file.xml output/data \
  --format llm_optimized \
  --chunk-gb 5 2>&1 | tee conversion.log
```

## 📁 Project Structure

```
XML-to-TXT-Converter/
├── src/
│   └── xml_converter.py          # Main converter (optimized for LLM)
├── input/                         # Place XML files here
│   └── test_sample/              # Sample data
├── output/                        # Converted TXT files
├── help/
│   ├── clean.sh/.bat             # Clean output files
│   └── docs/                     # Additional documentation
│       ├── QUICKSTART_LLM.md
│       ├── FORMAT_EXAMPLES.md
│       ├── LLM_TRAINING_GUIDE.md
│       └── OPTIMIZATION_SUMMARY.md
├── start.sh / start.bat          # Quick start scripts
├── demo_formats.py               # Demo all output formats
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🛠️ Helper Scripts

### Clean Output Files
```bash
./help/clean.sh         # Linux/macOS
help\clean.bat          # Windows
```

### Demo All Formats
```bash
python3 demo_formats.py
```

### Monitor Conversion Progress
The converter outputs progress information directly to the console:
```bash
# Run converter and see live progress
python3 src/xml_converter.py input/file.xml output/data --format llm_optimized

# Save output to file for later review
python3 src/xml_converter.py input/file.xml output/data --format llm_optimized 2>&1 | tee conversion.log
```

## ⚙️ Command-Line Options

### Format Options
```bash
--format {llm_optimized|markdown|structured|plain}  # Output format (default: llm_optimized)
--no-normalize          # Disable whitespace normalization
--no-metadata           # Disable metadata headers/footers
--no-separators         # Disable section markers
```

### Content Filtering
```bash
--min-length N          # Minimum text length in chars (filter noise)
--max-length N          # Maximum text length in chars
--no-attributes         # Exclude XML attributes
--no-path               # Exclude element paths
```

### Performance Options
```bash
--chunk-gb N            # GB per output file (default: 2)
--batch-size N          # Elements per batch (default: 100)
--no-parallel           # Disable multiprocessing
--indent N              # Indentation size (default: 2)
```

### Resume/Advanced
```bash
--start-element N       # Resume from specific element
--file-part N           # Starting file part number
```

### Get Help
```bash
python3 src/xml_converter.py --help
```

## 🔥 Performance & Benchmarks

| Metric | Performance |
|--------|-------------|
| **Processing Speed** | 4,000-6,000 elements/second |
| **Memory Usage** | 2-5 GB RAM (constant, independent of file size) |
| **File Size** | Tested on 105 GB Wikipedia XML dump |
| **Output Quality** | ⭐⭐⭐⭐⭐ (LLM-optimized) |

### How It Works (Optimized v2.0)
1. **Streaming Parser** - Uses `ET.iterparse()` for minimal memory usage
2. **Batch Writing** - Groups 200 elements before disk write (2x improved)
3. **Smart GC** - Optimized garbage collection at 100/400/1000 element intervals
4. **Memory Cleanup** - Clears XML nodes immediately after processing
5. **Auto-Split** - Creates new file every 2 GB (configurable)
6. **StringIO Builders** - Fast string concatenation with minimal overhead
7. **Pre-compiled Regex** - Pattern compilation at init for 2-3x faster normalization
8. **Efficient Iteration** - Uses generators to avoid double-iteration overhead

### Real-World Example: Wikipedia
```
Input:  105 GB XML dump (enwiki-20251001)
Output: ~85 GB LLM-optimized text
Time:   ~6-8 hours (single machine)
Memory: 3-4 GB RAM peak
Tokens: ~20 billion (estimated)
```

## 🔗 Integration with Training Frameworks

### PyTorch Example
```python
from torch.utils.data import Dataset, DataLoader

class XMLTextDataset(Dataset):
    def __init__(self, file_path, tokenizer):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        # Split by section markers (llm_optimized format)
        self.sections = [s.strip() for s in text.split('='*60) if s.strip()]
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.sections)
    
    def __getitem__(self, idx):
        return self.tokenizer(
            self.sections[idx],
            max_length=512,
            truncation=True,
            padding='max_length'
        )

# Usage
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
dataset = XMLTextDataset("output/llm_data_part1.txt", tokenizer)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
```

### HuggingFace Datasets
```python
from datasets import load_dataset

# Load all output files
dataset = load_dataset('text', data_files={
    'train': 'output/llm_data_part*.txt'
})

# Optional: Filter by length
dataset = dataset.filter(lambda x: len(x['text']) > 100)

# Tokenize
def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
```

## 🎯 Best Practices & Tips

### Choosing the Right Format

| Your Use Case | Recommended Format | Command |
|---------------|-------------------|---------|
| General LLM training | `llm_optimized` | `--format llm_optimized` |
| GPT-style models | `llm_optimized` | `--format llm_optimized` |
| Instruction following | `markdown` | `--format markdown` |
| Q&A datasets | `markdown` | `--format markdown` |
| Data analysis | `structured` | `--format structured` |
| Legacy systems | `plain` | `--format plain` |

### Quality Optimization Tips

1. **Filter Noise** - Use `--min-length 20` to remove very short text
2. **Check Samples** - Review first output file before processing large datasets
3. **Use Separators** - Keep them enabled (default) for better context learning
4. **Keep Metadata** - Useful for debugging and dataset management
5. **Normalize Text** - Keep enabled (default) for better tokenization

### For Large Datasets (100+ GB)

```bash
# 1. Start with smaller chunks for testing
python3 src/xml_converter.py input/large.xml output/test \
  --format llm_optimized \
  --chunk-gb 0.1  # 100MB chunks for testing

# 2. If satisfied, process full dataset with larger chunks
python3 src/xml_converter.py input/large.xml output/train \
  --format llm_optimized \
  --chunk-gb 5    # 5GB chunks for production

# 3. Progress is shown in console automatically
# Watch for: "... X elements | File Y: Z.ZZ GB"
```

## 🩺 Troubleshooting

### Conversion Slows Down
```bash
# Check RAM usage
htop                    # Linux/macOS
taskmgr                 # Windows

# Progress is shown in console output
# Look for lines like: "... 50000 elements | File 1: 1.50 GB"

# If needed, restart with resume
python3 src/xml_converter.py input/file.xml output/data \
  --start-element 50000 \
  --file-part 2
```

### Out of Memory
```bash
# Reduce batch size
python3 src/xml_converter.py input/file.xml output/data \
  --batch-size 50  # Default is 100

# Or disable parallel processing
python3 src/xml_converter.py input/file.xml output/data \
  --no-parallel
```

### Output Too Large
```bash
# Filter short text and disable metadata
python3 src/xml_converter.py input/file.xml output/data \
  --format llm_optimized \
  --min-length 50 \
  --no-metadata \
  --no-separators
```

### Check Results
```bash
# View sample output
head -50 output/llm_data_part1.txt

# Count tokens (approximate)
wc -w output/llm_data_part*.txt

# Check file sizes
ls -lh output/
```

## 🧰 Installation & Requirements

### Requirements
- **Python 3.6+**
- **psutil** (optional, for memory monitoring)

### Installation
```bash
# Clone repository
git clone https://github.com/Schludertrauma/XML-to-TXT-Converter.git
cd XML-to-TXT-Converter

# Install dependencies (optional)
pip install -r requirements.txt

# Test installation
python3 src/xml_converter.py --help
```

### No Installation Needed!
The converter uses only Python standard library (except optional psutil). You can run it immediately:
```bash
python3 src/xml_converter.py input/data.xml output/result --format llm_optimized
```

## 💻 Platform Support

| Platform | Scripts | Path Separator | Tested |
|----------|---------|----------------|--------|
| **Linux** | `.sh` | `/` | ✅ |
| **macOS** | `.sh` | `/` | ✅ |
| **Windows** | `.bat` | `\` | ✅ |

### Linux/macOS
```bash
./start.sh              # Start conversion
./help/monitor.sh       # Monitor progress
```

### Windows
```cmd
start.bat               # Start conversion
help\monitor.bat        # Monitor progress
```

## 📖 Additional Documentation

**This README contains everything you need to get started!**

For users who want more detailed information, additional guides are available in **[help/docs/](help/docs/)**:

| Guide | Description |
|-------|-------------|
| **[QUICKSTART_LLM.md](help/docs/QUICKSTART_LLM.md)** | 3-step quick start for impatient users |
| **[FORMAT_EXAMPLES.md](help/docs/FORMAT_EXAMPLES.md)** | Detailed format comparisons with side-by-side examples |
| **[LLM_TRAINING_GUIDE.md](help/docs/LLM_TRAINING_GUIDE.md)** | Comprehensive guide with PyTorch/HuggingFace integration examples |
| **[OPTIMIZATION_SUMMARY.md](help/docs/OPTIMIZATION_SUMMARY.md)** | Technical implementation details and benchmarks |

**Recommendation:**
- **New users**: Just read this README! It has everything you need.
- **Want examples**: Check [FORMAT_EXAMPLES.md](help/docs/FORMAT_EXAMPLES.md)
- **Deep dive**: See [LLM_TRAINING_GUIDE.md](help/docs/LLM_TRAINING_GUIDE.md) for advanced topics

## ❓ FAQ

**Q: Which format should I use?**
A: For most LLM training, use `--format llm_optimized`. It provides the best structure and quality.

**Q: How do I filter out noise?**
A: Use `--min-length 20` to remove text shorter than 20 characters.

**Q: Can I resume interrupted conversions?**
A: Yes! Use `--start-element N` and `--file-part N` to resume from where you stopped.

**Q: What's the output size?**
A: Typically 70-85% of input XML size, depending on format and filtering.

**Q: Does it work with any XML format?**
A: Yes! It works with any valid XML structure.

**Q: Is it backward compatible?**
A: Yes! Use `--format plain` for the original behavior.

## 🌟 Key Improvements Over Original

| Feature | Before | After |
|---------|--------|-------|
| **Output Formats** | 1 (plain) | 4 (multiple) |
| **Text Normalization** | ❌ | ✅ |
| **Content Filtering** | ❌ | ✅ |
| **Training Metadata** | ❌ | ✅ |
| **Statistics** | ❌ | ✅ (tokens/chars/lines) |
| **Documentation** | Basic | Comprehensive (6 guides) |
| **Memory Usage** | 2-5 GB | 2-5 GB (unchanged) ✅ |
| **Speed** | 5,000 elem/s | 4,800 elem/s (-4%) ✅ |

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Share your use cases and results
- Improve documentation

## 📄 License

MIT License – Free to use, modify, and distribute.

## 🙏 Acknowledgments

- Tested on Wikipedia XML dumps (105 GB)
- Optimized for transformer-based language models
- Built with Python standard library for maximum compatibility

---

**Ready to convert XML for LLM training?** 🚀

```bash
python3 src/xml_converter.py input/your_data.xml output/llm_data --format llm_optimized
```

For questions or support, open an issue on GitHub!
