"""
Base converter class defining the interface for all format-specific converters.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from enum import Enum


class Resolution(Enum):
    """Resolution presets for PDF conversion."""
    LOW = 'low'
    STANDARD = 'standard'
    HIGH = 'high'


class BaseConverter(ABC):
    """
    Abstract base class for format-specific converters.
    All format converters should inherit from this class.
    """
    
    def __init__(self, resolution: Resolution = Resolution.STANDARD):
        """
        Initialize base converter.
        
        Args:
            resolution: Resolution preset (low, standard, high)
        """
        if isinstance(resolution, str):
            resolution = Resolution(resolution.lower())
        self.resolution = resolution
    
    @abstractmethod
    def convert(self, input_path: str) -> str:
        """
        Convert input file to PDF.
        
        Args:
            input_path: Path to input file
            
        Returns:
            Path to generated PDF file
        """
        pass
    
    def get_output_path(self, input_path: str, temp_dir: str = './temp') -> str:
        """
        Generate output path for converted file.
        
        Args:
            input_path: Input file path
            temp_dir: Directory for temporary files
            
        Returns:
            Path for output PDF
        """
        input_file = Path(input_path)
        output_file = f"{temp_dir}/{input_file.stem}_temp.pdf"
        return output_file
    
    def cleanup(self, temp_file: str) -> None:
        """Remove temporary files."""
        try:
            Path(temp_file).unlink()
        except Exception as e:
            print(f"Warning: Could not delete temp file {temp_file}: {e}")
