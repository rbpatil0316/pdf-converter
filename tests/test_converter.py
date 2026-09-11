"""
Unit tests for PDF Converter core functionality.
"""

import unittest
import os
import tempfile
from pathlib import Path
from src.core.converter import PDFConverter, Resolution


class TestPDFConverter(unittest.TestCase):
    """Test cases for PDFConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.converter = PDFConverter(resolution='standard')
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_resolution_enum(self):
        """Test Resolution enum."""
        self.assertEqual(Resolution.LOW.value, 'low')
        self.assertEqual(Resolution.STANDARD.value, 'standard')
        self.assertEqual(Resolution.HIGH.value, 'high')
    
    def test_converter_initialization(self):
        """Test PDFConverter initialization."""
        converter = PDFConverter(resolution='high', target_size=10)
        self.assertEqual(converter.resolution.value, 'high')
        self.assertEqual(converter.target_size, 10)
    
    def test_invalid_resolution(self):
        """Test invalid resolution raises error."""
        with self.assertRaises(ValueError):
            PDFConverter(resolution='ultra-low')
    
    def test_supported_formats(self):
        """Test supported formats list."""
        formats = self.converter.get_supported_formats()
        self.assertIn('.docx', formats)
        self.assertIn('.jpg', formats)
        self.assertIn('.pptx', formats)
        self.assertIn('.xlsx', formats)
    
    def test_resolution_info(self):
        """Test resolution information."""
        info = self.converter.get_resolution_info()
        self.assertIn('low', info)
        self.assertIn('standard', info)
        self.assertIn('high', info)
        
        self.assertEqual(info['low']['dpi'], 72)
        self.assertEqual(info['standard']['dpi'], 150)
        self.assertEqual(info['high']['dpi'], 300)
    
    def test_nonexistent_file(self):
        """Test conversion of non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert('nonexistent.docx', 'output.pdf')
    
    def test_unsupported_format(self):
        """Test unsupported file format."""
        # Create a temp file with unsupported extension
        temp_file = os.path.join(self.temp_dir, 'test.xyz')
        Path(temp_file).touch()
        
        with self.assertRaises(ValueError):
            self.converter.convert(temp_file, 'output.pdf')


class TestResolution(unittest.TestCase):
    """Test Resolution enum."""
    
    def test_resolution_values(self):
        """Test resolution enum values."""
        self.assertEqual(Resolution.LOW.value, 'low')
        self.assertEqual(Resolution.STANDARD.value, 'standard')
        self.assertEqual(Resolution.HIGH.value, 'high')
    
    def test_resolution_creation(self):
        """Test creating Resolution from string."""
        res = Resolution('low')
        self.assertEqual(res, Resolution.LOW)


if __name__ == '__main__':
    unittest.main()
