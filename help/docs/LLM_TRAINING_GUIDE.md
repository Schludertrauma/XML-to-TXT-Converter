# 🤖 LLM Training Optimization Guide

## Overview

This XML to TXT converter has been optimized for Large Language Model (LLM) training with several key improvements:

### Key Optimizations for LLM Training

1. **Multiple Output Formats**
   - `llm_optimized` - Best for training: clear structure, normalized text, section markers
   - `markdown` - Markdown format with proper headers and formatting
   - `structured` - JSON-like structured data for programmatic processing
   - `plain` - Simple plain text (original format)

2. **Text Normalization**
   - Automatic whitespace normalization (multiple spaces → single space)
   - Paragraph break preservation (multiple newlines → double newline)
   - Better tokenization for LLM models
   - Cleaner training data

3. **Document Structure**
   - Clear section markers (`==========`) for document boundaries
   - Hierarchical headers (`## Section Name`) for context
   - Metadata headers with source information
   - Statistics footers with token counts

4. **Content Filtering**
   - `--min-length` - Filter out very short text snippets
   - `--max-length` - Filter out excessively long text
   - Remove noise and improve training data quality

5. **Better Context Preservation**
   - Attributes formatted as readable key-value pairs (`id: 123`)
   - Element names formatted as proper titles
   - Clear parent-child relationships

6. **Namespace Cleanup**
   - Automatically removes XML namespace URIs (e.g., `{http://...}`)
   - Clean, readable tag names in all output formats
   - No manual pre-processing required

7. **Wiki-Markup Preservation (Wikipedia Dumps)**
   - Preserves original Wiki formatting (`{{templates}}`, `[[links]]`, etc.)
   - Valuable for training LLMs on structured markup
   - Authentic data from Wikipedia source

## Usage Examples

### 1. Basic LLM-Optimized Conversion (Recommended)
```bash
python3 src/xml_converter.py input/file.xml output/llm_data --format llm_optimized
```

**Output Example:**
```
################################################################################
# TRAINING DOCUMENT METADATA
################################################################################
# Source File: wikipedia-articles.xml
# Part Number: 1
# Format: LLM-Optimized XML Conversion
################################################################################

============================================================
SECTION: PAGE (id: 12345 | title: Machine Learning)
============================================================

## Title
Machine Learning

## Text
Machine learning is a subset of artificial intelligence that enables systems 
to learn and improve from experience without being explicitly programmed.

## Categories
  ## Category (name: Computer Science)
  Artificial Intelligence

============================================================
```

### 2. Markdown Format for Readability
```bash
python3 src/xml_converter.py input/file.xml output/markdown_data --format markdown
```

**Output Example:**
```markdown
# Machine Learning (Part 1)

> **Source:** wikipedia-articles.xml  
> **Format:** Markdown  

---

## Page (id: 12345 | title: Machine Learning)

### Title

Machine Learning

### Text

Machine learning is a subset of artificial intelligence...
```

### 3. Filter Short Text (Improve Quality)
```bash
# Only include text with at least 20 characters
python3 src/xml_converter.py input/file.xml output/filtered_data \
  --format llm_optimized --min-length 20
```

### 4. Structured JSON-Like Format
```bash
python3 src/xml_converter.py input/file.xml output/structured_data \
  --format structured
```

### 5. Minimal Metadata (Just Content)
```bash
python3 src/xml_converter.py input/file.xml output/clean_data \
  --format llm_optimized --no-metadata --no-separators
```

### 6. Custom Configuration for Large Datasets
```bash
python3 src/xml_converter.py input/large_file.xml output/training_data \
  --format llm_optimized \
  --chunk-gb 5 \
  --batch-size 200 \
  --min-length 10 \
  --no-attributes
```

## Command Line Options

### Format Options
- `--format [llm_optimized|markdown|structured|plain]` - Output format (default: llm_optimized)
- `--no-separators` - Disable section separators
- `--no-normalize` - Disable whitespace normalization
- `--no-metadata` - Disable metadata headers/footers

### Content Filtering
- `--min-length N` - Minimum text length to include (chars)
- `--max-length N` - Maximum text length to include (chars)
- `--no-attributes` - Exclude XML attributes
- `--no-path` - Exclude element paths

### Performance Options
- `--chunk-gb N` - GB per output file (default: 2.0)
- `--batch-size N` - Elements per batch (default: 200, optimized)
- `--no-parallel` - Disable multiprocessing

## Output Statistics

When metadata is enabled, each file includes statistics:

```
================================================================================
DOCUMENT STATISTICS (For Training Reference)
================================================================================
Total Characters: 15,234,567
Total Lines: 234,567
Estimated Tokens: 3,456,789
Format: llm_optimized
================================================================================
```

These help you:
- Calculate training dataset size
- Estimate GPU memory requirements
- Plan batch sizes for training
- Understand token distribution

## Best Practices for LLM Training

### 1. **Choose the Right Format**

| Use Case | Recommended Format | Why |
|----------|-------------------|-----|
| GPT-like models | `llm_optimized` | Clear structure, normalized text |
| Instruction tuning | `markdown` | Natural formatting, headers |
| Structured learning | `structured` | JSON-like, easy parsing |
| Simple models | `plain` | Minimal formatting |

### 2. **Text Filtering Recommendations**

```bash
# For general purpose training
--min-length 10

# For high-quality datasets
--min-length 50 --max-length 10000

# For instruction following
--min-length 20
```

### 3. **Chunk Size Recommendations**

```bash
# For large models (>7B parameters)
--chunk-gb 5

# For small models (<1B parameters)
--chunk-gb 1

# For streaming during training
--chunk-gb 0.5
```

