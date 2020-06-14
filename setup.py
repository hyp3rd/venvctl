"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

VenvCtl setup.
VenvCtl is a wrapper around virtualenv.

Tools is a helper object.
This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
"""
from __future__ import (absolute_import, division, print_function)
import codecs
import os
import re
from typing import Any
import setuptools

entry_points: str = """\"""THIS SOFTWARE IS PROVIDED AS IS.

Released under GNU General Public License:
<https://www.gnu.org/licenses/gpl-3.0.en.html>

USE IT AT YOUR OWN RISK.

VenvCtl is a python object to leverage virtual environments programmatically.
VenvCtl is a wrapper around virtualenv.

This module is part of VenvCtl: <https://pypi.org/project/venvctl/>.
The code is available on GitLab: <https://gitlab.com/hyperd/venvctl>.
\"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type  # pylint: disable=invalid-name

__version__ = \"{version}\"
__author__ = \"Hyper(d)\"
"""


def envstring(var: str) -> str:
    """Return environment var as string."""
    return os.environ.get(var) or ""


def read(rel_path: str) -> Any:
    """Read file helper."""
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), 'r') as file_path:
        return file_path.read()


try:
    LONG_DESCRIPTION = read("README.md")
except FileNotFoundError:
    LONG_DESCRIPTION = ""

if os.path.isfile("variables"):
    try:
        VARIABLES = read("variables").strip().split("\n")
        for v in VARIABLES:
            key, value = v.split("=")
            os.environ[key] = re.sub("['\"]", "", value)
    except FileNotFoundError:
        pass

setuptools.setup(
    name=envstring("NAME"),

    # Version SCM based.
    use_scm_version={
        'write_to': 'module/main/release.py',
        'write_to_template': entry_points,
        'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$',
        'version_scheme': 'python-simplified-semver',
        'local_scheme': 'no-local-version',
    },

    description=envstring("DESCRIPTION"),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    license='GPL-3.0',

    author=envstring("AUTHOR"),
    author_email=envstring("AUTHOR_EMAIL"),

    url=envstring("URL"),

    project_urls={
        "Documentation": envstring("URL"),
        "Source": envstring("DOCUMENTATION_URL"),
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Plugins',
    ],

    install_requires=[
        'piphyperd==1.9.8',
        'markd==0.1.20',
        'virtualenv==20.0.23',
        'click8==8.0.1',
        'binaryornot==0.4.4',
        'bandit==1.6.2',
    ],

    packages=[
        envstring("NAME"), envstring("NAME") + ".main",
        envstring("NAME"), envstring("NAME") + ".utils",
        envstring("NAME"), envstring("NAME") + ".security",
        envstring("NAME"), envstring("NAME") + ".cli",
    ],

    entry_points={
        "console_scripts": [
            "venvctl=venvctl.cli.main:run",
        ]
    },

    python_requires='>=3.6',
    zip_safe=False,
)
