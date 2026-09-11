"""
Base converter for format-specific implementations.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseConverter(ABC):
    """
    Abstract base class for format-specific converters.
    All format converters should inherit from this class.
    """
    
    def __init__(self, resolution='standard'):
        """
        Initialize base converter.
        
        Args:
            resolution: Resolution preset (low, standard, high)
        """
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
    
    @abstractmethod
    def supports_format(self, file_extension: str) -> bool:
        """Check if the format is supported."""
        pass
