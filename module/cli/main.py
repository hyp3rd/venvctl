"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

from pathlib import Path
import sys
import logging
from typing import Optional, Dict, List, Any
import click
from .options import PythonLiteralOption
from ..main.venvctl import VenvCtl
from ..security.bandit import BnaditScanner
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
            logging.error("I was unable to determine the version")
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
    Generate virtual environments in batch, based on a config file.

    Creates virtual environments and corresponding reports,
    based on a predefined configuration.
    """
    config_file = Path(config)
    output_dir = None if out is None else Path(out)
    python_binary = Path(sys.executable) if python is None else Path(python)

    VenvCtl(config_file=config_file,
            python_binary=python_binary,
            output_dir=output_dir).run()


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--name', required=True,
              help='Name of the virtual env')
@click.option('--packages', required=True, cls=PythonLiteralOption,
              default=[],
              help='Packages to install, e.g.: \'["ansible", "tox"]\'')
@click.option('--out', required=False, help='Virtual env output folder')
def create(name: str, packages: List[str],
           out: Optional[str] = None) -> None:
    """
    Create a virtual environment.

    Creates a virtual environment and corresponding reports,
    initializing it with a list of packages.
    """
    venv_name = name
    output_dir = None if out is None else Path(out)
    packages_list = packages

    VenvCtl.create_venv(name=venv_name, packages=packages_list,
                        output_dir=output_dir)


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--target', required=True,
              help='Target path to scan')
def bandit(target: Path) -> None:
    """
    Scan a target path with Bandit.

    Processes a target path with Bandit and generates corresponding reports
    in Markdown format.
    """
    target_path = target
    BnaditScanner.run(target_path)


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
