"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

from __future__ import (absolute_import, division, print_function)
from typing import Any, Dict, List, Tuple
from pathlib import Path
import json
import errno
import os
from ..utils import utils
from ..main.venv import Venv

ERRORS = {
    "INVALID_CONFIG_OBJECT_TYPE": "The configuration object must be a list",
    "INVALID_CONFIG_ITEM_TYPE": "The configuration items must be dicts",
    "INVALID_ITEM_KEY": "Invalid configuration item key: \"__KEY__\"",
    "INVALID_ITEM_KEY_TYPE": """
    Invalid configuration item key type. \"__KEY__\" should be \"__TYPE__\"
    """,
    "INVALID_ITEM_PARENT": "Invalid configuration item parent: \"__KEY__\""
}


def generate_config(name: str,
                    packages: List[str]) -> Path:
    """Generate a venv config file."""
    venv = Venv(name=name, packages=packages)
    venvs = list()
    venvs.append(venv)

    # Serializing
    data = json.dumps(venvs, default=lambda o: o.__dict__,
                      sort_keys=False, indent=4)

    # base storage dir for the config file(s)
    base_config_path = utils.Helpers.get_venvs_config_base_path()

    # ensure the base storage dir exists
    if not Path(base_config_path).is_dir():
        os.mkdir(base_config_path)

    file_path = Path(f'{base_config_path}/{name}.config.json')

    with open(file_path, 'w',
              encoding='utf-8') as config_file:
        json.dump(json.loads(data), config_file,
                  sort_keys=False, ensure_ascii=False, indent=4)

    return file_path


def get_config(config_file: Path) -> Any:
    """Get the venvs config file."""
    if config_file.exists() and config_file.is_file():
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    raise FileNotFoundError(
        errno.ENOENT, os.strerror(errno.ENOENT), config_file)


def valid_properties() -> Dict[Any, Any]:
    """Validate configuration item properties and types."""
    return {
        "name": str,
        "parent": str,
        "packages": list
    }


def get_item_by_name(config: List[Any], name: str) -> Any:
    """
    Search all virtual environments.

    Returns the one with a matching `name` property.
    """
    return next((item for item in config if item["name"] == name), None)


def validate_config(config: Any) -> Tuple[bool, str]:
    """Validate configuration file."""
    props = valid_properties()

    # Ensure that the config object is a list
    if not isinstance(config, list):
        return False, ERRORS["INVALID_CONFIG_OBJECT_TYPE"]

    for item in config:
        # Ensure that config items are dictionaries
        if not isinstance(item, dict):
            return False, ERRORS["INVALID_CONFIG_ITEM_TYPE"]
        for key, value in item.items():
            # Ensure config item key is valid
            if key not in props:
                return False, ERRORS["INVALID_ITEM_KEY"].replace(
                    "__KEY__", key)
            if not isinstance(value, props[key]):
                return False, ERRORS["INVALID_ITEM_PARENT"].replace(
                    "__KEY__", key).replace("__TYPE__", str(props[key]))

            # Ensure that if defined, the parent exists
            if key == "parent":
                if get_item_by_name(config,
                                    value) is None:
                    return False, ERRORS["INVALID_ITEM_PARENT"].replace(
                        "__KEY__", value)

    return True, "ALL TESTS PASSED"
