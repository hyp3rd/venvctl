"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

Configutils unit testing.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import unittest
from ..utils import configutils


class TestMethods(unittest.TestCase):
    """Configutils unit testing class."""

    def setUp(self) -> None:
        """Test setup."""
        self.valid_config = [{
            "name": "base",
            "packages": [
                "docker==4.1.0",
                "cryptography==2.7",
                "whichcraft==Í0.5.2"
            ]
        }, {
            "name": "ansible_2_6",
            "parent": "base",
            "packages": [
                "ansible==2.6",
                "identify==1.4.11"
            ]
        }, {
            "name": "ansible_2_7",
            "parent": "base",
            "packages": [
                "ansible==2.7"
            ]
        }, {
            "name": "ansible_2_9",
            "parent": "base",
            "packages": [
                "ansible==2.9"
            ]
        }, {
            "name": "ansible_2_9_networking",
            "parent": "ansible_2_9",
            "packages": [
                "websocket-client==0.56.0",
                "urllib3==1.24.1",
                "tox==3.12.1"
            ]
        }]

        self.invalid_config_item_parent = [{
            "name": "base",
            "packages": [
                "docker==4.1.0",
                "cryptography==2.7",
                "whichcraft==0.5.2"
            ]
        }, {
            "name": "ansible_2_6",
            "parent": "whatever",
            "packages": [
                "ansible==2.6",
                "identify==1.4.11"
            ]
        }, {
            "name": "ansible_2_7",
            "parent": "base",
            "packages": [
                "ansible==2.7"
            ]
        }, {
            "name": "ansible_2_9",
            "parent": "base",
            "packages": [
                "ansible==2.9"
            ]
        }, {
            "name": "ansible_2_9_networking",
            "parent": "ansible_2_9",
            "packages": [
                "websocket-client==0.56.0",
                "urllib3==1.24.1",
                "tox==3.12.1"
            ]
        }]

        self.invalid_config_type = {
            "venvs": [
                {
                    "name": "test",
                    "packages": []
                }
            ]}

        self.invalid_config_item_prop = [
            {
                "whatever": "test",
                "packages": []
            }
        ]

        self.invalid_config_item_prop_type = [{
            "name": False,
            "packages": []}]

        self.invalid_config_item_type = ["a string"]

    def test_valid_config(self) -> None:
        """Assert that the config is valid."""
        self.assertTrue(configutils.validate_config(self.valid_config))

    def test_invalid_config_type(self) -> None:
        """Assert that the config type is valid."""
        with self.assertRaises(AssertionError) as error:
            configutils.validate_config(self.invalid_config_type)
        self.assertEqual(
            configutils.ERRORS["INVALID_CONFIG_OBJECT_TYPE"],
            str(error.exception))

    def test_invalid_config_item_prop(self) -> None:
        """Assert that the config items properties valid."""
        with self.assertRaises(AssertionError) as error:
            configutils.validate_config(self.invalid_config_item_prop)
        self.assertEqual(
            configutils.ERRORS["INVALID_ITEM_KEY"].replace(
                "__KEY__", "whatever"),
            str(error.exception))

    def test_invalid_config_item_prop_type(self) -> None:
        """Assert that the config items property types are valid."""
        with self.assertRaises(AssertionError):
            configutils.validate_config(self.invalid_config_item_prop_type)

    def test_invalid_config_item_type(self) -> None:
        """Assert that the config items type is valid."""
        with self.assertRaises(AssertionError) as error:
            configutils.validate_config(self.invalid_config_item_type)
        self.assertEqual(
            configutils.ERRORS["INVALID_CONFIG_ITEM_TYPE"],
            str(error.exception))

    def test_invalid_config_item_parent(self) -> None:
        """Assert that the defined parents are valid."""
        with self.assertRaises(AssertionError) as error:
            configutils.validate_config(self.invalid_config_item_parent)
        self.assertEqual(
            configutils.ERRORS["INVALID_ITEM_PARENT"].replace(
                "__KEY__", "whatever"),
            str(error.exception))


if __name__ == '__main__':
    unittest.main()
