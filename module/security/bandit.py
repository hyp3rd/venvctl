"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import sys
import subprocess   # nosec
from pathlib import Path
from typing import Any, Dict
from ..utils import reports


class BnaditScanner():  # pylint: disable=too-few-public-methods
    """Bandit wrapper class."""

    @staticmethod
    def run(venv_path: Path) -> Any:
        """Run a bandit scan against a given venv."""
        try:
            # Bandit check disabled:
            # https://github.com/PyCQA/bandit/issues/373
            process = subprocess.run(
                [str(Path(sys.executable)),
                 "-m", "bandit",
                 "-r", venv_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True, shell=False)   # nosec

            process.check_returncode()

            output = f'{process.stdout.decode("utf-8")}'
            sys.stdout.write(output)

            outerr = f'{process.stderr.decode("utf-8")}'
            sys.stderr.write(outerr)

            return output, outerr, process.returncode

        except subprocess.CalledProcessError as called_process_error:

            ex_output: str = f'Error output:\n{called_process_error.output}'
            ex_cmd: str = f'cmd:\n{called_process_error.cmd}'

            return ex_output, ex_cmd, called_process_error.returncode

    @staticmethod
    def generate_bandit_report(venvs_path: str, bandit_report: str,
                               venv_name: str,
                               exitcode: int) -> None:
        """Run a bandit scan against a given venv."""
        reports_map: Dict[str, str] = {
            "Bandit Report": bandit_report,
        }

        reports.Reports().generate_reports(
            Path(f'{venvs_path}/reports'),
            venv_name, reports_map, exitcode)
