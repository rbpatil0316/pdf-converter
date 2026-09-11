"""
Command-line interface for PDF Converter.
"""

import click
import os
from pathlib import Path
from ..core.converter import PDFConverter


@click.group()
def cli():
    """PDF Converter - Convert files to PDF with configurable resolution and size."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), required=True, help='Output PDF file path')
@click.option('-r', '--resolution', type=click.Choice(['low', 'standard', 'high']), 
              default='standard', help='Resolution quality (default: standard)')
@click.option('-s', '--size', type=float, help='Target file size in MB')
def convert(input_file, output, resolution, size):
    """Convert a single file to PDF."""
    try:
        converter = PDFConverter(resolution=resolution, target_size=size)
        converter.convert(input_file, output, target_size=size)
        output_size = os.path.getsize(output) / (1024 * 1024)
        click.echo(f"✓ Successfully converted {input_file} to {output}")
        click.echo(f"  Output size: {output_size:.2f} MB")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        exit(1)


@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.option('-o', '--output-dir', type=click.Path(), required=True, help='Output directory for PDFs')
@click.option('-r', '--resolution', type=click.Choice(['low', 'standard', 'high']), 
              default='standard', help='Resolution quality (default: standard)')
@click.option('-p', '--pattern', default='*', help='File pattern to match (default: *)')
@click.option('--recursive', is_flag=True, help='Recursively search subdirectories')
def batch(input_dir, output_dir, resolution, pattern, recursive):
    """Batch convert multiple files to PDF."""
    try:
        converter = PDFConverter(resolution=resolution)
        results = converter.batch_convert(input_dir, output_dir, pattern, recursive)
        
        successful = sum(1 for v in results.values() if v)
        failed = len(results) - successful
        
        click.echo(f"\n✓ Batch conversion complete:")
        click.echo(f"  Successful: {successful}")
        click.echo(f"  Failed: {failed}")
        
        if failed > 0:
            click.echo("\nFailed files:")
            for file, success in results.items():
                if not success:
                    click.echo(f"  - {file}")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        exit(1)


@cli.command()
def info():
    """Display supported formats and resolution information."""
    converter = PDFConverter()
    
    click.echo("\n=== Supported Input Formats ===")
    formats = converter.get_supported_formats()
    for fmt in formats:
        click.echo(f"  {fmt}")
    
    click.echo("\n=== Resolution Presets ===")
    resolutions = converter.get_resolution_info()
    for res_name, settings in resolutions.items():
        click.echo(f"\n  {res_name.upper()}:")
        for key, value in settings.items():
            click.echo(f"    {key}: {value}")


if __name__ == '__main__':
    cli()
