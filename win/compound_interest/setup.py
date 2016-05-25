# setup.py
from distutils.core import setup
import py2exe
 
setup(
    windows = [
        {
            "script": "interest.py",
            "icon_resources": [(1, "money.ico")]
        }
    ],
)