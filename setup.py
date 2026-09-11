from setuptools import setup, find_packages

setup(
    name='pdf-converter',
    version='1.0.0',
    description='Convert various file formats to PDF with configurable resolution and file size optimization',
    author='rbpatil0316',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'python-pptx>=0.6.21',
        'python-docx>=0.8.11',
        'openpyxl>=3.8.1',
        'Pillow>=9.0.0',
        'PyPDF2>=3.0.0',
        'reportlab>=3.6.0',
        'click>=8.0.0',
        'PyYAML>=6.0',
        'tqdm>=4.62.0',
    ],
    entry_points={
        'console_scripts': [
            'pdf-converter=src.cli.main:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
