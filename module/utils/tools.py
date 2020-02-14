"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

Tools is a helper object.
This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import os
import tarfile
import contextlib
import io
import re
import glob
from pathlib import Path
from binaryornot.check import is_binary


class Tools:
    """Tools and Utils."""

    @staticmethod
    def __get_shebang_fix() -> str:
        """FIX: the shebang in python files."""
        return '#!/usr/bin/env python'

    @classmethod
    def shebang_fixer(cls, venv_path: str, target_dir: str) -> None:
        """Fix the shebang path in any python file."""
        target_path = f'{venv_path}/{target_dir}'

        for child in glob.glob(
                f'{target_path}/**/*', recursive=True):
            if os.path.isdir(child) or is_binary(str(child)):
                pass
            else:
                with open(child, 'r') as python_file:
                    content = python_file.read()

                content = re.sub(r'#!(.*)/python.*',
                                 cls.__get_shebang_fix(), content)

                with open(child, 'w') as python_file:
                    python_file.write(content)

    @staticmethod
    def packer(venv_path: Path, venv_name: str) -> str:
        """Generate a tarball of the specified virtual environment."""
        builds_path = "{}/builds".format(venv_path)
        if not os.path.isdir(builds_path):
            os.mkdir(builds_path)

        with tarfile.open("{}/{}.tar.gz".format(builds_path, venv_name),
                          "w:gz") as tar:
            tar.add("{}/{}".format(venv_path, venv_name),
                    arcname=os.path.basename(
                        "{}/{}".format(venv_path, venv_name)), recursive=True)

            tarball_content = io.StringIO()

            with contextlib.redirect_stdout(tarball_content):
                tar.list()

            output = tarball_content.getvalue()
            return f'{output}'
