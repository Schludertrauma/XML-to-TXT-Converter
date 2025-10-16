# Format Comparison Examples

This document shows actual output examples for each format to help you choose.

## Test Data (Input XML)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<company>
  <name>Tech Solutions Inc.</name>
  <founded>2020</founded>
  <employees>
    <employee id="E001">
      <name>Alice Johnson</name>
      <position>CEO</position>
      <email>alice@techsolutions.com</email>
    </employee>
  </employees>
</company>
```

---

## Format 1: LLM-Optimized (Recommended)

**Command:**
```bash
python3 src/xml_converter.py input.xml output/data --format llm_optimized
```

**Output:**
```
################################################################################
# TRAINING DOCUMENT METADATA
################################################################################
# Source File: sample_data.xml
# Part Number: 1
# Format: LLM-Optimized XML Conversion
# Normalization: Enabled
# Attributes: Included
################################################################################

############################################################
# ROOT: COMPANY
############################################################

Name:
  Tech Solutions Inc.

Founded:
  2020

============================================================
SECTION: EMPLOYEES
============================================================

    ## Employee (id: E001)
      ## Name
        Alice Johnson
      ## Position
        CEO
      ## Email
        alice@techsolutions.com

============================================================

================================================================================
DOCUMENT STATISTICS (For Training Reference)
================================================================================
Total Characters: 1,234
Total Lines: 45
Estimated Tokens: 187
Format: llm_optimized
================================================================================
```

**Pros:**
- ✅ Clear section boundaries (`=====`)
- ✅ Hierarchical structure with `##`
- ✅ Training metadata included
- ✅ Normalized whitespace
- ✅ Best for transformer models

**Cons:**
- ❌ Slightly larger file size (+10-15%)
- ❌ Custom format (not standard Markdown)

**Best For:** General LLM pre-training, GPT-style models, document understanding

---

## Format 2: Markdown

**Command:**
```bash
python3 src/xml_converter.py input.xml output/data --format markdown
```

**Output:**
```markdown
# sample_data (Part 1)

> **Source:** sample_data.xml  
> **Format:** Markdown  

---

# Company

## name

Tech Solutions Inc.

## founded

2020

## employees

### employee (id: E001)

#### name

Alice Johnson

#### position

CEO

#### email

alice@techsolutions.com
```

**Pros:**
- ✅ Standard Markdown format
- ✅ Natural for instruction-following
- ✅ Human-readable
- ✅ Compatible with many tools

**Cons:**
- ❌ Less structured than LLM-optimized
- ❌ Header levels can get deep

**Best For:** Instruction tuning, documentation tasks, Q&A datasets

---

## Format 3: Structured (JSON-like)

**Command:**
```bash
python3 src/xml_converter.py input.xml output/data --format structured
```

**Output:**
```json
{"tag": "company", "attributes": {}, "text": null}
  {"tag": "name", "attributes": {}, "text": "Tech Solutions Inc."}
  {"tag": "founded", "attributes": {}, "text": "2020"}
  {"tag": "employees", "attributes": {}, "text": null}
    {"tag": "employee", "attributes": {"id": "E001"}, "text": null}
      {"tag": "name", "attributes": {}, "text": "Alice Johnson"}
      {"tag": "position", "attributes": {}, "text": "CEO"}
      {"tag": "email", "attributes": {}, "text": "alice@techsolutions.com"}
```

**Pros:**
- ✅ Machine-readable
- ✅ Preserves all metadata
- ✅ Easy to parse programmatically
- ✅ Complete data preservation

**Cons:**
- ❌ Not natural language
- ❌ Larger file size (+20-25%)
- ❌ Requires deserialization

**Best For:** Structured data extraction, analysis pipelines, data science

---

## Format 4: Plain (Original)

**Command:**
```bash
python3 src/xml_converter.py input.xml output/data --format plain
```

**Output:**
```
Document: sample_data.xml
Part 1 | Process: 12345
================================================================================

company
  name
    Tech Solutions Inc.
  founded
    2020
  employees
    employee [id='E001']
      name
        Alice Johnson
      position
        CEO
      email
        alice@techsolutions.com
```

**Pros:**
- ✅ Smallest file size
- ✅ Simple indentation
- ✅ Minimal overhead
- ✅ Fast processing

**Cons:**
- ❌ Less structure
- ❌ Basic formatting
- ❌ No training metadata

**Best For:** Legacy compatibility, minimal needs, storage optimization

---

## Side-by-Side Comparison

| Feature | LLM-Optimized | Markdown | Structured | Plain |
|---------|---------------|----------|------------|-------|
| File Size | Medium (+10%) | Medium (+5%) | Large (+25%) | Small (baseline) |
| Structure | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Readability | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Training Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Metadata | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Minimal |
| Normalization | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Optional |
| Separators | ✅ Yes | ❌ No | ❌ No | ❌ No |

---

## Filtering Examples

### With Minimum Length Filter

**Command:**
```bash
python3 src/xml_converter.py input.xml output/data \
  --format llm_optimized \
  --min-length 10
```

**Effect:**
- Filters out text shorter than 10 characters
- Removes noise like "CEO", "2020" alone
- Keeps substantial content only

**Before (no filter):**
```
Founded:
  2020              ← Only 4 chars, noise

Position:
  CEO               ← Only 3 chars, noise

Name:
  Alice Johnson    ← 13 chars, kept
```

**After (--min-length 10):**
```
Name:
  Alice Johnson    ← 13 chars, kept

Email:
  alice@techsolutions.com  ← 27 chars, kept
```

---

## Recommendation Matrix

| Your Use Case | Recommended Format | Command |
|---------------|-------------------|---------|
| General LLM training | `llm_optimized` | `--format llm_optimized` |
| GPT-style models | `llm_optimized` | `--format llm_optimized` |
| Instruction following | `markdown` | `--format markdown` |
| Documentation corpus | `markdown` | `--format markdown` |
| Structured extraction | `structured` | `--format structured` |
| Data analysis | `structured` | `--format structured` |
| Legacy systems | `plain` | `--format plain` |
| Storage-constrained | `plain` | `--format plain --no-metadata` |

---

## Quick Decision Tree

```
Do you need structured, clean data for LLM training?
├─ YES → Use llm_optimized
│   └─ Need to remove noise? → Add --min-length 20
│
└─ NO → Are you doing instruction tuning?
    ├─ YES → Use markdown
    │
    └─ NO → Do you need programmatic parsing?
        ├─ YES → Use structured
        │
        └─ NO → Use plain
```

---

## Testing Different Formats

Run this to test all formats on your data:

```bash
# Test all formats quickly
for format in llm_optimized markdown structured plain; do
  python3 src/xml_converter.py input/test.xml output/test_$format \
    --format $format \
    --chunk-gb 0.01
done

# Compare results
ls -lh output/test_*
head -30 output/test_llm_optimized_part1.txt
head -30 output/test_markdown_part1.txt
```

---

## Summary

**For 90% of users:** Start with `--format llm_optimized`

**For instruction tuning:** Use `--format markdown`

**For analysis:** Use `--format structured`

**For minimal overhead:** Use `--format plain`

**Always consider:** Adding `--min-length 20` to filter noise

---

See [LLM_TRAINING_GUIDE.md](LLM_TRAINING_GUIDE.md) for complete documentation!
