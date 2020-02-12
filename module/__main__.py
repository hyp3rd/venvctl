"""DO NOT REMOVE THIS."""

# import sys
import os
from pathlib import Path
from .main.venvctl import VenvCtl

if __name__ == '__main__':
    config_file: Path = Path(f'{os.getcwd()}/module/tests/config/venvs.json')
    VenvCtl(
        config_file=config_file).run()
