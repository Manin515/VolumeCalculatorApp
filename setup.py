"""
setup.py for Volume of Revolution Calculator (macOS)
"""

from setuptools import setup

APP = ['src/volume_calculator_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,  # Set to False for Tkinter apps
    'packages': ['numpy', 'matplotlib', 'sympy', 'tkinter'],
    'includes': [
        'numpy',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',  # Important for TkAgg
        'matplotlib.backends.backend_tk',
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
