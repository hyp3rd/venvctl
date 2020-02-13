"""DO NOT REMOVE THIS."""

from pathlib import Path
from typing import Optional
import click
from .main.venvctl import VenvCtl


@click.command()
@click.option('--config', help='The path to the virtual environments configuration file')
@click.option('--out', required=False, help='The virtual environments output folder')
@click.option('--python', required=False, help='The path to the python binary')
def run(config: str,
        out: Optional[str] = None,
        python: Optional[str] = None) -> None:
    """
    A program that generates virtual environments
    and corresponding reports, based on a predefined configuration.
    """
    config_file = Path(config)
    output_dir = Path(out) if out else None
    VenvCtl(config_file=config_file,
            python_binary=python,
            output_dir=output_dir).run()


if __name__ == '__main__':
    run()  # pylint: disable=no-value-for-parameter
