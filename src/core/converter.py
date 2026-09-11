"""
Core conversion logic for PDF Converter.
Handles format detection and routing to appropriate converters.
"""

import os
from pathlib import Path
from typing import Optional, Dict
from enum import Enum
from .base import BaseConverter
from ..formats.document import DocumentConverter
from ..formats.image import ImageConverter
from ..formats.presentation import PresentationConverter
from ..formats.spreadsheet import SpreadsheetConverter
from ..compression.optimizer import PDFOptimizer


class Resolution(Enum):
    """Resolution presets for PDF conversion."""
    LOW = 'low'
    STANDARD = 'standard'
    HIGH = 'high'


class PDFConverter:
    """
    Main PDF Converter class that orchestrates file conversion
    with support for multiple formats and resolution options.
    """
    
    # Supported format handlers
    FORMAT_HANDLERS = {
        # Documents
        '.docx': DocumentConverter,
        '.doc': DocumentConverter,
        '.odt': DocumentConverter,
        '.rtf': DocumentConverter,
        
        # Presentations
        '.pptx': PresentationConverter,
        '.ppt': PresentationConverter,
        '.odp': PresentationConverter,
        
        # Spreadsheets
        '.xlsx': SpreadsheetConverter,
        '.xls': SpreadsheetConverter,
        '.ods': SpreadsheetConverter,
        '.csv': SpreadsheetConverter,
        
        # Images
        '.jpg': ImageConverter,
        '.jpeg': ImageConverter,
        '.png': ImageConverter,
        '.tiff': ImageConverter,
        '.bmp': ImageConverter,
        '.gif': ImageConverter,
        '.webp': ImageConverter,
    }
    
    # DPI settings for different resolutions
    DPI_SETTINGS = {
        Resolution.LOW: {'dpi': 72, 'quality': 60, 'compress': True},
        Resolution.STANDARD: {'dpi': 150, 'quality': 85, 'compress': False},
        Resolution.HIGH: {'dpi': 300, 'quality': 100, 'compress': False},
    }
    
    def __init__(self, resolution: str = 'standard', target_size: Optional[float] = None):
        """
        Initialize PDF Converter.
        
        Args:
            resolution: 'low', 'standard', or 'high' (default: 'standard')
            target_size: Target file size in MB (optional)
        """
        try:
            self.resolution = Resolution(resolution.lower())
        except ValueError:
            raise ValueError(f"Invalid resolution. Must be one of: {', '.join([r.value for r in Resolution])}")
        
        self.target_size = target_size  # in MB
        self.optimizer = PDFOptimizer()
    
    def convert(self, input_path: str, output_path: str, target_size: Optional[float] = None) -> bool:
        """
        Convert a file to PDF.
        
        Args:
            input_path: Path to input file
            output_path: Path to output PDF file
            target_size: Override target file size in MB
            
        Returns:
            True if conversion successful, False otherwise
        """
        # Validate input file
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Get file extension
        file_ext = Path(input_path).suffix.lower()
        
        if file_ext not in self.FORMAT_HANDLERS:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        try:
            # Get appropriate converter
            handler_class = self.FORMAT_HANDLERS[file_ext]
            converter = handler_class(resolution=self.resolution)
            
            # Convert to PDF
            temp_pdf = converter.convert(input_path)
            
            # Optimize if needed
            effective_target_size = target_size or self.target_size
            if effective_target_size:
                self.optimizer.optimize_to_size(temp_pdf, output_path, effective_target_size)
            else:
                # Just apply resolution-based optimization
                self.optimizer.optimize(temp_pdf, output_path, self.resolution)
            
            return True
            
        except Exception as e:
            raise RuntimeError(f"Conversion failed for {input_path}: {str(e)}")
    
    def batch_convert(self, input_dir: str, output_dir: str, pattern: str = '*', 
                     recursive: bool = False) -> Dict[str, bool]:
        """
        Batch convert multiple files in a directory.
        
        Args:
            input_dir: Directory containing files to convert
            output_dir: Directory to save converted PDFs
            pattern: File pattern to match (default: '*' - all files)
            recursive: Search subdirectories (default: False)
            
        Returns:
            Dictionary with results for each file
        """
        os.makedirs(output_dir, exist_ok=True)
        results = {}
        
        input_path = Path(input_dir)
        search_method = input_path.rglob if recursive else input_path.glob
        
        for file_path in search_method(pattern):
            if file_path.is_file():
                output_file = os.path.join(output_dir, file_path.stem + '.pdf')
                try:
                    self.convert(str(file_path), output_file)
                    results[str(file_path)] = True
                except Exception as e:
                    print(f"Error converting {file_path}: {str(e)}")
                    results[str(file_path)] = False
        
        return results
    
    def get_supported_formats(self) -> list:
        """Get list of supported input formats."""
        return sorted(self.FORMAT_HANDLERS.keys())
    
    def get_resolution_info(self) -> Dict:
        """Get information about available resolutions."""
        return {
            r.value: settings 
            for r, settings in self.DPI_SETTINGS.items()
        }
