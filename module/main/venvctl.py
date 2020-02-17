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
# import errno
# import json
import subprocess
from pathlib import Path
from typing import Any, List, Tuple, Dict, Optional
import shutil
from piphyperd import PipHyperd
from ..utils import reports, utils, configutils


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
        # set the environment
        utils.Helpers().set_envoironment()
        # venvs config file
        self.config_file: Path = Path(config_file)
        # venvs base dir
        default_dir = Path(f'{os.getcwd()}/python-venvs')
        # venvs output directory
        self.venvs_path: Path = Path(output_dir) if output_dir else default_dir
        # Initialize venvs
        self.venvs: List[Any] = []
        # path to the python binary to use
        self.python_binary = python_binary if python_binary else sys.executable

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

    # def get_config(self) -> Any:
    #     """Get the venvs config file."""
    #     if self.config_file.exists() and self.config_file.is_file():
    #         with open(self.config_file, 'r') as file:
    #             config = json.load(file)
    #         return config
    #     raise FileNotFoundError(
    #         errno.ENOENT, os.strerror(errno.ENOENT), self.config_file)

    def __create_venv(self, venv_path: Path,
                      venv_packages: List[str],
                      parent_path: Optional[Path]) -> Tuple[str, str, int]:
        """Create virtual environment."""
        # If a parent is defined, clone it and install the extra packages
        if parent_path is not None:
            shutil.copytree(src=parent_path, dst=venv_path)
            return self.install_packages(venv_path, venv_packages)

        process = subprocess.run(
            [str(self.python_binary),
             "-m", "virtualenv",
             "--activators", "bash", "--copies", venv_path], check=True,
            capture_output=True)

        process.check_returncode()

        install_report, install_errors, exitcode = self.install_packages(
            venv_path, venv_packages)

        # Apply fix to /bin/activate
        utils.Helpers().apply_bash_activation_fix(venv_path)

        return install_report, install_errors, exitcode

    def __generate_venv(self, venv: Any) -> None:
        venv_path = Path(f'{self.venvs_path}/{venv["name"]}')
        parent_path = None

        if "parent" in venv:
            parent_path = Path(f'{self.venvs_path}/{venv["parent"]}')

        install_report, install_errors, exitcode = self.__create_venv(
            venv_path, venv["packages"], parent_path)

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

    def __ensure_parent_venv_is_present(self, venv: Any) -> None:
        """Ensure that the prerequisite parent venv is present."""
        parent_dir = Path(f'{self.venvs_path}/{venv["parent"]}')
        if not os.path.isdir(parent_dir):
            parent_venv = configutils.get_item_by_name(
                self.venvs, venv["parent"])
            if parent_venv is None:
                raise Exception(
                    "Invalid Virtual Environment configuration.")
            self.__generate_venv(parent_venv)

    def __generate_venvs(self, venvs: Any) -> None:
        """Generate virtual environments."""
        for venv in venvs:
            if "parent" in venv:
                self.__ensure_parent_venv_is_present(venv)
            self.__generate_venv(venv)

    def run(self) -> None:
        """Run the virtual environments generation."""
        self.venvs = configutils.get_config(self.config_file)
        try:
            configutils.validate_config(self.venvs)
        except AssertionError as error:
            print(str(error))
            sys.exit(1)
        self.__generate_venvs(self.venvs)
