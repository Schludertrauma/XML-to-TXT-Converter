#!/usr/bin/env python3
"""
Interactive menu for XML to TXT Converter
Simple interface for selecting files and conversion settings
"""

import os
import sys
from pathlib import Path


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header():
    """Print the menu header"""
    print("=" * 70)
    print("🧩 XML to TXT Converter - Interactive Menu")
    print("=" * 70)
    print()


def list_xml_files():
    """List all XML files in input directory"""
    input_dir = Path("input")
    xml_files = []
    
    # Get all XML files (including in subdirectories)
    for file_path in input_dir.rglob("*.xml"):
        xml_files.append(file_path)
    
    return sorted(xml_files)


def select_file():
    """Let user select an XML file"""
    xml_files = list_xml_files()
    
    if not xml_files:
        print("❌ No XML files found in input/ directory!")
        print("   Place your XML files in input/ and try again.")
        input("\nPress Enter to continue...")
        return None
    
    print("📁 Available XML files:")
    print()
    for idx, file_path in enumerate(xml_files, 1):
        file_size = file_path.stat().st_size
        size_str = format_size(file_size)
        print(f"  {idx}. {file_path.relative_to('input')} ({size_str})")
    
    print()
    print("  0. Back to main menu")
    print()
    
    while True:
        try:
            choice = input("👉 Select file (0-{}): ".format(len(xml_files))).strip()
            
            if choice == '0':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(xml_files):
                return xml_files[choice_num - 1]
            else:
                print(f"❌ Please enter a number between 0 and {len(xml_files)}")
        except ValueError:
            print("❌ Please enter a valid number")


