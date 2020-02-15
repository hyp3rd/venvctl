"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

from typing import Any

def valid_properties() -> dict:
    """Valid configuration item properties and types."""
    return {
        "name": str,
        "parent": str,
        "packages": list
    }

def get_item_by_name(config: list, name: str) -> dict:
    """
    Search all virtual environments.

    Returns the one with a matching `name` property.
    """
    return next((item for item in config if item["name"] == name), None)

def validate_config(config: Any) -> None:
    """Validate configuration file."""

    props = valid_properties()

    # Ensure that the config object is a list
    assert isinstance(config, list), "The configuration object must be a list"

    for item in config:
        # Ensure that config items are dictionaries
        assert isinstance(item, dict), "The configuration items must be dicts"
        for key, value in item.items():
            # Ensure config item key is valid
            assert key in props, f'Invalid configuration item key: {key}'
            assert isinstance(value, props[key]), f'''
            Invalid configuration item key type. "{key}" should be {props[key]}'
            '''
            # Ensure that if defined, the parent exists
            if key == "parent":
                assert get_item_by_name(config, value) is not None, f'''
                Invalid configuration item parent: {value}
                '''
