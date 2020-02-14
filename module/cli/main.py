"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

from pathlib import Path
import os
import sys
from typing import Optional
import click
from ..main.venvctl import VenvCtl


def getversion() -> str:
    """Get version from variables file."""
    varsfile = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..', 'variables'))
    version = """
    Could not determine version.
    Are you sure a `variables` file exists in the root folder?
    """
    if os.path.isfile(varsfile):
        try:
            with open("variables", "r") as file:
                variables = file.read().strip().split("\n")
            for variable in variables:
                key, value = variable.split("=")
                if key == "VERSION":
                    version = value
                    break
        except FileNotFoundError:
            pass
    return version


@click.version_option(version=getversion())
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
