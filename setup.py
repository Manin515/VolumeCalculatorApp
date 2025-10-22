"""
setup.py for Volume of Revolution Calculator (macOS)
"""

from setuptools import setup

APP = ['src/volume_calculator_gui.py']
DATA_FILES = []

OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'numpy', 
        'matplotlib', 
        'sympy',
        'tkinter',
        'mpl_toolkits',
        'PIL',
        'pkg_resources.py2_warn'
    ],
    'includes': [
        # Core packages
        'numpy',
        'matplotlib',
        'sympy',
        
        # Matplotlib components
        'matplotlib.backends.backend_tkagg',
        'matplotlib.backends.backend_tk',
        'matplotlib.pyplot',
        'matplotlib.figure',
        'matplotlib.axes._base',
        'matplotlib.axes._axes',
        'matplotlib.backends._backend_tk',
        
        # 3D plotting
        'mpl_toolkits.mplot3d',
        'mpl_toolkits.mplot3d.art3d',
        
        # Tkinter
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        
        # STL (if available)
        'stl',
        'stl.mesh',
    ],
    'excludes': [
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'wx', 'gtk',
        'matplotlib.tests', 'numpy.tests', 'sympy.tests',
        'tkinter.test',
    ],
    'plist': {
        'CFBundleName': 'VolumeCalculator',
        'CFBundleDisplayName': 'Volume of Revolution Calculator',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.volumecalculator.app',
        'NSHumanReadableCopyright': '© 2024 Volume Calculator',
        'CFBundleDevelopmentRegion': 'English',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
