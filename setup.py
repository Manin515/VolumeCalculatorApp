"""
setup.py for Volume of Revolution Calculator (macOS)
"""

from setuptools import setup

APP = ['src/volume_calculator_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
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
    'excludes': ['PyQt5', 'PyQt6', 'wx'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
