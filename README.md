# PDF Converter

A versatile file-to-PDF conversion tool with configurable resolution options and file size optimization.

## Features

- **Multiple File Format Support**: Convert various file formats (DOCX, PPTX, XLSX, images, etc.) to PDF
- **Resolution Options**: 
  - Low Definition (LD): Optimized for web viewing, smallest file size
  - Standard Definition (SD): Balanced quality and file size
  - High Definition (HD): Maximum quality, larger file size
- **File Size Control**: Set target file size and automatically optimize compression
- **Batch Processing**: Convert multiple files in one operation
- **Progress Tracking**: Real-time conversion progress updates

## Installation

```bash
# Clone the repository
git clone https://github.com/rbpatil0316/pdf-converter.git
cd pdf-converter

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from pdf_converter import PDFConverter

# Initialize converter
converter = PDFConverter(resolution='standard')

# Convert a single file
converter.convert('document.docx', 'output.pdf')

# Convert with file size target (in MB)
converter.convert('document.docx', 'output.pdf', target_size=5)

# Batch conversion
files = ['file1.docx', 'file2.pptx', 'image.jpg']
converter.batch_convert(files, output_dir='./pdfs/')
```

## Resolution Options

| Resolution | Quality | File Size | Use Case |
|-----------|---------|-----------|----------|
| **low** | Standard | Smallest | Web, Email distribution |
| **standard** | Good | Medium | General purpose |
| **high** | Excellent | Largest | Printing, archival |

## Configuration

Create a `config.yaml` file:

```yaml
default_resolution: standard
target_file_size: null  # MB, null for no limit
compress_images: true
dpi_settings:
  low: 72
  standard: 150
  high: 300
```

## Usage

### Command Line

```bash
# Basic conversion
python -m pdf_converter input.docx -o output.pdf

# With resolution
python -m pdf_converter input.docx -o output.pdf -r high

# With target file size
python -m pdf_converter input.docx -o output.pdf -s 5
```

### Python API

See examples in the `examples/` directory.

## Supported Formats

### Input Formats
- Documents: DOCX, DOC, ODT, RTF
- Presentations: PPTX, PPT, ODP
- Spreadsheets: XLSX, XLS, ODS, CSV
- Images: JPG, PNG, TIFF, BMP, GIF
- Web: HTML

### Output Format
- PDF (with customizable compression and quality)

## Architecture

- `src/core/` - Core conversion logic
- `src/formats/` - Format-specific handlers
- `src/compression/` - Compression and optimization algorithms
- `src/cli/` - Command-line interface
- `tests/` - Unit and integration tests
- `examples/` - Usage examples

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Building

```bash
python setup.py build
```

## Requirements

- Python 3.8+
- LibreOffice (for document conversion)
- ImageMagick (for image processing)
- GhostScript (for PDF optimization)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Troubleshooting

- **Unsupported format error**: Check `SUPPORTED_FORMATS` in config
- **File size too large**: Try `low` resolution or set smaller `target_size`
- **Conversion failure**: Ensure required system dependencies are installed

## Support

For issues and feature requests, please open a GitHub issue.
