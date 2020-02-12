"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

Reports is a python object to dinamically generate markdown reports.
This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import time
from pathlib import Path
from typing import Dict, List
from collections import UserDict
from markd import Markdown


class Reports:
    """Reports helper."""

    @staticmethod
    def report_builder(report_title: str, report_body: str) -> UserDict:
        """Generate a report object."""
        report: UserDict = UserDict()
        report['title'] = report_title
        report['output'] = report_body

        return report

    @staticmethod
    def generate_report(reports_path: Path, venv_name: str,
                        reports: List[UserDict], exitcode: int):
        """Generate markdown reports."""
        generated_at = time.strftime("%Y:%M:%d - %H:%M")

        markd = Markdown()

        markd.add_header(f'{venv_name} {generated_at}')

        markd.add_text("Process exited with code {}".format(exitcode))

        for report in reports:
            if report['output']:
                markd.add_header(report["title"], 2)
                markd.add_code(report["output"])

        markd.save(f'{reports_path}/{venv_name}.md')

    @classmethod
    def generate_reports(cls, reports_path: Path, venv_name: str,
                         reports: Dict[str, str], exitcode: int):
        """Parse and generate reports."""
        all_reports = list()
        for key, val in reports.items():
            all_reports.append(cls.report_builder(
                key, val))

        cls.generate_report(
            Path(f'{reports_path}/reports'), venv_name, all_reports, exitcode)
