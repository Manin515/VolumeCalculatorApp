"""
setup.py for Volume of Revolution Calculator (macOS)
"""

from setuptools import setup

APP = ['src/volume_calculator_gui.py']
DATA_FILES = []

# Simplified options - let py2app auto-detect dependencies
OPTIONS = {
    'argv_emulation': False,
    'packages': ['numpy', 'matplotlib', 'sympy', 'tkinter'],
    'includes': [
        'numpy',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.pyplot',
        'mpl_toolkits.mplot3d',
        'sympy',
        'tkinter',
    ],
    'excludes': [
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'wx', 'gtk',
    ],
    'plist': {
        'CFBundleName': 'VolumeCalculator',
        'CFBundleDisplayName': 'Volume of Revolution Calculator',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.volumecalculator.app',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
