"""
DO NOT REMOVE THIS
"""

# import sys
import os
from pathlib import Path
from .main.venvctl import VenvCtl

if __name__ == '__main__':
    VenvCtl(
        config_file=Path(f'{os.getcwd()}/module/tests/config/venvs.json')).run()
