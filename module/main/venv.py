"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

Venv serializeble / deserializable object

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

from typing import List, Dict, Any

__metaclass__ = type  # pylint: disable=invalid-name


class Venv():  # pylint: disable=too-few-public-methods
    """Represent a virtual environment."""

    def __init__(self, name: str,
                 packages: List[str]):
        """Describe a venv through its configuration."""
        self.name = name
        self.packages = packages

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Any:
        """Object serialization helper."""
        name = str(map(cls.from_json, data["name"]))
        packages = list(map(cls.from_json, data["packages"]))
        return cls(name, packages)
