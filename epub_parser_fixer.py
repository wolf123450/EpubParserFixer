#!/usr/bin/env python3
import os
import zipfile
import tempfile
import shutil
import re
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import html
import argparse
from pathlib import Path

def fix_html_entities(text):
    """Convert HTML entities to their proper characters."""
    # Fix common HTML entities
    text = re.sub(r'&amp;#160;', ' ', text)  # Non-breaking space
    text = re.sub(r'&amp;#(\d+);', lambda m: chr(int(m.group(1))), text)
    
    # Unescape any remaining HTML entities
    return html.unescape(text)

def fix_br_tags(text):
    """Convert <br> tags to XHTML-compliant <br /> tags."""
    return re.sub(r'<br>', '<br />', text)

def extract_sourcetext_content(html_content):
    """Extract content from sourcetext tag within parsererror."""
    # Look for parsererror tag with sourcetext inside
    match = re.search(r'<parsererror[^>]*>.*?<sourcetext>(.*?)</sourcetext></parsererror>', 
                      html_content, re.DOTALL)
    
    if match:
        # Extract the content from sourcetext
        sourcetext_content = match.group(1)
        
        # Fix HTML entities in the sourcetext content
        sourcetext_content = fix_html_entities(sourcetext_content)
        
        # Fix <br> tags
        sourcetext_content = fix_br_tags(sourcetext_content)
        
        # Return the fixed content
        return sourcetext_content
    
    return None

def fix_chapter_content(content):
    """Fix XML parsing errors in chapter content."""
    # Check if the content contains a parsererror
    if "<parsererror" in content:
        print("  - Found XML parsing error, attempting to fix...")
        
        # Extract the sourcetext content
        sourcetext_content = extract_sourcetext_content(content)
        
        if sourcetext_content:
            # Replace the parsererror and sourcetext with the actual content
            fixed_content = re.sub(r'<div><parsererror.*?</parsererror></div>', 
                                 f'<div>{sourcetext_content}</div>', 
                                 content, flags=re.DOTALL)
            
            print("  - Successfully fixed parser error")
            return fixed_content
        else:
            print("  - Could not extract sourcetext content")
    
    return content

def process_epub(epub_path, output_path=None):
    """Process an EPUB file to fix XML parsing errors."""
    if output_path is None:
        # Create output path based on input path if not specified
        base_path = os.path.splitext(epub_path)[0]
        output_path = f"{base_path}_fixed.epub"
    
    print(f"Processing EPUB: {epub_path}")
    print(f"Output will be saved to: {output_path}")
    
    # Create a temporary directory to extract and modify the EPUB
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the EPUB to the temporary directory
        with zipfile.ZipFile(epub_path, 'r') as epub_zip:
            epub_zip.extractall(temp_dir)
        
        # Find all content files (HTML/XHTML)
        content_files = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(('.html', '.xhtml', '.htm')):
                    content_files.append(os.path.join(root, file))
        
        files_fixed = 0
        
        # Process each content file
        for content_file in content_files:
            print(f"Checking: {os.path.basename(content_file)}")
            
            # Read the file content
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix parser errors if present
            fixed_content = fix_chapter_content(content)
            
            # If content was modified, save it back
            if fixed_content != content:
                with open(content_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                files_fixed += 1
        
        print(f"Fixed {files_fixed} file(s) out of {len(content_files)} checked.")
        
        # Create the new EPUB file
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as new_epub:
            # Add all files from the temporary directory to the new EPUB
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Get the relative path in the EPUB
                    arcname = os.path.relpath(file_path, temp_dir)
                    new_epub.write(file_path, arcname)
    
    print(f"EPUB processing complete. Output saved to {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Fix XML parsing errors in EPUB files')
    parser.add_argument('epub_path', help='Path to the EPUB file to process')
    parser.add_argument('-o', '--output', help='Path for the output EPUB file (optional)')
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.isfile(args.epub_path):
        print(f"Error: Input file '{args.epub_path}' does not exist or is not a file.")
        return 1
    
    # Process the EPUB file
    try:
        output_path = process_epub(args.epub_path, args.output)
        print(f"Successfully processed EPUB. Output saved to {output_path}")
        return 0
    except Exception as e:
        print(f"Error processing EPUB: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
