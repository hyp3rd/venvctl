"""
THIS SOFTWARE IS PROVIDED AS IS
and under GNU General Public License. <https://www.gnu.org/licenses/gpl-3.0.en.html>
USE IT AT YOUR OWN RISK.

PipHyperd unit testing.

The module is published on PyPi <https://pypi.org/project/piphyperd/>.

The code is available on GitLab <https://gitlab.com/hyperd/piphyperd>.
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

    """
    PipHyperd unit testing class
    """

    def setUp(self):
        """
        tests setup
        """
        self.venvctl = VenvCtl(config_file="/Users/dy14uc/Developer/gitlab.com/venvctl/module/main/tests/config/venvs.json")

    def tearDown(self):
        """
        Remove test venv after testing
        """
        self.wiper(self.venvctl.base_venv_path)

    def test_is_not_none(self):
        """
        Assert that PipHyperd is not None
        """
        self.assertIsNotNone(self.venvctl)

    def test_all(self):
        self.venvctl.run()

        test = os.path.isdir(self.venvctl.base_venv_path)

        self.assertTrue(test)

    @staticmethod
    def wiper(folder):
        """
        Helper function to clean up folders generated during the tests
        """
        if os.path.isdir(folder):
            shutil.rmtree(folder)


if __name__ == '__main__':
    unittest.main()
