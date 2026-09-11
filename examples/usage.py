"""
Example usage of PDF Converter library.
"""

from src.core.converter import PDFConverter


def example_single_conversion():
    """Example: Convert a single file."""
    converter = PDFConverter(resolution='standard')
    converter.convert('document.docx', 'output.pdf')
    print("✓ Single file conversion complete")


def example_conversion_with_size():
    """Example: Convert with target file size."""
    converter = PDFConverter(resolution='standard', target_size=5)
    converter.convert('presentation.pptx', 'output.pdf', target_size=5)
    print("✓ Conversion with size optimization complete")


def example_batch_conversion():
    """Example: Batch convert multiple files."""
    converter = PDFConverter(resolution='high')
    results = converter.batch_convert(
        input_dir='./documents',
        output_dir='./pdfs',
        pattern='*.docx',
        recursive=False
    )
    
    successful = sum(1 for v in results.values() if v)
    print(f"✓ Batch conversion complete: {successful} files converted")


def example_different_resolutions():
    """Example: Try different resolution options."""
    input_file = 'large_document.docx'
    
    resolutions = ['low', 'standard', 'high']
    
    for res in resolutions:
        converter = PDFConverter(resolution=res)
        output_file = f'output_{res}.pdf'
        converter.convert(input_file, output_file)
        print(f"✓ Created {output_file} with {res} resolution")


def example_get_info():
    """Example: Get information about supported formats."""
    converter = PDFConverter()
    
    print("\nSupported Formats:")
    for fmt in converter.get_supported_formats():
        print(f"  {fmt}")
    
    print("\nResolution Information:")
    for res_name, settings in converter.get_resolution_info().items():
        print(f"  {res_name}: {settings}")


if __name__ == '__main__':
    print("PDF Converter Examples\n")
    print("=" * 50)
    
    # Uncomment examples to run
    # example_single_conversion()
    # example_conversion_with_size()
    # example_batch_conversion()
    # example_different_resolutions()
    example_get_info()
