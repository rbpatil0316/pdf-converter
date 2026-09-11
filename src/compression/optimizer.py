"""
PDF optimization and compression module.
Handles file size reduction and quality optimization based on resolution presets.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from enum import Enum


class Resolution(Enum):
    """Resolution presets."""
    LOW = 'low'
    STANDARD = 'standard'
    HIGH = 'high'


class PDFOptimizer:
    """Optimize PDF files for different resolutions and target file sizes."""
    
    # GhostScript quality presets
    QUALITY_SETTINGS = {
        'low': {
            'dPDFSETTINGS': '/screen',
            'dQFactor': 0.4,
            'compression': 'high'
        },
        'standard': {
            'dPDFSETTINGS': '/ebook',
            'dQFactor': 0.75,
            'compression': 'medium'
        },
        'high': {
            'dPDFSETTINGS': '/prepress',
            'dQFactor': 1.0,
            'compression': 'low'
        },
    }
    
    def __init__(self):
        """Initialize PDF optimizer."""
        self.temp_dir = tempfile.gettempdir()
    
    def optimize(self, input_pdf: str, output_pdf: str, resolution: Resolution) -> bool:
        """
        Optimize PDF based on resolution preset.
        
        Args:
            input_pdf: Path to input PDF
            output_pdf: Path to output optimized PDF
            resolution: Resolution preset (low, standard, high)
            
        Returns:
            True if optimization successful
        """
        if isinstance(resolution, str):
            resolution = Resolution(resolution.lower())
        
        settings = self.QUALITY_SETTINGS.get(resolution.value)
        
        try:
            self._optimize_with_ghostscript(input_pdf, output_pdf, settings)
            return True
        except Exception as e:
            # If GhostScript fails, try fallback method
            print(f"GhostScript optimization failed: {e}. Using fallback method.")
            return self._fallback_optimize(input_pdf, output_pdf)
    
    def optimize_to_size(self, input_pdf: str, output_pdf: str, target_size_mb: float) -> bool:
        """
        Optimize PDF to target file size.
        
        Args:
            input_pdf: Path to input PDF
            output_pdf: Path to output PDF
            target_size_mb: Target file size in MB
            
        Returns:
            True if optimization successful
        """
        try:
            # Start with standard quality
            current_pdf = input_pdf
            
            # Get current file size
            current_size_mb = os.path.getsize(input_pdf) / (1024 * 1024)
            
            if current_size_mb <= target_size_mb:
                # Already within target size
                self._copy_file(input_pdf, output_pdf)
                return True
            
            # Try progressive optimization levels
            for resolution_level in ['standard', 'low']:
                self._optimize_with_ghostscript(
                    current_pdf, 
                    output_pdf, 
                    self.QUALITY_SETTINGS[resolution_level]
                )
                
                output_size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
                
                if output_size_mb <= target_size_mb:
                    return True
                
                current_pdf = output_pdf
            
            # If still too large, apply additional compression
            return self._apply_aggressive_compression(output_pdf, target_size_mb)
            
        except Exception as e:
            print(f"Size optimization failed: {e}")
            return False
    
    def _optimize_with_ghostscript(self, input_pdf: str, output_pdf: str, settings: dict) -> None:
        """Use GhostScript to optimize PDF."""
        
        cmd = [
            'gs',
            '-sDEVICE=pdfwrite',
            f"-dPDFSETTINGS={settings['dPDFSETTINGS']}",
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            '-dDetectDuplicateImages',
            '-r150',  # resolution
            f'-sOutputFile={output_pdf}',
            input_pdf
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"GhostScript failed: {result.stderr}")
    
    def _fallback_optimize(self, input_pdf: str, output_pdf: str) -> bool:
        """Fallback optimization method without GhostScript."""
        try:
            # Try using PyPDF2 for compression
            from PyPDF2 import PdfReader, PdfWriter
            
            reader = PdfReader(input_pdf)
            writer = PdfWriter()
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page.compress_content_streams()
                writer.add_page(page)
            
            with open(output_pdf, 'wb') as f:
                writer.write(f)
            
            return True
        except Exception as e:
            print(f"Fallback optimization failed: {e}")
            # Copy file as-is if all optimizations fail
            self._copy_file(input_pdf, output_pdf)
            return False
    
    def _apply_aggressive_compression(self, pdf_file: str, target_size_mb: float) -> bool:
        """Apply additional compression if standard methods don't achieve target."""
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            # Remove metadata and optimize streams
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                
                # Remove metadata
                if '/Contents' in page:
                    page.compress_content_streams()
                
                writer.add_page(page)
            
            # Rewrite without preserving metadata
            temp_file = os.path.join(self.temp_dir, 'temp_compressed.pdf')
            with open(temp_file, 'wb') as f:
                writer.write(f)
            
            # Replace original
            os.replace(temp_file, pdf_file)
            return True
            
        except Exception as e:
            print(f"Aggressive compression failed: {e}")
            return False
    
    def _copy_file(self, source: str, destination: str) -> None:
        """Copy file if no optimization is needed."""
        with open(source, 'rb') as src:
            with open(destination, 'wb') as dst:
                dst.write(src.read())
    
    def get_file_size_mb(self, pdf_path: str) -> float:
        """Get PDF file size in MB."""
        return os.path.getsize(pdf_path) / (1024 * 1024)
