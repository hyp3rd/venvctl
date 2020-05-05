"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

Configutils unit testing.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import unittest
from pathlib import Path
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
        valid, _ = configutils.validate_config(self.valid_config)
        self.assertTrue(valid)

    def test_invalid_config_type(self) -> None:
        """Assert that the config type is valid."""
        valid, message = configutils.validate_config(self.invalid_config_type)
        self.assertFalse(valid)

        self.assertEqual(
            configutils.ERRORS["INVALID_CONFIG_OBJECT_TYPE"],
            str(message))

    def test_invalid_config_item_prop(self) -> None:
        """Assert that the config items properties valid."""
        valid, _ = configutils.validate_config(
            self.invalid_config_item_prop)
        self.assertFalse(valid)

        valid, message = configutils.validate_config(
            self.invalid_config_item_prop)
        self.assertFalse(valid)
        self.assertEqual(
            configutils.ERRORS["INVALID_ITEM_KEY"].replace(
                "__KEY__", "whatever"),
            message)

    def test_invalid_config_item_prop_type(self) -> None:
        """Assert that the config items property types are valid."""
        valid, _ = configutils.validate_config(
            self.invalid_config_item_prop_type)
        self.assertFalse(valid)

    def test_invalid_config_item_type(self) -> None:
        """Assert that the config items type is valid."""
        valid, message = configutils.validate_config(
            self.invalid_config_item_type)
        self.assertFalse(valid)

        self.assertEqual(
            configutils.ERRORS["INVALID_CONFIG_ITEM_TYPE"],
            message)

    def test_invalid_config_item_parent(self) -> None:
        """Assert that the defined parents are valid."""
        valid, message = configutils.validate_config(
            self.invalid_config_item_parent)
        self.assertFalse(valid)

        self.assertEqual(
            configutils.ERRORS["INVALID_ITEM_PARENT"].replace(
                "__KEY__", "whatever"),
            message)

    def test_config_is_generated(self) -> None:
        """Assert that a configuration file is generated and is valid."""
        packages = [
            "piphyperd==1.5.5",
            "markd==0.1.19",
            "click==7.0",
            "binaryornot==0.4.4"
        ]
        config_file = configutils.generate_config(
            name="test", packages=packages)

        self.assertTrue(Path(config_file).is_file(), "{config} exists.")

        config = configutils.get_config(config_file)
        valid = configutils.validate_config(
            config)
        self.assertTrue(valid, "{config} is valid")


if __name__ == '__main__':
    unittest.main()
