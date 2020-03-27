"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import ast
from typing import Any
import click


class PythonLiteralOption(click.Option):
    """PythonLiteralOption class."""

    def type_cast_value(self, ctx: Any, value: str) -> Any:
        """Parse and return complex click options like '["ansible", "tox"]'."""
        try:
            return ast.literal_eval(value)
        except Exception:
            raise click.BadParameter(value)
