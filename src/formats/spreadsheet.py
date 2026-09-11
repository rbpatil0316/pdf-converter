"""
Spreadsheet format converter (XLSX, XLS, ODS, CSV to PDF).
Uses LibreOffice backend for conversion.
"""

import os
import tempfile
import subprocess
from pathlib import Path
from .base import BaseConverter


class SpreadsheetConverter(BaseConverter):
    """Convert spreadsheet formats (XLSX, XLS, ODS, CSV) to PDF."""
    
    def __init__(self, resolution='standard'):
        super().__init__(resolution)
        self.supported_formats = ['.xlsx', '.xls', '.ods', '.csv']
    
    def convert(self, input_path: str) -> str:
        """
        Convert spreadsheet to PDF using LibreOffice.
        
        Args:
            input_path: Path to spreadsheet file
            
        Returns:
            Path to generated PDF
        """
        input_file = Path(input_path)
        
        if input_file.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported spreadsheet format: {input_file.suffix}")
        
        temp_dir = tempfile.gettempdir()
        
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
            raise RuntimeError("LibreOffice is not installed. Please install libreoffice to convert spreadsheets.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Spreadsheet conversion timed out")
    
    def supports_format(self, file_extension: str) -> bool:
        """Check if format is supported."""
        return file_extension.lower() in self.supported_formats
