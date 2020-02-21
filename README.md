# venvctl

[![codecov](https://codecov.io/gl/hyperd/venvctl/branch/master/graph/badge.svg)](https://codecov.io/gl/hyperd/venvctl)

[![pipeline status](https://gitlab.com/hyperd/venvctl/badges/master/pipeline.svg)](https://gitlab.com/hyperd/venvctl/-/commits/master)

**venvctl** is a tool allowing the creation of **portable Python virtual environments**.

## Synopsis

**venvctl** helps to build __fully portable__ Python virtual environments, in **bulk**, or **single** mode, keeping the state in **config files**. Each virtual environment comes with a detailed markdown report, allowing you to control the integrity of its state, broken dependencies, errors, and warnings that occurred in the build process. Eventually, the folders ready for distributions get packed in tarballs, as shown in the folders tree example below:

```bash
...
│   ...
│   └── pyvenv.cfg
├── builds
│   ├── ansible_2_9.tar.gz
│   └── base.tar.gz
└── reports
    ├── ansible_2_9.md
    └── base.md
```

## Requirements

**venvctl** relies on a few packages to explicate its core functionalities:

```text
piphyperd==1.7.3
```

[piphyperd](https://gitlab.com/hyperd/piphyperd/), a wrapper around `pip` to manage installations and audits.

```text
markd==0.1.20
```

[markd](https://github.com/pantsel/markd), a Python package that facilitates the generation of markdown flavored files.

```text
virtualenv==20.0.3  # Virtual Python Environment builder.
click==7.0  # Composable command line interface toolkit.
binaryornot==0.4.4  # Ultra-lightweight pure Python package to check if a file is binary or text.
```

## Installation

**venvctl** is currently distributed only through PyPi.org

```bash
pip install --user venvctl
```

Visit the [project page](https://pypi.org/project/venvctl/) for further information about the package status and releases.

## Documentation

For the detailed instructions and a full API walkthroug, refer to the [Official Documenation](https://venvctl.readthedocs.io/en/latest/).

You can leverage **venvctl** both programmatically, or calling the CLI, as shown in the example below:

```bash
venvctl generate \
    --config ~/path/to/your/config/venvs.json \
    --out ./venvs
```

A config file follows the json structure:

```json
[{
        "name": "base",
        "packages": [
            "docker==4.1.0"
        ]
    },
    {
        "name": "ansible_2_9",
        "parent": "base",
        "packages": [
            "ansible==2.9"
        ]
    },
    {
        "name": "ansible_2_9_tox",
        "parent": "ansible_2_9",
        "packages": [
            "tox==3.12.1"
        ]
    }
]
```

The build process follows an inheritance pattern, in the example above, the environment named `base` is the core for the rest; `ansible_2_9` inherits its packages; `ansible_2_9_tox` adds modules on the top of its **parent**, `ansible_2_9`.

With this logic, the build process in bulk can be quite fast, even when deploying complex virtual environments.

## License

[GNU General Public License v3 (GPLv3)](https://gitlab.com/hyperd/venvctl/blob/master/LICENSE)

## About the author

[Francesco Cosentino](https://www.linkedin.com/in/francesco-cosentino/)

I'm a surfer, a crypto trader, and a DevSecOps Engineer with 15 years of experience designing highly-available distributed production environments and developing cloud-native apps in public and private clouds.
