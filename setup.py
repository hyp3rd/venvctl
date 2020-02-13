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

import os
import re
import setuptools


def envstring(var):
    """Return environment var as string."""
    return os.environ.get(var) or ""


try:
    with open("README.md", "r") as fh:
        LONG_DESCRIPTION = fh.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ""

if os.path.isfile("variables"):
    try:
        with open("variables", "r") as fh:
            VARIABLES = fh.read().strip().split("\n")
        for v in VARIABLES:
            key, value = v.split("=")
            os.environ[key] = re.sub("['\"]", "", value)
    except FileNotFoundError:
        pass

print(envstring("NAME"))

setuptools.setup(
    name=envstring("NAME"),
    version=envstring("VERSION"),
    author=envstring("AUTHOR"),
    author_email=envstring("AUTHOR_EMAIL"),
    description=envstring("DESCRIPTION"),
    url=envstring("URL"),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=[
        envstring("NAME"), envstring("NAME") + ".main",
        envstring("NAME"), envstring("NAME") + ".utils"
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries',
        'Environment :: Plugins',
    ],
    zip_safe=False,
)
