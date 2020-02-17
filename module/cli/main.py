"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

from pathlib import Path
import sys
from typing import Optional, Dict, List, Any
import click
from ..main.venvctl import VenvCtl
from ..main.release import __version__


def version_info() -> Dict[str, str]:
    """Return full venvctl version info."""
    venvctl_version_string = __version__
    venvctl_version = venvctl_version_string.split()[0]
    venvctl_versions: List[Any] = venvctl_version.split('.')
    # pylint: disable=consider-using-enumerate
    for counter in range(len(venvctl_versions)):
        if venvctl_versions[counter] == "":
            venvctl_versions[counter] = 0
        try:
            venvctl_versions[counter] = int(venvctl_versions[counter])
        except Exception:  # pylint: disable=broad-except
            pass
    if len(venvctl_versions) < 3:
        for counter in range(len(venvctl_versions), 3):
            venvctl_versions.append(0)
    return {'string': venvctl_version_string.strip(),
            'full': venvctl_version,
            'major': venvctl_versions[0],
            'minor': venvctl_versions[1],
            'revision': venvctl_versions[2]}


@click.version_option(version=version_info()["string"])
@click.group()
def cli() -> None:
    """Implement the default CLI group."""


@cli.command()
@click.option('--config', required=True,
              help='Path to the virtual envs configuration file')
@click.option('--out', required=False, help='Virtual envs output folder')
@click.option('--python', required=False, help='The path to the python binary')
def generate(config: str,
             out: Optional[str] = None,
             python: Optional[str] = None) -> None:
    """
    Generate command.

    Creates virtual envs and corresponding reports,
    based on a predefined configuration.
    """
    config_file = Path(config)
    output_dir = None if out is None else Path(out)
    python_binary = Path(sys.executable) if python is None else Path(python)
    VenvCtl(config_file=config_file,
            python_binary=python_binary,
            output_dir=output_dir).run()


def run() -> None:
    """Run the CLI."""
    try:
        cli()  # pylint: disable=no-value-for-parameter
    except RuntimeError as rerr:
        click.echo(str(rerr))
    except TypeError as terr:
        click.echo(str(terr))
    except click.ClickException as cerr:
        cerr.show()


if __name__ == "__main__":
    run()
