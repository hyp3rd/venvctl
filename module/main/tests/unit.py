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

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not PATH in sys.path:
    sys.path.insert(1, PATH)
    from venvctl import VenvCtl
del PATH


class TestMethods(unittest.TestCase):
    """VenvCtl unit testing class."""

    def setUp(self):
        """Tests setup."""
        self.venvctl = VenvCtl(
            config_file=f'{os.getcwd()}/module/main/tests/config/venvs.json')

    def tearDown(self):
        """Remove test venv after testing."""
        self.wiper(self.venvctl.base_venv_path)

    def test_is_not_none(self):
        """Assert that venvctl is not None."""
        self.assertIsNotNone(self.venvctl)

    def test_all(self):
        """Assert that base_venv_path exists."""
        self.venvctl.run()

        test = os.path.isdir(self.venvctl.base_venv_path)
        self.assertTrue(test)

    @staticmethod
    def wiper(folder):
        """Clean up folders generated during the tests."""
        if os.path.isdir(folder):
            shutil.rmtree(folder)


if __name__ == '__main__':
    unittest.main()
