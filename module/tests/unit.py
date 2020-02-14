"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

VenvCtl unit testing.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import unittest
# import sys
import os
import shutil
from pathlib import Path

from ..main.venvctl import VenvCtl


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

    @staticmethod
    def get_bash_activation_fix() -> str:
        """FIX the bashvenv activation. WARNING.

        If you have any bash profile customization
        at the `cd` command, this fix will breake.
        """
        return 'VIRTUAL_ENV=$(cd $(dirname "$BASH_SOURCE"); dirname `pwd`)'

    @staticmethod
    def wiper(folder_path: Path) -> None:
        """Clean up folders generated during the tests."""
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)

    def setUp(self) -> None:
        """Test setup."""
        self.venvctl = VenvCtl(
            config_file=self.get_config_file())

    # def tearDown(self):
    #     """Remove test venv after testing."""
    #     self.wiper(self.get_venv_base_path())

    def test_a_is_not_none(self) -> None:
        """Assert that venvctl is not None."""
        self.assertIsNotNone(self.venvctl)

    def test_b_create_all(self) -> None:
        """Assert that base_venv_path exists."""
        self.venvctl.run()

        test = os.path.isdir(self.venvctl.base_venv_path)
        self.assertTrue(test)

    def test_c_activate_fix(self) -> None:
        """Assert that the bash activate fix is applied."""
        config = self.venvctl.get_config()
        _, regulars_venvs, networking_venvs = self.venvctl.parse_venvs(
            config)

        all_venvs = regulars_venvs + networking_venvs

        for venv in all_venvs:
            __path = f'{self.get_venv_base_path()}/{venv["name"]}'
            print(__path)
            with open(f'{__path}/bin/activate', 'r') as file:
                verify = (self.get_bash_activation_fix() in file.read())

                self.assertTrue(verify)

    def test_d_packages(self) -> None:
        """Assert that the expected packages are listed in each venv."""
        config = self.venvctl.get_config()

        _, regulars_venvs, networking_venvs = self.venvctl.parse_venvs(
            config)

        all_venvs = regulars_venvs + networking_venvs

        for venv in all_venvs:
            pip_freeze_report, _, _ = self.venvctl.audit(
                Path(f'{self.get_venv_base_path()}/{venv["name"]}'))
            for package in venv['packages']:
                self.assertIn(package, pip_freeze_report)


if __name__ == '__main__':
    unittest.main()
