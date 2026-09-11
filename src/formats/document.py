"""
Document format converter (DOCX, DOC, ODT, RTF to PDF).
Uses python-docx and LibreOffice backend for conversion.
"""

import os
import tempfile
import subprocess
from pathlib import Path
from .base import BaseConverter


class DocumentConverter(BaseConverter):
    """Convert document formats (DOCX, DOC, ODT, RTF) to PDF."""
    
    def __init__(self, resolution='standard'):
        super().__init__(resolution)
        self.supported_formats = ['.docx', '.doc', '.odt', '.rtf']
    
    def convert(self, input_path: str) -> str:
        """
        Convert document to PDF using LibreOffice.
        
        Args:
            input_path: Path to document file
            
        Returns:
            Path to generated PDF
        """
        input_file = Path(input_path)
        
        if input_file.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported document format: {input_file.suffix}")
        
        # Create temp directory for output
        temp_dir = tempfile.gettempdir()
        output_pdf = os.path.join(temp_dir, f"{input_file.stem}_converted.pdf")
        
        try:
            # Use LibreOffice for conversion
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', temp_dir,
                str(input_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")
            
            # LibreOffice outputs with original filename stem
            expected_output = os.path.join(temp_dir, f"{input_file.stem}.pdf")
            
            if os.path.exists(expected_output):
                return expected_output
            else:
                raise FileNotFoundError(f"PDF output not created: {expected_output}")
                
        except FileNotFoundError:
            raise RuntimeError("LibreOffice is not installed. Please install libreoffice to convert documents.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Document conversion timed out")
    
    def supports_format(self, file_extension: str) -> bool:
        """Check if format is supported."""
        return file_extension.lower() in self.supported_formats
