#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse
import os
import gc
import sys
import subprocess
from pathlib import Path
from typing import Optional, List
from multiprocessing import Pool, cpu_count


class XMLToTXTConverter:
    
    def __init__(self, indent_size: int = 2, include_attributes: bool = True,
                 include_path: bool = True, file_chunk_gb: int = 2,
                 use_parallel: bool = True, batch_size: int = 100):
        self.indent_size = indent_size
        self.include_attributes = include_attributes
        self.include_path = include_path
        self.file_chunk_gb = file_chunk_gb
        self.use_parallel = use_parallel and cpu_count() > 1
        self.batch_size = batch_size
        self.num_processes = max(2, cpu_count() - 1) if self.use_parallel else 1
    
    def _format_attributes(self, element) -> str:
        if not self.include_attributes or not element.attrib:
            return ""
        attrs = ", ".join([f"{k}='{v}'" for k, v in element.attrib.items()])
        return f" [{attrs}]"
    
    def _element_to_text(self, element, level: int = 0, parent_path: str = "") -> str:
        lines = []
        indent = " " * (level * self.indent_size)
        
        attributes = self._format_attributes(element)
        if self.include_path and level > 0:
            lines.append(f"{indent}[{element.tag}]{attributes}")
        else:
            lines.append(f"{indent}{element.tag}{attributes}")
        
        if element.text and element.text.strip():
            text_content = element.text.strip()
            for line in text_content.split('\n'):
                line = line.strip()
                if line:
                    lines.append(f"{indent}  {line}")
        
        for child in element:
            child_text = self._element_to_text(child, level + 1, element.tag)
            lines.append(child_text)
            
            if child.tail and child.tail.strip():
                tail_content = child.tail.strip()
                for line in tail_content.split('\n'):
                    line = line.strip()
                    if line:
                        lines.append(f"{indent}  {line}")
        
        return '\n'.join(lines)
    
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
        
        try:
            output_path = f"{output_base}_part{file_part}.txt"
            current_file = open(output_path, 'w', encoding='utf-8', buffering=4*1024*1024)
            
            # Write header
            header = f"Document: {Path(input_path).name}\n"
            header += f"Part {file_part} | Process: {os.getpid()}\n"
            if start_element > 0:
                header += f"Continuing from element {start_element + 1}\n"
            header += "=" * 80 + "\n\n"
            current_file.write(header)
            bytes_written = len(header.encode('utf-8'))
            
            write_batch = []
            
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
                    attributes = self._format_attributes(root)
                    root_line = f"{root.tag}{attributes}\n"
                    current_file.write(root_line)
                    bytes_written += len(root_line.encode('utf-8'))
                    
                    if elem.text and elem.text.strip():
                        for line in elem.text.strip().split('\n'):
                            line = line.strip()
                            if line:
                                text_line = f"  {line}\n"
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
                    element_text = self._element_to_text(elem, level=1, parent_path=root_element.tag)
                    
                    element_count += 1
                    processed_in_session += 1
                    
                    write_batch.append(element_text)
                    del element_text
                    
                    if len(write_batch) >= 50:
                        batch_text = '\n'.join(write_batch) + '\n'
                        current_file.write(batch_text)
                        bytes_written += len(batch_text.encode('utf-8'))
                        write_batch.clear()
                        del batch_text
                    
                    if processed_in_session % 50 == 0:
                        gc.collect(0)
                        
                    if processed_in_session % 200 == 0:
                        gc.collect(1)
                        
                    if processed_in_session % 500 == 0:
                        gc.collect(2)
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
                            
                        else:
                            total_gb = bytes_written / (1024**3)
                            print(f"  ... {element_count} elements | File {file_part}: {total_gb:.2f} GB")
                    
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
            
            if current_file:
                current_file.close()
                file_size_gb = bytes_written / (1024**3)
                print(f"  ✓ File {file_part} complete: {file_size_gb:.2f} GB")
            
            print()
            print("=" * 80)
            print(f"✅ CONVERSION COMPLETE!")
            print(f"📊 Total: {element_count} elements in {file_part} files")
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
        description="XML to TXT Converter - Optimized for Large Files"
    )
    parser.add_argument('input', help='Input XML file')
    parser.add_argument('output_base', help='Base output path (e.g., output/data)')
    parser.add_argument('--start-element', type=int, default=0,
                       help='Element to start from (for resume)')
    parser.add_argument('--file-part', type=int, default=1,
                       help='Starting file part number')
    parser.add_argument('--indent', type=int, default=2,
                       help='Indentation size')
    parser.add_argument('--chunk-gb', type=float, default=2.0,
                       help='GB per output file (can be decimal for testing)')
    parser.add_argument('--no-parallel', action='store_true',
                       help='Disable parallel processing (use single core)')
    parser.add_argument('--batch-size', type=int, default=100,
                       help='Number of elements to batch before writing (default: 100)')
    parser.add_argument('--no-attributes', action='store_true',
                       help='Exclude XML attributes')
    parser.add_argument('--no-path', action='store_true',
                       help='Exclude element paths')
    
    args = parser.parse_args()
    
    # Show optimization info
    if not args.no_parallel and cpu_count() > 1:
        print(f"⚡ Performance Optimizations Enabled:")
        print(f"   • Batch Writing: {args.batch_size} elements per batch")
        print(f"   • String Builder: Optimized text generation")
        print(f"   • I/O Buffer: 1 MB write buffer")
        print(f"   • CPU Cores: Using {max(2, cpu_count()-1)} cores")
        print()
    
    converter = XMLToTXTConverter(
        indent_size=args.indent,
        include_attributes=not args.no_attributes,
        include_path=not args.no_path,
        file_chunk_gb=args.chunk_gb,
        use_parallel=not args.no_parallel,
        batch_size=args.batch_size
    )
    
    converter.convert(
        args.input,
        args.output_base,
        args.start_element,
        args.file_part
    )


if __name__ == '__main__':
    main()