def format_size(bytes_size):
    """Format byte size to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def select_format():
    """Let user select output format"""
    print("📝 Output Format:")
    print()
    print("  1. LLM-Optimized (Recommended for training)")
    print("     → Clear structure, section markers, normalized text")
    print()
    print("  2. Markdown")
    print("     → Headers, lists, readable format")
    print()
    print("  3. Structured")
    print("     → JSON-like with indentation")
    print()
    print("  4. Plain")
    print("     → Simple text, minimal formatting")
    print()
    print("  0. Back")
    print()
    
    formats = {
        '1': 'llm_optimized',
        '2': 'markdown',
        '3': 'structured',
        '4': 'plain'
    }
    
    while True:
        choice = input("👉 Select format (0-4) [default: 1]: ").strip()
        
        if choice == '0':
            return None
        
        if choice == '':
            return 'llm_optimized'
        
        if choice in formats:
            return formats[choice]
        
        print("❌ Please enter a number between 0 and 4")


def configure_settings():
    """Configure conversion settings"""
    settings = {
        'format': 'llm_optimized',
        'batch_size': 200,
        'chunk_gb': 2.0,
        'normalize': True,
        'metadata': True,
        'min_length': 0,
        'max_length': 0,
        'clean_wiki_markup': False
    }
    
    while True:
        clear_screen()
        print_header()
        print("⚙️  CONVERSION SETTINGS")
        print()
        print(f"  1. Output Format: {settings['format']}")
        print(f"  2. Batch Size: {settings['batch_size']} elements")
        print(f"  3. File Chunk Size: {settings['chunk_gb']} GB")
        print(f"  4. Normalize Whitespace: {'Yes' if settings['normalize'] else 'No'}")
        print(f"  5. Add Metadata: {'Yes' if settings['metadata'] else 'No'}")
        print(f"  6. Min Text Length: {settings['min_length']} chars (0=disabled)")
        print(f"  7. Max Text Length: {settings['max_length']} chars (0=disabled)")
        print(f"  8. Clean Wiki Markup: {'Yes' if settings['clean_wiki_markup'] else 'No'} (removes [[links]], {{{{templates}}}})")
        print()
        print("  9. 🔄 Reset to Defaults")
        print("  0. ✅ Save & Back")
        print()
        
        choice = input("👉 Choose setting to change (0-9): ").strip()
        
        if choice == '0':
            return settings
        elif choice == '1':
            fmt = select_format()
            if fmt:
                settings['format'] = fmt
        elif choice == '2':
            try:
                val = input(f"Batch size [current: {settings['batch_size']}]: ").strip()
                if val:
                    settings['batch_size'] = int(val)
            except ValueError:
                print("❌ Invalid number")
                input("Press Enter...")
        elif choice == '3':
            try:
                val = input(f"File chunk size in GB [current: {settings['chunk_gb']}]: ").strip()
                if val:
                    settings['chunk_gb'] = float(val)
            except ValueError:
                print("❌ Invalid number")
                input("Press Enter...")
        elif choice == '4':
            settings['normalize'] = not settings['normalize']
        elif choice == '5':
            settings['metadata'] = not settings['metadata']
        elif choice == '6':
            try:
                val = input(f"Min text length [current: {settings['min_length']}]: ").strip()
                if val:
                    settings['min_length'] = int(val)
            except ValueError:
                print("❌ Invalid number")
                input("Press Enter...")
        elif choice == '7':
            try:
                val = input(f"Max text length [current: {settings['max_length']}]: ").strip()
                if val:
                    settings['max_length'] = int(val)
            except ValueError:
                print("❌ Invalid number")
                input("Press Enter...")
        elif choice == '8':
            settings['clean_wiki_markup'] = not settings['clean_wiki_markup']
            status = "enabled" if settings['clean_wiki_markup'] else "disabled"
            print(f"✅ Wiki markup cleanup {status}")
            if settings['clean_wiki_markup']:
                print("   ℹ️  Requires: pip install mwparserfromhell")
            input("Press Enter...")
        elif choice == '9':
            settings = {
                'format': 'llm_optimized',
                'batch_size': 200,
                'chunk_gb': 2.0,
                'normalize': True,
                'metadata': True,
                'min_length': 0,
                'max_length': 0,
                'clean_wiki_markup': False
            }
            print("✅ Settings reset to defaults")
            input("Press Enter...")


def start_conversion(input_file, settings):
    """Start the conversion process"""
    clear_screen()
    print_header()
    print("🚀 STARTING CONVERSION")
    print()
    print(f"📄 Input: {input_file}")
    print(f"📝 Format: {settings['format']}")
    print(f"📦 Batch Size: {settings['batch_size']}")
    print(f"💾 Chunk Size: {settings['chunk_gb']} GB")
    print()
    
    # Generate output path
    output_base = f"output/{input_file.stem}_converted"
    
    # Build command
    cmd_parts = [
        "python3", "src/xml_converter.py",
        str(input_file),
        output_base,
        f"--format {settings['format']}",
        f"--batch-size {settings['batch_size']}",
        f"--chunk-gb {settings['chunk_gb']}"
    ]
    
    if not settings['normalize']:
        cmd_parts.append("--no-normalize")
    if not settings['metadata']:
        cmd_parts.append("--no-metadata")
    if settings['min_length'] > 0:
        cmd_parts.append(f"--min-length {settings['min_length']}")
    if settings['max_length'] > 0:
        cmd_parts.append(f"--max-length {settings['max_length']}")
    if settings.get('clean_wiki_markup', False):
        cmd_parts.append("--clean-wiki-markup")
    
    command = " ".join(cmd_parts)
    
    print("💻 Command:")
    print(f"   {command}")
    print()
    
    confirm = input("Continue? (Y/n): ").strip().lower()
    if confirm in ['', 'y', 'yes']:
        print()
        print("=" * 70)
        print()
        os.system(command)
        print()
        print("=" * 70)
        print()
        input("⏸️  Press Enter to return to menu...")
    else:
        print("❌ Conversion cancelled")
        input("Press Enter...")


def quick_convert():
    """Quick convert with default settings"""
    xml_file = select_file()
    if not xml_file:
        return
    
    settings = {
        'format': 'llm_optimized',
        'batch_size': 200,
        'chunk_gb': 2.0,
        'normalize': True,
        'metadata': True,
        'min_length': 0,
        'max_length': 0
    }
    
    start_conversion(xml_file, settings)


def custom_convert():
    """Convert with custom settings"""
    xml_file = select_file()
    if not xml_file:
        return
    
    clear_screen()
    print_header()
    settings = configure_settings()
    
    start_conversion(xml_file, settings)


def show_help():
    """Show help information"""
    clear_screen()
    print_header()
    print("❓ HELP & INFORMATION")
    print()
    print("📖 Quick Start:")
    print("   1. Place your XML file in input/ directory")
    print("   2. Choose option 1 (Quick Convert) for default settings")
    print("   3. Select your file and confirm")
    print()
    print("🎯 Output Formats:")
    print("   • LLM-Optimized: Best for training language models")
    print("   • Markdown: Human-readable with headers")
    print("   • Structured: JSON-like indented format")
    print("   • Plain: Simple flat text")
    print()
    print("⚙️  Settings:")
    print("   • Batch Size: Elements processed before writing (default: 200)")
    print("   • Chunk Size: Max size per output file (default: 2 GB)")
    print("   • Normalize: Clean up extra whitespace")
    print("   • Metadata: Add headers with file info")
    print()
    print("📁 Output Location:")
    print("   Files will be saved to: output/<filename>_converted_part1.txt")
    print()
    print("📊 Performance:")
    print("   • Speed: 4,000-6,000 elements/second")
    print("   • Memory: 2-5 GB RAM (constant)")
    print("   • Large files: Automatically split into chunks")
    print()
    print("📚 Documentation:")
    print("   See README.md and help/docs/ for detailed guides")
    print()
    input("Press Enter to return to menu...")


def main_menu():
    """Main menu loop"""
    while True:
        clear_screen()
        print_header()
        print("📋 MAIN MENU:")
        print()
        print("  1. 🚀 Quick Convert (Default Settings)")
        print("  2. ⚙️  Custom Convert (Configure Settings)")
        print("  3. 📁 View Input Files")
        print("  4. ❓ Help & Information")
        print("  0. 🚪 Exit")
        print()
        
        choice = input("👉 Enter your choice (0-4): ").strip()
        
        if choice == '0':
            print()
            print("👋 Goodbye!")
            sys.exit(0)
        elif choice == '1':
            quick_convert()
        elif choice == '2':
            custom_convert()
        elif choice == '3':
            clear_screen()
            print_header()
            xml_files = list_xml_files()
            if xml_files:
                print("📁 XML files in input/ directory:")
                print()
                for file_path in xml_files:
                    file_size = file_path.stat().st_size
                    size_str = format_size(file_size)
                    print(f"  • {file_path.relative_to('input')} ({size_str})")
            else:
                print("❌ No XML files found in input/ directory")
            print()
            input("Press Enter to continue...")
        elif choice == '4':
            show_help()
        else:
            print("❌ Invalid choice. Please enter 0-4")
            input("Press Enter...")


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
