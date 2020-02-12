"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

VenvCtl unit testing.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import unittest
import sys
import os
import shutil
from pathlib import Path

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PATH not in sys.path:
    sys.path.insert(1, PATH)
    from venvctl import VenvCtl
del PATH


class TestMethods(unittest.TestCase):
    """VenvCtl unit testing class."""

    @staticmethod
    def get_config_file() -> Path:
        """Return the config file path."""
        return Path(f'{os.getcwd()}/module/main/tests/config/venvs.json')

    def setUp(self):
        """Test setup."""
        self.venvctl = VenvCtl(
            config_file=self.get_config_file())

    def tearDown(self):
        """Remove test venv after testing."""
        self.wiper(self.venvctl.base_venv_path)

    def test_is_not_none(self):
        """Assert that venvctl is not None."""
        self.assertIsNotNone(self.venvctl)

    def test_create_all(self):
        """Assert that base_venv_path exists."""
        self.venvctl.run()

        test = os.path.isdir(self.venvctl.base_venv_path)
        self.assertTrue(test)

    def test_packages_status(self):
        """Assert that the expected packages are listed in each venv."""
        config = self.venvctl.get_config()

        _, regulars_venvs, networking_venvs = self.venvctl.parse_venvs(
            config)
        venv_base_path = f'{os.getcwd()}/python-venvs'
        for venv in regulars_venvs:
            pip_freeze_report, _, _ = self.venvctl.venv_audit(
                f'{venv_base_path}/{venv["name"]}')
            for package in venv['packages']:
                self.assertIn(package, pip_freeze_report)

        for venv in networking_venvs:
            pip_freeze_report, _, _ = self.venvctl.venv_audit(
                f'{venv_base_path}/{venv["name"]}')
            for package in venv['packages']:
                self.assertIn(package, pip_freeze_report)

    @staticmethod
    def wiper(folder):
        """Clean up folders generated during the tests."""
        if os.path.isdir(folder):
            shutil.rmtree(folder)


if __name__ == '__main__':
    unittest.main()
