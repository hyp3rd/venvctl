"""DO NOT REMOVE THIS."""

from pathlib import Path
from typing import Optional
import click
from ..main.venvctl import VenvCtl


class Cli:
    """CLI class"""

    @click.version_option()
    @click.group()
    def cli(self):
        """Default CLI group."""


    @cli.command()
    @click.option('--config', required=True,
                  help='The path to the virtual environments configuration file')
    @click.option('--out', required=False, help='The virtual environments output folder')
    @click.option('--python', required=False, help='The path to the python binary')
    def generate(self, config: str,
                 out: Optional[str] = None,
                 python: Optional[str] = None) -> None:
        """
        Generate virtual environments
        and corresponding reports, based on a predefined configuration.
        """
        config_file = Path(config)
        output_dir = None if out is None else Path(out)
        python_binary = None if python is None else Path(python)
        VenvCtl(config_file=config_file,
                python_binary=python_binary,
                output_dir=output_dir).run()

    def run(self):
        """Run the CLI."""
        try:
            self.cli()  # pylint: disable=no-value-for-parameter
        except RuntimeError as rerr:
            click.echo(str(rerr))
        except TypeError as terr:
            click.echo(str(terr))
        except click.ClickException as cerr:
            cerr.show()

