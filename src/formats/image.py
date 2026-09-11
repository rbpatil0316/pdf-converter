"""
Image format converter (JPG, PNG, TIFF, BMP, GIF, WEBP to PDF).
Uses Pillow for image processing and ReportLab for PDF generation.
"""

import os
import tempfile
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from .base import BaseConverter


class ImageConverter(BaseConverter):
    """Convert image formats to PDF."""
    
    def __init__(self, resolution='standard'):
        super().__init__(resolution)
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif', '.webp']
    
    def convert(self, input_path: str) -> str:
        """
        Convert image to PDF.
        
        Args:
            input_path: Path to image file
            
        Returns:
            Path to generated PDF
        """
        input_file = Path(input_path)
        
        if input_file.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported image format: {input_file.suffix}")
        
        try:
            # Open and validate image
            img = Image.open(input_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Determine page size and scale image accordingly
            page_width, page_height = letter
            img_width, img_height = img.size
            
            # Calculate scaling to fit image on page
            scale = min(page_width / img_width, page_height / img_height)
            
            # Apply quality settings based on resolution
            quality = self._get_quality_setting()
            
            # Create temp PDF
            temp_dir = tempfile.gettempdir()
            output_pdf = os.path.join(temp_dir, f"{input_file.stem}_converted.pdf")
            
            # Create PDF
            c = canvas.Canvas(output_pdf, pagesize=letter)
            
            # Draw image centered on page
            scaled_width = img_width * scale
            scaled_height = img_height * scale
            x = (page_width - scaled_width) / 2
            y = (page_height - scaled_height) / 2
            
            c.drawImage(ImageReader(img), x, y, width=scaled_width, height=scaled_height)
            c.save()
            
            return output_pdf
            
        except IOError as e:
            raise RuntimeError(f"Failed to open image file: {e}")
        except Exception as e:
            raise RuntimeError(f"Image conversion failed: {e}")
    
    def _get_quality_setting(self) -> int:
        """Get quality setting based on resolution."""
        quality_map = {
            'low': 60,
            'standard': 85,
            'high': 100,
        }
        return quality_map.get(self.resolution.value, 85)
    
    def supports_format(self, file_extension: str) -> bool:
        """Check if format is supported."""
        return file_extension.lower() in self.supported_formats
