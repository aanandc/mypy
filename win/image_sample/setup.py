# setup.py
from distutils.core import setup
import py2exe
 
setup(
    windows = [
        {
            "script": "crazy.py",
            "icon_resources": [(1, "game.ico")]
        }
    ],
)