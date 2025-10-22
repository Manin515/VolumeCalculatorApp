"""
Minimal setup.py for Volume Calculator
"""

from setuptools import setup

APP = ['src/volume_calculator_gui.py']
DATA_FILES = []

# Very minimal options - let py2app auto-detect everything
OPTIONS = {
    'argv_emulation': False,
    'packages': ['numpy', 'matplotlib', 'sympy', 'tkinter'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
