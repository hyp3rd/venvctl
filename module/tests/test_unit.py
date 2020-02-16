"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

VenvCtl unit testing.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import unittest
import os
from pathlib import Path
from typing import Any
import glob
from binaryornot.check import is_binary
from ..main.venvctl import VenvCtl
from ..utils import utils


class TestMethods(unittest.TestCase):
    """VenvCtl unit testing class."""

    @staticmethod
    def get_config_file() -> Path:
        """Return the config file path."""
        return Path(f'{os.getcwd()}/module/tests/config/venvs.json')

    @staticmethod
    def get_venv_base_path() -> Path:
        """Return the venv base folder path."""
        return Path(f'{os.getcwd()}/python-venvs')

    def get_venvs_config(self) -> Any:
        """Get the venvs config file."""
        return self.venvctl.get_config()

    def setUp(self) -> None:
        """Test setup."""
        self.venvctl = VenvCtl(
            config_file=self.get_config_file())

    def test_a_is_not_none(self) -> None:
        """Assert that venvctl is not None."""
        self.assertIsNotNone(self.venvctl)

    def test_b_config_is_not_none(self) -> None:
        """Assert that the config file is not None."""
        self.assertIsNotNone(self.get_config_file())

    def test_c_create_all(self) -> None:
        """Assert that base_venv_path exists."""
        self.venvctl.run()

        test = os.path.isdir(self.get_venv_base_path())
        self.assertTrue(test)

    def test_d_venv_integrity(self) -> None:
        """Assert that each venv contains the expected packages."""
        for venv in self.get_venvs_config():
            pip_freeze_report, _, _ = self.venvctl.audit(
                Path(f'{self.get_venv_base_path()}/{venv["name"]}'))
            for package in venv['packages']:
                self.assertIn(package, pip_freeze_report)

    def test_e_activate_fix(self) -> None:
        """Assert that the bash activate fix is applied."""
        for venv in self.get_venvs_config():
            current_path = f'{self.get_venv_base_path()}/{venv["name"]}'
            with open(f'{current_path}/bin/activate', 'r') as file:
                verify = (utils.Helpers().get_bash_activation_fix()
                          in file.read())

                self.assertTrue(verify)

    def test_f_shebang_fix(self) -> None:
        """Assert that the shebang fix is applied."""
        for venv in self.get_venvs_config():
            target_path = f'{self.get_venv_base_path()}/{venv["name"]}/bin'
            for child in glob.glob(
                    f'{target_path}/**/easy*', recursive=True):
                if os.path.isdir(child) or is_binary(str(child)):
                    pass
                else:
                    with open(child, 'r') as python_file:
                        verify = (utils.Helpers().get_shebang_fix()
                                  in python_file.read())
                        self.assertTrue(verify, "The shebang fix is present.")


if __name__ == '__main__':
    unittest.main()