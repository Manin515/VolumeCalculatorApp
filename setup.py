"""
setup.py for Volume of Revolution Calculator (macOS)
Usage: python setup.py py2app
"""

from setuptools import setup
import os

APP = ['src/volume_calculator_gui.py']
DATA_FILES = []

# Comprehensive options for py2app
OPTIONS = {
    'argv_emulation': False,  # Set to False for better Tkinter compatibility
    'packages': [
        'numpy', 
        'matplotlib', 
        'sympy',
        'tkinter',
        'mpl_toolkits',
        'stl',
        'pkg_resources'
    ],
    'includes': [
        # NumPy
        'numpy',
        'numpy.core._methods',
        'numpy.lib.format',
        
        # Matplotlib
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.backends.backend_tk',
        'matplotlib.pyplot',
        'matplotlib.figure',
        'matplotlib.axes',
        
        # 3D plotting
        'mpl_toolkits',
        'mpl_toolkits.mplot3d',
        'mpl_toolkits.mplot3d.art3d',
        
        # SymPy
        'sympy',
        'sympy.*',
        
        # STL
        'stl',
        'stl.mesh',
        
        # Tkinter
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox'
    ],
    'excludes': [
        'PyQt4', 'PyQt5', 'PySide', 'PySide2', 'wx',
        'gtk', 'curses', 'email', 'pdb', 'unittest',
        'multiprocessing', 'test', 'lib2to3',
        'pydoc_data', 'distutils', 'setuptools',
    ],
    'resources': [
        # Include any additional resource files if needed
    ],
    'frameworks': [],
    'plist': {
        'CFBundleName': 'VolumeCalculator',
        'CFBundleDisplayName': 'Volume of Revolution Calculator',
        'CFBundleGetInfoString': "Calculates volumes of revolution with 3D visualization",
        'CFBundleIdentifier': "com.volumecalculator.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "© 2024 Volume Calculator",
        'CFBundleDevelopmentRegion': 'English',
        'NSPrincipalClass': 'NSApplication',
        'LSMinimumSystemVersion': '10.14.0',  # macOS Mojave or later
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeExtensions': ['stl'],
                'CFBundleTypeName': 'STL File',
                'CFBundleTypeRole': 'Viewer',
            }
        ]
    },
    'optimize': 2,
}

setup(
    name='Volume Calculator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)