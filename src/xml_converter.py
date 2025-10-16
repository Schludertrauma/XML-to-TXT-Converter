#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse
import os
import gc
import sys
import re
import json
import subprocess
import time
from io import StringIO
from pathlib import Path
from typing import Optional, List, Dict
from multiprocessing import Pool, cpu_count
from collections import Counter


class XMLToTXTConverter:
    
    def __init__(self, indent_size: int = 2, include_attributes: bool = True,
                 include_path: bool = True, file_chunk_gb: int = 2,
                 use_parallel: bool = True, batch_size: int = 200,
                 output_format: str = 'llm_optimized', add_separators: bool = True,
                 normalize_whitespace: bool = True, add_metadata: bool = True,
                 min_text_length: int = 0, max_text_length: int = 0):
        self.indent_size = indent_size
        self.include_attributes = include_attributes
        self.include_path = include_path
        self.file_chunk_gb = file_chunk_gb
        self.use_parallel = use_parallel and cpu_count() > 1
        self.batch_size = batch_size
        self.num_processes = max(2, cpu_count() - 1) if self.use_parallel else 1
        self.output_format = output_format  # 'llm_optimized', 'plain', 'markdown', 'structured'
        self.add_separators = add_separators
        self.normalize_whitespace = normalize_whitespace
        self.add_metadata = add_metadata
        self.min_text_length = min_text_length
        self.max_text_length = max_text_length
        
        # Pre-compile regex patterns for performance
        self._regex_spaces = re.compile(r'[ \t]+')
        self._regex_newlines = re.compile(r'\n\s*\n\s*\n+')
        
        # Statistics for LLM training insights
        self.token_count = 0
        self.char_count = 0
        self.line_count = 0
    
    def _clean_tag_name(self, tag: str) -> str:
        """Clean XML tag names by removing namespaces and making readable."""
        # Remove namespace URLs (e.g., {http://...}tag -> tag)
        if '}' in tag:
            tag = tag.split('}', 1)[1]
        return tag
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better LLM training."""
        if not self.normalize_whitespace:
            return text
        
        # Use pre-compiled regex for better performance
        text = self._regex_spaces.sub(' ', text)  # Multiple spaces to single
        text = self._regex_newlines.sub('\n\n', text)  # Multiple newlines to double
        text = text.strip()
        return text
    
    def _format_attributes(self, element) -> str:
        if not self.include_attributes or not element.attrib:
            return ""
        
        # Clean attribute names (remove namespaces)
        clean_attribs = {self._clean_tag_name(k): v for k, v in element.attrib.items()}
        
        if self.output_format == 'llm_optimized':
            # Format as key-value pairs for better LLM understanding
            attrs = " | ".join([f"{k}: {v}" for k, v in clean_attribs.items()])
            return f" ({attrs})"
        elif self.output_format == 'structured':
            return f" {json.dumps(clean_attribs)}"
        else:
            attrs = ", ".join([f"{k}='{v}'" for k, v in clean_attribs.items()])
            return f" [{attrs}]"
    
    def _element_to_text(self, element, level: int = 0, parent_path: str = "") -> str:
        # Use StringIO for better performance than list + join
        output = StringIO()
        indent = " " * (level * self.indent_size)
        
        # Format based on output type
        if self.output_format == 'llm_optimized':
            lines = self._format_llm_optimized(element, level, parent_path, indent)
        elif self.output_format == 'markdown':
            lines = self._format_markdown(element, level, parent_path, indent)
        elif self.output_format == 'structured':
            lines = self._format_structured(element, level, parent_path, indent)
        else:  # plain
            lines = self._format_plain(element, level, parent_path, indent)
        
        for line in lines:
            output.write(line)
            output.write('\n')
        
        result = output.getvalue()
        output.close()
        
        # Update statistics (batched for efficiency)
        self.char_count += len(result)
        self.line_count += result.count('\n')
        # Approximate token count (words) - faster than split()
        self.token_count += result.count(' ') + result.count('\n')
        
        return result
    
    def _format_llm_optimized(self, element, level: int, parent_path: str, indent: str) -> List[str]:
        """Format optimized for LLM training with clear structure and context."""
        lines = []
        # Efficient check for children without double iteration
        has_children = any(True for _ in element)
        
        # Clean tag name for readability
        tag_name = self._clean_tag_name(element.tag)
        
        # Add element header with clear markers
        attributes = self._format_attributes(element)
        
        # Only major sections (with children) get big separators at level 1
        if level == 1 and has_children:
            lines.append(f"\n{'='*60}")
            lines.append(f"SECTION: {tag_name.upper()}{attributes}")
            lines.append(f"{'='*60}\n")
        elif level == 1 and not has_children:
            # Simple leaf elements at level 1
            lines.append(f"\n{tag_name.title()}{attributes}:")
        elif level > 1:
            # Nested elements
            lines.append(f"{indent}## {tag_name.title()}{attributes}")
        
        # Process text content
        has_text = element.text and element.text.strip()
        if has_text:
            text_content = self._normalize_text(element.text)
            if self._is_valid_text(text_content):
                # Add content with proper indentation
                for line in text_content.split('\n'):
                    if line.strip():
                        if level == 1:
                            lines.append(f"  {line}")
                        elif level > 1:
                            lines.append(f"{indent}  {line}")
                        else:
                            lines.append(f"{line}")
        
        # Process children
        for child in element:
            child_indent = " " * ((level + 1) * self.indent_size)
            child_text = self._element_to_text(child, level + 1, tag_name)
            if child_text:
                lines.append(child_text)
            
            # Process tail content
            if child.tail and child.tail.strip():
                tail_content = self._normalize_text(child.tail)
                if self._is_valid_text(tail_content):
                    for line in tail_content.split('\n'):
                        if line.strip():
                            if level == 1:
                                lines.append(f"  {line}")
                            elif level > 1:
                                lines.append(f"{indent}  {line}")
                            else:
                                lines.append(f"{line}")
        
        # Add section separator for major sections
        if level == 1 and has_children and self.add_separators:
            lines.append(f"\n{'='*60}\n")
        
        return lines
    
    def _format_markdown(self, element, level: int, parent_path: str, indent: str) -> List[str]:
        """Format as Markdown for better readability."""
        lines = []
        tag_name = self._clean_tag_name(element.tag)
        has_children = any(True for _ in element)
        
        # Format attributes for markdown (cleaner than default)
        attr_str = ""
        if self.include_attributes and element.attrib:
            clean_attribs = {self._clean_tag_name(k): v for k, v in element.attrib.items()}
            attrs = [f"**{k}**: {v}" for k, v in clean_attribs.items()]
            attr_str = f" ({', '.join(attrs)})"
        
        # Use markdown headers with appropriate levels
        if level == 1 and has_children and self.add_separators:
            # Major sections get horizontal rules
            lines.append(f"\n---\n")
            lines.append(f"## {tag_name}{attr_str}\n")
        else:
            header_level = min(level + 2, 6)
            lines.append(f"{'#' * header_level} {tag_name}{attr_str}")
        
        # Add text content as blockquote for leaf elements
        if element.text and element.text.strip():
            text_content = self._normalize_text(element.text)
            if self._is_valid_text(text_content):
                if not has_children and level > 0:
                    # Leaf node - format as blockquote
                    lines.append(f"> {text_content}\n")
                else:
                    lines.append(f"\n{text_content}\n")
        
        # Process children
        for child in element:
            child_text = self._element_to_text(child, level + 1, tag_name)
            if child_text:
                lines.append(child_text)
            
            if child.tail and child.tail.strip():
                tail_content = self._normalize_text(child.tail)
                if self._is_valid_text(tail_content):
                    lines.append(f"\n{tail_content}\n")
        
        return lines
    
    def _format_structured(self, element, level: int, parent_path: str, indent: str) -> List[str]:
        """Format as structured data (JSON-like) for programmatic processing."""
        lines = []
        tag_name = self._clean_tag_name(element.tag)
        has_children = any(True for _ in element)
        
        # Build structured data object
        data = {
            "tag": tag_name,
            "level": level,
            "path": f"{parent_path}/{tag_name}" if parent_path else tag_name,
            "has_children": has_children
        }
        
        # Add attributes if present (with cleaned names)
        if element.attrib:
            data["attributes"] = {self._clean_tag_name(k): v for k, v in element.attrib.items()}
        
        # Add text content if present
        if element.text and element.text.strip():
            text_content = self._normalize_text(element.text)
            if self._is_valid_text(text_content):
                data["text"] = text_content
        
        # Add visual separator for major sections
        if level == 1 and has_children and self.add_separators:
            lines.append(f"{indent}{'─' * 40}")
        
        # Write JSON object (pretty-printed for readability)
        lines.append(f"{indent}{json.dumps(data, ensure_ascii=False, indent=2)}")
        
        # Process children with increased indentation
        for child in element:
            child_text = self._element_to_text(child, level + 1, data["path"])
            if child_text:
                lines.append(child_text)
        
        return lines
    
    def _format_plain(self, element, level: int, parent_path: str, indent: str) -> List[str]:
        """Plain text format with improved readability."""
        lines = []
        tag_name = self._clean_tag_name(element.tag)
        has_children = any(True for _ in element)
        attributes = self._format_attributes(element)
        
        # Add section separators for major sections
        if level == 1 and has_children and self.add_separators:
            lines.append(f"\n{indent}{'─' * 50}")
            lines.append(f"{indent}[{tag_name}]{attributes}")
            lines.append(f"{indent}{'─' * 50}")
        elif level == 1 and not has_children:
            # Simple leaf at level 1
            lines.append(f"\n{indent}{tag_name}{attributes}:")
        else:
            # Nested elements
            if self.include_path and level > 0:
                lines.append(f"{indent}• {tag_name}{attributes}")
            else:
                lines.append(f"{indent}{tag_name}{attributes}")
        
        # Add text content
        if element.text and element.text.strip():
            text_content = self._normalize_text(element.text)
            if self._is_valid_text(text_content):
                for line in text_content.split('\n'):
                    line = line.strip()
                    if line:
                        if level == 1:
                            lines.append(f"{indent}  {line}")
                        else:
                            lines.append(f"{indent}    {line}")
        
        # Process children
        for child in element:
            child_text = self._element_to_text(child, level + 1, tag_name)
            if child_text:
                lines.append(child_text)
            
            # Process tail text
            if child.tail and child.tail.strip():
                tail_content = self._normalize_text(child.tail)
                if self._is_valid_text(tail_content):
                    for line in tail_content.split('\n'):
                        line = line.strip()
                        if line:
                            lines.append(f"{indent}  {line}")
        
        return lines
    
    def _is_valid_text(self, text: str) -> bool:
        """Check if text meets length requirements."""
        if not text:
            return False
        
        text_len = len(text)
        
        if self.min_text_length > 0 and text_len < self.min_text_length:
            return False
        
        if self.max_text_length > 0 and text_len > self.max_text_length:
            return False
        
        return True
    
    def _generate_header(self, input_path: str, file_part: int, start_element: int) -> str:
        """Generate document header with metadata for LLM training."""
        if self.output_format == 'llm_optimized':
            header = f"""
{'#'*80}
# TRAINING DOCUMENT METADATA
{'#'*80}
# Source File: {Path(input_path).name}
# Part Number: {file_part}
# Format: LLM-Optimized XML Conversion
# Normalization: {'Enabled' if self.normalize_whitespace else 'Disabled'}
# Attributes: {'Included' if self.include_attributes else 'Excluded'}
"""
            if start_element > 0:
                header += f"# Resume Point: Element {start_element + 1}\n"
            header += f"{'#'*80}\n\n"
            return header
        elif self.output_format == 'markdown':
            header = f"# {Path(input_path).stem} (Part {file_part})\n\n"
            header += f"> **Source:** {Path(input_path).name}  \n"
            header += f"> **Format:** Markdown  \n\n"
            header += "---\n\n"
            return header
        else:
            header = f"Document: {Path(input_path).name}\n"
            header += f"Part {file_part} | Process: {os.getpid()}\n"
            if start_element > 0:
                header += f"Continuing from element {start_element + 1}\n"
            header += "=" * 80 + "\n\n"
            return header
    
    def _generate_statistics_footer(self) -> str:
        """Generate statistics footer for training insights."""
        footer = f"""
{'='*80}
DOCUMENT STATISTICS (For Training Reference)
{'='*80}
Total Characters: {self.char_count:,}
Total Lines: {self.line_count:,}
Estimated Tokens: {self.token_count:,}
Format: {self.output_format}
{'='*80}
"""
        return footer
    
    def convert(self, input_path: str, output_base: str, 
                start_element: int = 0, file_part: int = 1):
        print(f"=" * 80)
        print(f"🔄 Process started (PID: {os.getpid()})")
        if start_element > 0:
            print(f"📍 Resuming from element {start_element}, file part {file_part}")
        print(f"=" * 80)
        print()
        
        file_chunk_bytes = self.file_chunk_gb * 1024 * 1024 * 1024
        element_count = 0
        processed_in_session = 0
        bytes_written = 0
        current_file = None
        root_element = None
        root_written = False
        files_in_session = 0
        last_update_time = time.time()  # Track last progress update
        
        try:
            output_path = f"{output_base}_part{file_part}.txt"
            current_file = open(output_path, 'w', encoding='utf-8', buffering=4*1024*1024)
            
            # Write header with metadata for LLM training
            if self.add_metadata:
                header = self._generate_header(input_path, file_part, start_element)
            else:
                header = ""
            
            if header:
                current_file.write(header)
                bytes_written = len(header.encode('utf-8'))
            else:
                bytes_written = 0
            
            write_batch = []
            start_time = time.time()  # Track overall processing time
            
            context = ET.iterparse(input_path, events=('start', 'end'))
            context = iter(context)
            event, root = next(context)
            
            skip_count = 0
            for event, elem in context:
                if event != 'end':
                    continue
                
                if elem == root:
                    continue
                
                if root_element is None:
                    root_element = root
                    
                    # Write root element header if using certain formats
                    if self.output_format in ['llm_optimized', 'markdown']:
                        root_tag = self._clean_tag_name(root.tag)
                        attributes = self._format_attributes(root)
                        if self.output_format == 'llm_optimized':
                            root_line = f"\n{'#'*60}\n# ROOT: {root_tag.upper()}{attributes}\n{'#'*60}\n\n"
                        else:
                            root_line = f"# {root_tag.title()}{attributes}\n\n"
                        current_file.write(root_line)
                        bytes_written += len(root_line.encode('utf-8'))
                        
                        if root.text and root.text.strip():
                            text_content = self._normalize_text(root.text)
                            if self._is_valid_text(text_content):
                                text_line = f"{text_content}\n\n"
                                current_file.write(text_line)
                                bytes_written += len(text_line.encode('utf-8'))
                    
                    root_written = True
                    continue
                
                if element_count < start_element:
                    element_count += 1
                    elem.clear()
                    if root_element is not None and elem in root_element:
                        root_element.remove(elem)
                    del elem
                    
                    if element_count % 10 == 0:
                        gc.collect()
                    continue
                
                if root_written:
                    # Process element (has_children check is done inside format methods if needed)
                    root_tag = self._clean_tag_name(root_element.tag)
                    element_text = self._element_to_text(elem, level=1, parent_path=root_tag)
                    
                    element_count += 1
                    processed_in_session += 1
                    
                    write_batch.append(element_text)
                    del element_text
                    
                    # Write batch when reaching batch_size (default 200)
                    if len(write_batch) >= self.batch_size:
                        batch_text = '\n'.join(write_batch) + '\n'
                        current_file.write(batch_text)
                        bytes_written += len(batch_text.encode('utf-8'))
                        write_batch.clear()
                        del batch_text
                    
                    # Optimized GC intervals (tuned for batch_size=200)
                    if processed_in_session % 100 == 0:
                        gc.collect(0)  # Quick gen-0 collection
                        
                    if processed_in_session % 400 == 0:
                        gc.collect(1)  # Gen-1 collection
                        
                    if processed_in_session % 1000 == 0:
                        gc.collect(2)  # Full collection
                        current_file.flush()
                        os.fsync(current_file.fileno())
                        
                        if bytes_written >= file_chunk_bytes:
                            if write_batch:
                                batch_text = '\n'.join(write_batch) + '\n'
                                current_file.write(batch_text)
                                bytes_written += len(batch_text.encode('utf-8'))
                                write_batch.clear()
                                del batch_text
                            
                            current_file.close()
                            file_size_gb = bytes_written / (1024**3)
                            print(f"  ✓ File {file_part} complete: {file_size_gb:.2f} GB, {processed_in_session} elements")
                            
                            file_part += 1
                            
                            output_path = f"{output_base}_part{file_part}.txt"
                            current_file = open(output_path, 'w', encoding='utf-8', buffering=4*1024*1024)
                            
                            header = f"Document: {Path(input_path).name}\n"
                            header += f"Part {file_part} | Process: {os.getpid()}\n"
                            header += f"Continuing from element {element_count + 1}\n"
                            header += "=" * 80 + "\n\n"
                            current_file.write(header)
                            bytes_written = len(header.encode('utf-8'))
                            processed_in_session = 0
                            last_update_time = time.time()  # Reset timer for new file
                    
                    # Progress update every 1 second (time-based for smooth updates)
                    current_time = time.time()
                    if current_time - last_update_time >= 1.0:
                        total_gb = bytes_written / (1024**3)
                        elapsed = current_time - start_time
                        elements_per_sec = element_count / elapsed if elapsed > 0 else 0
                        print(f"\r  ... {element_count:,} elements | File {file_part}: {total_gb:.2f} GB | {int(elements_per_sec):,} elem/s", end='', flush=True)
                        last_update_time = current_time
                    
                    elem.clear()
                    
                    try:
                        if root is not None and elem in root:
                            root.remove(elem)
                    except ValueError:
                        pass
                    
                    del elem
                    
                    if processed_in_session % 1000 == 0 and root is not None:
                        for child in list(root):
                            if child.tag != root.tag:
                                try:
                                    root.remove(child)
                                except ValueError:
                                    pass
            
            if write_batch and current_file:
                batch_text = '\n'.join(write_batch) + '\n'
                current_file.write(batch_text)
                bytes_written += len(batch_text.encode('utf-8'))
                write_batch.clear()
            
            # Add statistics footer if enabled
            if current_file and self.add_metadata:
                footer = self._generate_statistics_footer()
                current_file.write(footer)
            
            if current_file:
                current_file.close()
                file_size_gb = bytes_written / (1024**3)
                print()  # New line after progress updates
                print(f"  ✓ File {file_part} complete: {file_size_gb:.2f} GB")
            
            print()
            print("=" * 80)
            print(f"✅ CONVERSION COMPLETE!")
            print(f"📊 Total: {element_count} elements in {file_part} files")
            if self.add_metadata:
                print(f"📝 Total characters: {self.char_count:,}")
                print(f"📝 Total tokens (estimated): {self.token_count:,}")
                print(f"📝 Output format: {self.output_format}")
            print("=" * 80)
            
        except Exception as e:
            if current_file:
                current_file.close()
            print(f"❌ Error: {e}")
            raise
        finally:
            if root_element is not None:
                root_element.clear()
            gc.collect()
    



def main():
    parser = argparse.ArgumentParser(
        description="XML to TXT Converter - Optimized for LLM Training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Output Formats:
  llm_optimized  - Best for LLM training (default): clear structure, normalized text
  markdown       - Markdown format with headers and formatting
  structured     - JSON-like structured data
  plain          - Simple plain text (original format)

Examples:
  # LLM-optimized format with metadata
  python3 xml_converter.py input.xml output/data --format llm_optimized
  
  # Markdown format without metadata
  python3 xml_converter.py input.xml output/data --format markdown --no-metadata
  
  # Filter short text (< 10 chars)
  python3 xml_converter.py input.xml output/data --min-length 10
        """
    )
    parser.add_argument('input', help='Input XML file')
    parser.add_argument('output_base', help='Base output path (e.g., output/data)')
    parser.add_argument('--start-element', type=int, default=0,
                       help='Element to start from (for resume)')
    parser.add_argument('--file-part', type=int, default=1,
                       help='Starting file part number')
    parser.add_argument('--indent', type=int, default=2,
                       help='Indentation size (default: 2)')
    parser.add_argument('--chunk-gb', type=float, default=2.0,
                       help='GB per output file (default: 2.0)')
    parser.add_argument('--no-parallel', action='store_true',
                       help='Disable parallel processing (use single core)')
    parser.add_argument('--batch-size', type=int, default=200,
                       help='Number of elements to batch before writing (default: 200)')
    parser.add_argument('--no-attributes', action='store_true',
                       help='Exclude XML attributes')
    parser.add_argument('--no-path', action='store_true',
                       help='Exclude element paths')
    
    # LLM Training Optimization Options
    parser.add_argument('--format', '--output-format', dest='format', 
                       choices=['llm_optimized', 'markdown', 'structured', 'plain'],
                       default='llm_optimized',
                       help='Output format (default: llm_optimized)')
    parser.add_argument('--no-separators', action='store_true',
                       help='Disable section separators')
    parser.add_argument('--no-normalize', action='store_true',
                       help='Disable whitespace normalization')
    parser.add_argument('--no-metadata', action='store_true',
                       help='Disable document metadata headers/footers')
    parser.add_argument('--min-length', type=int, default=0,
                       help='Minimum text length to include (filter short text)')
    parser.add_argument('--max-length', type=int, default=0,
                       help='Maximum text length to include (filter long text)')
    
    args = parser.parse_args()
    
    # Show optimization info
    print()
    print("🤖 LLM Training Optimization Settings:")
    print(f"   • Output Format: {args.format}")
    print(f"   • Whitespace Normalization: {'Enabled' if not args.no_normalize else 'Disabled'}")
    print(f"   • Metadata: {'Enabled' if not args.no_metadata else 'Disabled'}")
    print(f"   • Section Separators: {'Enabled' if not args.no_separators else 'Disabled'}")
    if args.min_length > 0:
        print(f"   • Minimum Text Length: {args.min_length} chars")
    if args.max_length > 0:
        print(f"   • Maximum Text Length: {args.max_length} chars")
    print()
    
    if not args.no_parallel and cpu_count() > 1:
        print(f"⚡ Performance Optimizations Enabled:")
        print(f"   • Batch Writing: {args.batch_size} elements per batch")
        print(f"   • String Builder: Optimized text generation")
        print(f"   • I/O Buffer: 4 MB write buffer")
        print(f"   • CPU Cores: Using {max(2, cpu_count()-1)} cores")
        print()
    
    converter = XMLToTXTConverter(
        indent_size=args.indent,
        include_attributes=not args.no_attributes,
        include_path=not args.no_path,
        file_chunk_gb=args.chunk_gb,
        use_parallel=not args.no_parallel,
        batch_size=args.batch_size,
        output_format=args.format,
        add_separators=not args.no_separators,
        normalize_whitespace=not args.no_normalize,
        add_metadata=not args.no_metadata,
        min_text_length=args.min_length,
        max_text_length=args.max_length
    )
    
    converter.convert(
        args.input,
        args.output_base,
        args.start_element,
        args.file_part
    )


if __name__ == '__main__':
    main()
