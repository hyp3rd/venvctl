"""
DO NOT REMOVE THIS
"""

import os
from venvctl import VenvCtl

if __name__ == '__main__':
    VenvCtl(
        config_file=f'{os.getcwd()}/module/main/tests/config/venvs.json').run()
