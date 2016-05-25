# setup.py
from distutils.core import setup
import py2exe
 
setup(
    windows = [
        {
            "script": "clicker.py",
            "icon_resources": [(1, "mouse.ico")]
        }
    ],
)