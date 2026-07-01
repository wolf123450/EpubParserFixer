# EPUB Parser Fixer

A Python utility to fix common XML parsing errors in EPUB files. This tool extracts and repairs malformed HTML/XML content in EPUB books, making them compatible with e-readers and other EPUB readers.

## Features

- Extracts and processes EPUB files
- Fixes XML parsing errors by extracting the content from parser error messages
- Corrects common HTML entity encoding issues
- Converts HTML tags to XHTML-compliant format
- Preserves the original EPUB structure
- Creates a new fixed EPUB file without modifying the original

## Requirements

- Python 3.6+
- beautifulsoup4 (4.9.3+)
- lxml (4.6.3+)

## Installation

### Using pyenv with virtualenv (recommended)

1. Install pyenv (if not already installed)

   **On macOS/Linux:**
   ```bash
   curl https://pyenv.run | bash
   ```

   **On Windows:**
   Use pyenv-win:
   ```bash
   pip install pyenv-win --target $HOME/.pyenv
   ```

   For Windows, you'll need to add pyenv-win to your PATH:
   
   ```bash
   # Add these to your environment variables
   PYENV=%USERPROFILE%\.pyenv\pyenv-win
   PATH=%PYENV%\bin;%PYENV%\shims;%PATH%
   ```

   You can set these using PowerShell:
   ```powershell
   [System.Environment]::SetEnvironmentVariable('PYENV', $env:USERPROFILE + '\.pyenv\pyenv-win', 'User')
   [System.Environment]::SetEnvironmentVariable('PATH', $env:PYENV + '\bin;' + $env:PYENV + '\shims;' + $env:PATH, 'User')
   ```

3. Install Python using pyenv

   ```bash
   pyenv install 3.9.9
   ```

4. Create a virtual environment

   ```bash
   pyenv virtualenv 3.9.9 epub-fixer-env
   ```

4. Create a virtual environment using standard venv (for Windows users)

   ```bash
   # First set the Python version to use
   pyenv global 3.9.9
   
   # Create virtual environment in the project directory
   python -m venv .venv
   
   # Activate the environment
   .\.venv\Scripts\activate
   ```

5. Activate the virtual environment

   ```bash
   pyenv local epub-fixer-env
   ```

5. Install required packages

   ```bash
   pip install -r requirements.txt
   ```

### Standard installation

1. Clone or download this repository

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line:

```bash
python epub_parser_fixer.py path/to/your/ebook.epub
```

### Command-line options

- `epub_path`: Path to the EPUB file to process (required)
- `-o, --output`: Path for the output EPUB file (optional)

### Example

```bash
# Basic usage (creates book_fixed.epub)
python epub_parser_fixer.py book.epub

# Specify output file
python epub_parser_fixer.py book.epub -o fixed_book.epub
```

## How It Works

The script:
1. Extracts the EPUB file to a temporary directory
2. Identifies HTML/XHTML content files
3. Analyzes each file for XML parsing errors
4. Extracts the original content from the parser error messages
5. Fixes HTML entities and non-compliant HTML tags
6. Reconstructs the EPUB with the fixed content

## License

[Add your license information here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.