import pathlib
import os

# Dimensiones
WIDTH = 600
HEIGHT = 500

# Archivos
"""
BASE_DIR = pathlib.Path('.').absolute()
ICON_DIR = BASE_DIR / 'icons'

# Imagenes
BULBASAUR_ICON = ICON_DIR / 'bulbasaur.png'
METAPOD_ICON = ICON_DIR / 'metapod.png'
PIDGEY_ICON = ICON_DIR / 'pidgey.png'
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, 'icons')

BULBASAUR_ICON = os.path.join(ICON_DIR, 'bulbasaur.png')
METAPOD_ICON = os.path.join(ICON_DIR, 'metapod.png')
PIDGEY_ICON = os.path.join(ICON_DIR, 'pidgey.png')