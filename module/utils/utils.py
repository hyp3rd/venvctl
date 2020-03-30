"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

Tools is a helper object.
This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""
import sys
import os
import tarfile
import contextlib
import io
import re
import glob
from pathlib import Path
from typing import List
from binaryornot.check import is_binary


class Helpers:
    """Helper class."""

    @staticmethod
    def set_envoironment() -> None:
        """Set the environment."""
        sys.tracebacklimit = 1  # Avoid Traceback leaks

    @staticmethod
    def get_venvs_config_base_path() -> Path:
        """Return the base config file path."""
        return Path(f'{os.getcwd()}/venvs-config')

    @staticmethod
    def get_shebang_fix() -> str:
        """FIX: the shebang in python files."""
        return '#!/usr/bin/env python'

    @staticmethod
    def get_bash_activation_fix() -> str:
        """FIX the bashvenv activation. WARNING.

        If you have any bash profile customization
        at the `cd` command, this fix will break.
        """
        return 'VIRTUAL_ENV=$(cd $(dirname "$BASH_SOURCE"); dirname `pwd`)'

    @classmethod
    def bash_activation_fixer(cls, venv_path: Path) -> None:
        """Apply fix to /bin/activate."""
        with open(f'{venv_path}/bin/activate', 'r') as activate_file:
            content = activate_file.read()

        content = re.sub(r'VIRTUAL_ENV\s*=(.*)',
                         cls.get_bash_activation_fix(), content)

        with open(f'{venv_path}/bin/activate', 'w') as activate_file:
            activate_file.write(content)

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
                                 cls.get_shebang_fix(), content)

                with open(child, 'w') as python_file:
                    python_file.write(content)

    @staticmethod
    def detect_python_binary(venv_path: Path) -> Path:
        """Detect the python binary installed in a given virtual env."""
        python_version_paths: List[str] = [
            f"{venv_path}/bin/python",
            f"{venv_path}/bin/python2",
            f"{venv_path}/bin/python3"
        ]

        for python_version in python_version_paths:
            version_selected = Path(python_version)
            if version_selected.is_file():
                return version_selected

        raise FileNotFoundError()

    @staticmethod
    def packer(venv_path: Path, venv_name: str) -> str:
        """Generate a tarball of the specified virtual environment."""
        builds_path = "{}/builds".format(venv_path)
        build_tarball_path = "{}/{}.tar.gz".format(builds_path, venv_name)

        if not Path(builds_path).is_dir():
            os.mkdir(builds_path)

        if Path(builds_path).is_file():
            os.remove(build_tarball_path)

        with tarfile.open(build_tarball_path,
                          "w:gz") as tar:
            tar.add("{}/{}".format(venv_path, venv_name),
                    arcname=os.path.basename(
                        "{}/{}".format(venv_path, venv_name)), recursive=True)

            tarball_content = io.StringIO()

            with contextlib.redirect_stdout(tarball_content):
                tar.list()

            output = tarball_content.getvalue()
            return f'{output}'
