"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import os
import sys
from subprocess import Popen, PIPE, CalledProcessError   # nosec
from pathlib import Path
from typing import Any, Dict, Tuple
from ..utils import reports


class BnaditScanner():  # pylint: disable=too-few-public-methods
    """Bandit wrapper class."""

    @classmethod
    def run(cls, venvs_path: Path) -> Tuple[Any, int]:
        """Run a bandit scan against a given venv."""
        try:
            print(f'Bandit is scanning {venvs_path}')

            stdout = ""
            # Bandit check disabled:
            # https://github.com/PyCQA/bandit/issues/373
            with Popen([str(Path(sys.executable)),
                        "-m", "bandit",
                        "-r", venvs_path], stdout=PIPE, bufsize=1,
                       universal_newlines=True) as process:
                for line in process.stdout:   # type: ignore
                    stdout += line
                    print(line, end='')   # nosec

            sys.stdout.flush()
            scan_dir = os.path.basename(os.path.dirname(str(venvs_path)))
            cls.__generate_bandit_report(venvs_path, stdout,
                                         f'bandit-{scan_dir}',
                                         process.returncode)

            return stdout, process.returncode

        except CalledProcessError as called_process_error:
            print("*******************************")
            print("**************ERR**************")
            print("*******************************")
            raise called_process_error

    @staticmethod
    def __generate_bandit_report(venvs_path: Path, bandit_report: Any,
                                 report_name: str,
                                 exitcode: int) -> None:
        """Run a bandit scan against a given venv."""
        reports_map: Dict[str, str] = {
            "Bandit Report": bandit_report,
        }

        reports.Reports().generate_reports(
            Path(f'{venvs_path}/reports'),
            report_name, reports_map, exitcode)
