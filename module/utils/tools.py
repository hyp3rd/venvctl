"""
THIS SOFTWARE IS PROVIDED AS IS
and under GNU General Public License. <https://www.gnu.org/licenses/gpl-3.0.en.html>
USE IT AT YOUR OWN RISK.

IO is a python object helper for IO operations.

This module is part of VenvCtl, published on PyPi <https://pypi.org/project/venvctl/>.

The code is available on GitLab <https://gitlab.com/hyperd/venvctl>.
"""

import os
import tarfile
import contextlib
import io
from pathlib import Path


class Tools:
    """
    Tools and Utils.
    """

    @staticmethod
    def packer(venv_path: Path, venv_name: str) -> str:
        """ generates a tarball of the specified virtual environment """
        builds_path = "{}/builds".format(venv_path)
        if not os.path.isdir(builds_path):
            os.mkdir(builds_path)

        with tarfile.open("{}/{}.tar.gz".format(builds_path, venv_name), "w:gz") as tar:
            tar.add("{}/{}".format(venv_path, venv_name), arcname=os.path.basename(
                "{}/{}".format(venv_path, venv_name)), recursive=True)

            tarball_content = io.StringIO()

            with contextlib.redirect_stdout(tarball_content):
                tar.list()

            output = tarball_content.getvalue()
            return f'{output}'
