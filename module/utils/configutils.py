"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

from typing import Any, Dict

ERRORS = {
    "INVALID_CONFIG_OBJECT_TYPE": "The configuration object must be a list",
    "INVALID_CONFIG_ITEM_TYPE": "The configuration items must be dicts",
    "INVALID_ITEM_KEY": "Invalid configuration item key: \"__KEY__\"",
    "INVALID_ITEM_KEY_TYPE": """
    Invalid configuration item key type. \"__KEY__\" should be \"__TYPE__\"
    """,
    "INVALID_ITEM_PARENT": "Invalid configuration item parent: \"__KEY__\""
}

def valid_properties() -> Dict[Any, Any]:
    """Valid configuration item properties and types."""
    return {
        "name": str,
        "parent": str,
        "packages": list
    }

def get_item_by_name(config: list, name: str) -> Any:
    """
    Search all virtual environments.

    Returns the one with a matching `name` property.
    """
    return next((item for item in config if item["name"] == name), None)

def validate_config(config: Any) -> bool:
    """Validate configuration file."""

    props = valid_properties()

    # Ensure that the config object is a list
    assert isinstance(config, list), ERRORS["INVALID_CONFIG_OBJECT_TYPE"]

    for item in config:
        # Ensure that config items are dictionaries
        assert isinstance(item, dict), ERRORS["INVALID_CONFIG_ITEM_TYPE"]
        for key, value in item.items():
            # Ensure config item key is valid
            assert key in props, ERRORS["INVALID_ITEM_KEY"].replace("__KEY__", key)
            assert isinstance(value, props[key]), ERRORS["INVALID_ITEM_PARENT"].replace("__KEY__", key).replace("__TYPE__", str(props[key]))
            
            # Ensure that if defined, the parent exists
            if key == "parent":
                assert get_item_by_name(config, value) is not None, ERRORS["INVALID_ITEM_PARENT"].replace("__KEY__", value)

    return True
