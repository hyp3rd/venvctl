# Venvctl

[![codecov](https://codecov.io/gl/hyperd/venvctl/branch/master/graph/badge.svg)](https://codecov.io/gl/hyperd/venvctl)

[![pipeline status](https://gitlab.com/hyperd/venvctl/badges/master/pipeline.svg)](https://gitlab.com/hyperd/venvctl/-/commits/master)

A python package to create **portable** virtual enviroments programmatically and using CLI.

## Description

`Venvctl` is a python package to create isolated Python environments. Basically this package, generate the virtual enviroments and build the reports corresponding to each virtual environment.

## Prerequisites

Packages dependency for the usage of `Venvctl`

```text
piphyperd==1.5.5
markd==0.1.19
virtualenv==20.0.3
click==7.0
binaryornot==0.4.4
```

## Installation

Refer to the official [project page](https://pypi.org/project/venvctl/) for further information about the package status and releases.

To install the latest version, run the following command in your terminal:

```bash
pip install --user venvctl
```

## API overview

Once installed, you can import the package as follows `from venvctl import VenvCtl`.

## Usage

Pass the JSON file which will contain the information of all the modules required to generate the virtual env.
Here in the JSON file there will be two sections:

**Base Section**: All the base package which will be shared among all the created Virtualenvs.

**Venvs Section**: Import all the base packages and on top of that it will generate all the required Virtualenvs.

```json
{
    "base": [
        "docker==4.1.0",
        "cryptography==2.7"
    ],
    "venvs": [
        {
            "name": "ansible_2_6",
            "type": "regular",
            "packages": [
                "ansible==2.6",
                "identify==1.4.11"
            ]
        },
        {
            "name": "ansible_2_7",
            "type": "regular",
            "packages": [
                "ansible==2.7",
                "whichcraft==0.5.2"
            ]
        },
        {
            "name": "ansible_2_9_networking",
            "type": "networking",
            "packages": [
                "ansible==2.9",
                "websocket-client==0.56.0",
                "urllib3==1.24.1",
                "tox==3.12.1"
            ]
        }
    ]
}

```

### Programmatically

Run method will basically Generate, Package and Create Documentation for all the required virtualenv passed in **venvs.json**.
Run method basically require two parameters:

1. Path: Where to create the virtual env.

2. Json File: All the pacakges information to create the virtual env.

```python
venvctl.VenvCtl().run()
```

### CLI

### -->TO DO

## License

[GNU General Public License v3 (GPLv3)](https://gitlab.com/hyperd/venvctl/blob/master/LICENSE)

## Author Information

[Francesco Cosentino](https://www.linkedin.com/in/francesco-cosentino/)

I'm a surfer, a crypto trader, and a DevSecOps Engineer with 15 years of experience designing highly-available distributed production environments and developing cloud-native apps in public and private clouds.