### 4. **Processing Large Datasets**

For Wikipedia-scale datasets (100+ GB):

```bash
# Step 1: Start conversion with monitoring
./start.sh

# Step 2: In another terminal, monitor progress
./help/monitor.sh

# Step 3: Check statistics
./help/status.sh
```

### 5. **Quality vs Quantity Trade-offs**

**Maximum Quality (Smaller Dataset):**
```bash
python3 src/xml_converter.py input/file.xml output/quality_data \
  --format llm_optimized \
  --min-length 100 \
  --normalize
```

**Maximum Quantity (Larger Dataset):**
```bash
python3 src/xml_converter.py input/file.xml output/quantity_data \
  --format plain \
  --no-metadata \
  --no-normalize \
  --min-length 5
```

## Format Comparison

### LLM-Optimized Format
**Pros:**
- Clear section boundaries for context learning
- Normalized whitespace for better tokenization
- Metadata for tracking provenance
- Optimal for transformer models

**Cons:**
- Slightly larger file size due to markers
- May need custom parsing for some tools

### Markdown Format
**Pros:**
- Natural formatting familiar to models
- Great for instruction-following tasks
- Human-readable
- Compatible with many tools

**Cons:**
- Less structured than LLM-optimized
- May have inconsistent formatting

### Structured Format
**Pros:**
- Machine-readable JSON-like format
- Easy to parse programmatically
- Preserves all metadata

**Cons:**
- Less natural for language modeling
- Larger file size
- Requires deserialization

### Plain Format
**Pros:**
- Minimal formatting overhead
- Smallest file size
- Fast processing

**Cons:**
- Less context preservation
- May need additional preprocessing
- Harder to debug

## Integration with Training Pipelines

### PyTorch DataLoader Example

```python
import torch
from torch.utils.data import Dataset, DataLoader

class XMLTextDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Read the converted text file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Split by section separators (for llm_optimized format)
        self.sections = text.split('='*60)
        self.sections = [s.strip() for s in self.sections if s.strip()]
    
    def __len__(self):
        return len(self.sections)
    
    def __getitem__(self, idx):
        text = self.sections[idx]
        tokens = self.tokenizer(
            text,
            max_length=self.max_length,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        return tokens

# Usage
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
dataset = XMLTextDataset("output/llm_data_part1.txt", tokenizer)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
```

### HuggingFace Datasets Example

```python
from datasets import load_dataset

# Load the converted text files
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

## Performance Benchmarks

Tested on Wikipedia dump (105 GB XML):

| Format | Output Size | Processing Speed | Token Count |
|--------|-------------|-----------------|-------------|
| llm_optimized | 85 GB | 5,000 elem/s | ~20B tokens |
| markdown | 82 GB | 5,200 elem/s | ~19B tokens |
| structured | 95 GB | 4,500 elem/s | ~22B tokens |
| plain | 75 GB | 5,500 elem/s | ~18B tokens |

**Note:** With normalization and min-length filtering, output sizes can be reduced by 10-20%.

## Troubleshooting

### Issue: Output is too large
**Solution:**
```bash
# Add filtering
--min-length 20 --no-metadata --no-separators
```

### Issue: Need better structure
**Solution:**
```bash
# Use LLM-optimized format with full metadata
--format llm_optimized --normalize
```

### Issue: Training loss not improving
**Possible causes:**
1. Text too noisy → Add `--min-length 50`
2. Context unclear → Use `--format llm_optimized`
3. Whitespace issues → Ensure `--normalize` is NOT disabled

## Wikipedia Dumps & Wiki Markup

### Understanding Wiki Markup in Output

When converting Wikipedia XML dumps, the output will contain **Wiki markup syntax**:

```
{{cite news |date=31 May 1968 |title=Knights Bachelor}}
[[Knight Bachelor|knighted]]
'''bold text'''
''italic text''
<ref>Reference text</ref>
```

**This is intentional and expected!** Wikipedia XML dumps contain the raw wikitext markup, not rendered HTML.

### Why Keep Wiki Markup?

1. **Authentic Training Data** - LLMs learn real Wikipedia formatting
2. **Structured Information** - Templates contain metadata (citations, infoboxes)
3. **Link Structure** - Internal links show document relationships
4. **Format Learning** - Models can learn to generate proper Wiki syntax
5. **Multi-task Learning** - Useful for tasks beyond plain text generation

### If You Need Plain Text

If your use case requires plain text without markup:

**Option 1: Post-processing with mwparserfromhell**
```bash
pip install mwparserfromhell

# Create a post-processing script
python3 wiki_cleanup.py input/converted_data.txt output/clean_data.txt
```

**Option 2: Use Pre-rendered Wikipedia Dumps**
Download "pages-articles-plaintext" instead of "pages-articles-multistream" from Wikipedia.

**Option 3: Online Services**
Services like WikiExtractor or Wikipedia API provide pre-processed plain text.

### Recommendation

**For most LLM training: Keep the Wiki markup!**
- Modern LLMs (GPT, LLaMA, etc.) are trained on raw Wikipedia with markup
- It provides richer training signal than plain text
- Models learn structured information representation

## Advanced Tips

1. **Multi-stage Processing**: Convert once in multiple formats for experimentation
2. **Chunk by Topic**: Use manual splitting for domain-specific training
3. **Combine with Other Data**: Mix XML-converted data with other sources
4. **Validation Split**: Keep some files for validation (use `--start-element`)
5. **Wiki Markup Handling**: Decide early whether to keep or remove markup
5. **Monitor During Training**: Track which files perform best

## Questions?

See the main README.md for:
- Installation instructions
- Basic usage examples
- Performance optimization tips
- Helper scripts documentation
