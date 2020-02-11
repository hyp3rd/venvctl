"""
DO NOT REMOVE THIS
"""

import os
import sys


PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './main'))
if not PATH in sys.path:
    sys.path.insert(1, PATH)
    from .main.venvctl import VenvCtl
del PATH
