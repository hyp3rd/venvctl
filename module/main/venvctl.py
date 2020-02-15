"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

VenvCtl is a python object to leverage virtual environments programmatically.
VenvCtl is a wrapper around virtualenv.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Any, List, Tuple, Dict, Optional
import shutil
import re
from piphyperd import PipHyperd
from ..utils import reports, utils


class VenvCtl:
    """
    VenvCtl a wrapper class around virtualenv.

    python_path -- Path to the python binary to use
    """

    def __init__(self, config_file: Path,
                 output_dir: Optional[Path] = None,
                 python_binary: Path = Path(sys.executable)) -> None:
        """
        Init the venvctl.

        config_path -- Path to the venvs config file)
        output_dir -- Directory path to output the venvs artifacts
        """
        # venvs config file
        self.config_file: Path = Path(config_file)
        # venvs base dir
        default_dir = Path(f'{os.getcwd()}/python-venvs')
        self.venvs_path: Path = Path(output_dir) if output_dir else default_dir
        # Initialize venvs
        self.venvs: List[Any] = []
        # path to the python binary to use
        self.python_binary = python_binary if python_binary else sys.executable

    @property
    def __get_bash_activation_fix(self) -> str:
        """FIX the bashvenv activation. WARNING.

        If you have any bash profile customization
        at the `cd` command, this fix will breake.
        """
        return 'VIRTUAL_ENV=$(cd $(dirname "$BASH_SOURCE"); dirname `pwd`)'

    @property
    def __get_venv_cmd(self) -> str:
        """Return virtualenv command."""
        return 'virtualenv --activators bash --copies'

    @staticmethod
    def audit(venv_path: Path) -> Tuple[str, str, str]:
        """Run audit against a specific virtual environment."""
        piphyperd = PipHyperd(python_path=Path(f'{venv_path}/bin/python3'))

        pip_freeze_report, _, _ = piphyperd.freeze()
        pip_check_report, _, _ = piphyperd.check()

        pip_outdated_report, _, _ = piphyperd.list_packages(True)

        return pip_freeze_report, pip_check_report, pip_outdated_report

    @staticmethod
    def install_packages(venv_path: Path,
                         venv_packages: List[str]) -> Tuple[str, str, int]:
        """Install packages within a specific virtual environment."""
        piphyperd = PipHyperd(
            python_path=Path(f'{venv_path}/bin/python3'))

        install_report, install_errors, exitcode = piphyperd.install(
            *venv_packages)

        # Apply shebang fix to make the venv fully portable
        utils.Helpers().shebang_fixer(str(venv_path), "bin")

        return install_report, install_errors, exitcode

    def get_config(self) -> Any:
        """Get the venvs config file."""
        with open(self.config_file, 'r') as file:
            config = json.load(file)

        return config

    def __get_venv_by_name(self, venvname: str) -> Any:
        """
        Search all virtual environments.

        Returns the one with a matching `name` property.
        """
        for venv in self.venvs:
            if venv["name"] == venvname:
                return venv
        return None

    def __create_venv(self, venv_path: Path,
                      venv_packages: List[str],
                      parent_venv_path: Optional[Path]) -> Tuple[str, str, int]:
        """Create virtual environment."""
        # If a parent is defined, clone it and install the extra packages
        if parent_venv_path is not None:
            shutil.copytree(src=parent_venv_path, dst=venv_path)
            return self.install_packages(venv_path, venv_packages)

        # Otherwise create a brand new virtual environment
        subprocess.call(
            f'{self.python_binary} -m {self.__get_venv_cmd} {venv_path}',
            shell=True)

        install_report, install_errors, exitcode = self.install_packages(
            venv_path, venv_packages)

        # Apply fix to /bin/activate
        with open(f'{venv_path}/bin/activate', 'r') as activate_file:
            content = activate_file.read()

        content = re.sub(r'VIRTUAL_ENV\s*=(.*)',
                         self.__get_bash_activation_fix, content)

        with open(f'{venv_path}/bin/activate', 'w') as activate_file:
            activate_file.write(content)

        return install_report, install_errors, exitcode

    def __generate_venv(self, venv: Any) -> None:
        venv_path = Path(f'{self.venvs_path}/{venv["name"]}')
        parent_venv_path = None

        if "parent" in venv:
            parent_venv_path = Path(f'{self.venvs_path}/{venv["parent"]}')

        install_report, install_errors, exitcode = self.__create_venv(
            venv_path, venv["packages"], parent_venv_path)

        pip_freeze_report, pip_check_report, pip_outdated_report = self.audit(
            Path(f'{self.venvs_path}/{venv["name"]}'))

        build_report = utils.Helpers().packer(
            self.venvs_path, str(venv["name"]))

        reports_map: Dict[str, str] = {
            "Installation report": install_report,
            "Errors and Warnings": install_errors,
            "Pip Freeze Report": pip_freeze_report,
            "Packages Audit Report": pip_check_report,
            "Outdated Packages Report": pip_outdated_report,
            "Build Report": build_report,
        }

        reports.Reports().generate_reports(
            Path(f'{self.venvs_path}/reports'),
            venv["name"], reports_map, exitcode)

    def __generate_venvs(self, venvs: Any) -> None:
        """Generate virtual environments."""
        for venv in venvs:
            # Eensure that the parent venv, if any, is present
            if "parent" in venv:
                parent_dir = Path(f'{self.venvs_path}/{venv["parent"]}')
                if not parent_dir.exists() and parent_dir.is_dir():
                    parent_venv = self.__get_venv_by_name(venv["parent"])
                    if parent_venv is None:
                        raise Exception(
                            "Invalid Virtual Environment configuration.")
                    # Generate the parent first
                    self.__generate_venv(parent_venv)
                self.__generate_venv(venv)
            else:
                self.__generate_venv(venv)

    def run(self) -> None:
        """Run the virtual environments generation."""
        self.venvs = self.get_config()
        self.__generate_venvs(self.venvs)
