"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

VenvCtl is a python object to leverage virtual environments programmatically.
VenvCtl is a wrapper around virtualenv.

Tools is a helper object.
This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""


import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Any, List, Tuple, Dict
import shutil
from piphyperd import PipHyperd

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
print(PATH)
if PATH not in sys.path:
    sys.path.insert(1, PATH)
    from utils import reports, tools
del PATH


class VenvCtl:
    """
    VenvCtl a wrapper class around virtualenv.

    python_path -- Path to the python binary to use
    """

    def __init__(self, config_file: Path,
                 python_binary: Path = Path("/usr/local/bin/python3.8")):
        """Init the venvctl providing a venvs {config_path}."""
        # venvs config file
        self.config_file: Path = Path(config_file)
        # venvs base dir
        self.venvs_path = Path(f'{os.getcwd()}/python-venvs')
        # path of the base venv
        self.base_venv_path = Path(f'{self.venvs_path}/base')
        # path to the python binary to use
        self.python_binary = python_binary

    @property
    def __get_bash_activation_fix(self) -> str:
        """FIX the bashvenv activation. WARNING.

        If you have any bash profile customization
        at the `cd` command, this fix will breake.
        """
        return "VIRTUAL_ENV=$(cd $(dirname '$BASH_SOURCE'); dirname `pwd`)"

    @property
    def __get_venv_cmd(self) -> str:
        """Return virtualenv command."""
        return 'virtualenv --activators bash --copies'

    def get_config(self):
        """Get the venvs config file."""
        with open(self.config_file, 'r') as file:
            config = json.load(file)

        return config

    @staticmethod
    def parse_venvs(config) -> Tuple[Any, Any, Any]:
        """Parse the venvs config file."""
        base_venv = config["base"]

        all_venvs = config["venvs"]

        # regular venvs
        regulars_venvs = [
            venv for venv in all_venvs if venv["type"] == "regular"]

        # reserved to networking ops
        networking_venvs = [
            venv for venv in all_venvs if venv["type"] == "networking"]
        return base_venv, regulars_venvs, networking_venvs

    @staticmethod
    def install_packages(venv_path: Path,
                         venv_packages: List[str]) -> Tuple[str, str, int]:
        """Install packages within a specific virtual environment."""
        subprocess.call('source {}/bin/activate'.format(venv_path), shell=True)
        piphyperd = PipHyperd(python_path=Path(f'{venv_path}/bin/python3'))

        install_report, install_errors, install_exitcode = piphyperd.install(
            *venv_packages)

        # virtualenv.make_environment_relocatable(venv_path)
        return install_report, install_errors, install_exitcode

    def __create_base_venv(self, venv_packages: List[str]):
        """Create a virtual environment with the shared packages."""
        subprocess.call(
            f'{self.python_binary} -m {self.__get_venv_cmd} {self.base_venv_path}',
            shell=True)
        # virtualenv.create_environment(
        #     home_dir=self.base_venv_path, symlink=False)

        self.install_packages(self.base_venv_path, venv_packages)

        with open(f'{self.base_venv_path}/bin/activate', 'r') as activate_file:
            content = activate_file.read()

        content = content.replace(f"VIRTUAL_ENV='{self.base_venv_path}'",
                                  self.__get_bash_activation_fix)

        with open(f'{self.base_venv_path}/bin/activate', 'w') as activate_file:
            activate_file.write(content)

    def __create_from_base(self, venv_path: Path,
                           venv_packages: List[str]) -> Tuple[str, str, int]:
        shutil.copytree(src=self.base_venv_path, dst=venv_path)
        # virtualenv.copy_file_or_folder(self.base_venv_path, venv_path)
        return self.install_packages(venv_path, venv_packages)

    @staticmethod
    def venv_audit(venv_path: Path):
        """Run audit against a specific virtual environment."""
        piphyperd = PipHyperd(python_path=Path(f'{venv_path}/bin/python3'))

        pip_freeze_report, _, _ = piphyperd.freeze()
        pip_check_report, _, _ = piphyperd.check()

        pip_outdated_report, _, _ = piphyperd.list_packages(True)

        return pip_freeze_report, pip_check_report, pip_outdated_report

    def __generate_venvs(self, venvs):
        for venv in venvs:
            install_report, install_errors, install_exitcode = self.__create_from_base(
                f'{self.venvs_path}/{venv["name"]}', venv["packages"])

            pip_freeze_report, pip_check_report, pip_outdated_report = self.venv_audit(
                f'{self.venvs_path}/{venv["name"]}')

            build_report = tools.Tools().packer(
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
                f'{self.venvs_path}/reports',
                venv["name"], reports_map, install_exitcode)

    def run(self):
        """Run the virtual environments generation."""
        config = self.get_config()
        base_venv, regulars_venvs, networking_venvs = self.parse_venvs(
            config)
        self.__create_base_venv(base_venv)

        self.__generate_venvs(regulars_venvs)

        self.__generate_venvs(networking_venvs)
