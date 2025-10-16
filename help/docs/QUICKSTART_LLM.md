# 🚀 Quick Start: LLM Training Optimization

Get started with LLM-optimized XML conversion in 3 steps!

## Step 1: Place Your XML File

```bash
# Copy your XML file to the input directory
cp your_data.xml input/
```

## Step 2: Run Conversion (Choose Your Format)

### Option A: LLM-Optimized (Recommended) ⭐
```bash
python3 src/xml_converter.py input/your_data.xml output/llm_data \
  --format llm_optimized
```

**Output:** Clear structure, normalized text, training metadata

### Option B: Markdown Format
```bash
python3 src/xml_converter.py input/your_data.xml output/markdown_data \
  --format markdown
```

**Output:** Markdown headers, natural formatting

### Option C: With Filtering (High Quality)
```bash
python3 src/xml_converter.py input/your_data.xml output/quality_data \
  --format llm_optimized \
  --min-length 20
```

**Output:** Filtered to remove short/noisy text

## Step 3: Use in Training

### PyTorch Example

```python
from torch.utils.data import Dataset

class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer):
        with open(file_path, 'r') as f:
            text = f.read()
        # Split by section markers
        self.sections = text.split('='*60)
        self.sections = [s.strip() for s in self.sections if s.strip()]
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.sections)
    
    def __getitem__(self, idx):
        return self.tokenizer(self.sections[idx], truncation=True, max_length=512)
```

### HuggingFace Datasets

```python
from datasets import load_dataset

dataset = load_dataset('text', data_files={
    'train': 'output/llm_data_part*.txt'
})
```

## Common Use Cases

### Wikipedia/Large Corpus
```bash
# Use default 2GB chunks
python3 src/xml_converter.py input/wikipedia.xml output/wiki_train \
  --format llm_optimized \
  --min-length 50
```

### Instruction Tuning Dataset
```bash
# Markdown format for Q&A style
python3 src/xml_converter.py input/qa_data.xml output/instruct \
  --format markdown \
  --min-length 10
```

### Clean Dataset (No Metadata)
```bash
# Just content, no headers
python3 src/xml_converter.py input/data.xml output/clean \
  --format llm_optimized \
  --no-metadata \
  --no-separators
```

## What You Get

### LLM-Optimized Format Output Example
```
################################################################################
# TRAINING DOCUMENT METADATA
################################################################################
# Source File: wikipedia.xml
# Part Number: 1
# Format: LLM-Optimized XML Conversion
################################################################################

============================================================
SECTION: ARTICLE (title: Machine Learning)
============================================================

## Introduction
Machine learning is a subset of artificial intelligence...

## History
  The term "machine learning" was coined in 1959...

============================================================

[Statistics footer with token counts]
```

### 📝 Note on Wikipedia Dumps
If converting Wikipedia XML dumps, the output will contain **Wiki markup** (e.g., `{{cite}}`, `[[links]]`, `'''bold'''`). This is **intentional** – it preserves the original Wikipedia formatting, which is valuable for training LLMs. See [LLM_TRAINING_GUIDE.md](LLM_TRAINING_GUIDE.md) for more details.

## Monitor Progress

```bash
# In another terminal, monitor conversion
./help/monitor.sh    # Linux/Mac
help\monitor.bat     # Windows
```

## Check Results

```bash
# View sample output
head -50 output/llm_data_part1.txt

# Count tokens (approximate)
wc -w output/llm_data_part*.txt

# Check file sizes
ls -lh output/
```

## Need Help?

- **Full Guide:** See [LLM_TRAINING_GUIDE.md](LLM_TRAINING_GUIDE.md)
- **All Options:** Run `python3 src/xml_converter.py --help`
- **Demo:** Run `python3 demo_formats.py`
- **Summary:** See [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)

## Tips for Best Results

1. **Start with defaults** - They're optimized for most use cases (batch size: 200)
2. **Filter noise** - Use `--min-length 20` to remove short text
3. **Check samples** - Look at first file before processing large datasets
4. **Use separators** - They help models learn document boundaries
5. **Keep metadata** - Useful for debugging and dataset management
6. **Wiki markup is OK** - For Wikipedia dumps, keeping markup is recommended for LLM training
7. **Namespaces cleaned** - XML namespace URIs are automatically removed

## Comparison Table

| Format | Best For | File Size | Quality |
|--------|----------|-----------|---------|
| llm_optimized | General training | Medium | ⭐⭐⭐⭐⭐ |
| markdown | Instruction tuning | Medium | ⭐⭐⭐⭐ |
| structured | Analysis/parsing | Large | ⭐⭐⭐⭐ |
| plain | Legacy/minimal | Small | ⭐⭐⭐ |

---

**That's it!** You're ready to convert XML to LLM-optimized text. 🎉

For detailed documentation, see the full guide:
📖 [LLM_TRAINING_GUIDE.md](LLM_TRAINING_GUIDE.md)
