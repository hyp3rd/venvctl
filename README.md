# venvctl

[![codecov](https://codecov.io/gl/hyperd/venvctl/branch/master/graph/badge.svg)](https://codecov.io/gl/hyperd/venvctl)
[![pipeline status](https://gitlab.com/hyperd/venvctl/badges/master/pipeline.svg)](https://gitlab.com/hyperd/venvctl/-/commits/master)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
![Python package](https://github.com/hyp3rd/venvctl/workflows/Python%20package/badge.svg)

**venvctl** is a CLI tool allowing the creation of fully **portable Python virtual environments**.

## Synopsis

**venvctl** helps to build __fully portable__ Python virtual environments, in **bulk**, or **single** mode, keeping the state in **config files**. Each virtual environment comes with a detailed markdown report, to overview the integrity of its state, broken dependencies, errors, and warnings that occurred in the build process. Eventually, the folders ready for distributions get packed in tarballs, as shown in the example below:

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

## Limitations

It is evident that the portability is limited to systems sharing the same kernel, **do not expect** to build a virtual environment on a **Debian** based system, and deploy it on a **RHEL** host, to mention one of the many cases;

It is possible shipping a virtual environment with a different version of python other than the one installed on the destination system, yet again, do not assume to run python3 based venvs on a system solely configured with python 2.x.

## Requirements

**venvctl** relies on a few packages to explicate its core functionalities:

```text
piphyperd==1.9.6
```

[piphyperd](https://gitlab.com/hyperd/piphyperd/), a wrapper around `pip` to manage installations and audits.

```text
markd==0.1.20
```

[markd](https://github.com/pantsel/markd), a Python package that facilitates the generation of markdown flavored files.

```text
virtualenv==20.0.15  # Virtual Python Environment builder.
click8==8.0.1  # Composable command line interface toolkit.
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

You can leverage **venvctl** both programmatically, or calling the CLI, as shown in the examples below:

Build virtual environments in **bulk programmatically**

```python
"""Python"""
from venvctl import VenvCtl

# Build virtualenvs in bulk
VenvCtl(config_file=/path/to/config.json,
        python_binary=/usr/bin/python{version},
        output_dir=/my/output/dir).run()
```

Build virtual environments in **bulk leveraging the CLI**

```bash
#!/bin/bash

# Build virtualenvs in bulk
venvctl generate \
    --config ~/path/to/your/config/venvs.json \
    --out ./venvs
```

Build a **single virtual environment programmatically**

```python
"""Python"""
from venvctl import VenvCtl

name = "test-venv"
packages = [
    "Click==7.0",
    "binaryornot==0.4.4"
]

# Build a single virtual env;
# It will generate the config file for you.
VenvCtl.create_venv(name=name, packages=packages_list,
                    output_dir=/my/output/dir)
```

Build a **single virtual environment leveraging the CLI**

```bash
#!/bin/bash

# Build a single virtual env;
# It will generate the config file for you.
venvctl create --name my_venv --packages '["tox", "docker"]' --out /my/output/dir
```

### Configuration File

A config file follows the json structure:

```json
[
  {
      "name": "base",
      "packages": [
          "asn1crypto==1.3.0",
          "dnspython==1.16.0",
          "enum34==1.1.10",
          "ipaddress==1.0.23",
          "jmespath==0.9.5",
          "lxml==4.5.0",
          "paramiko==2.7.1",
          "psutil==5.7.0",
          "pycrypto==2.6.1",
          "pyopenssl==19.1.0",
          "python-ldap==3.2.0",
          "python-memcached==1.59"
      ]
  },
  {
    "name": "base_networking",
    "parent": "base",
    "packages": [
      "f5-sdk==3.0.21",
      "bigsuds==1.0.6",
      "netaddr==0.7.19",
      "cloudshell-networking-cisco-iosxr==4.0.6"
    ]
  },
  {
    "name": "ansible_2_9",
    "parent": "base",
    "packages": [
        "ansible==2.9.6"
    ]
  },
  {
    "name": "ansible_2_9_networking",
    "parent": "base_networking",
    "packages": [
        "ansible==2.9.6"
    ]
  }
]
```

The build process follows an inheritance pattern, in the example above, the environment named `base` is the core for the rest; `ansible_2_9` inherits its packages; `ansible_2_9_tox` adds modules on the top of its **parent**, `ansible_2_9`.

With this logic, the build process in bulk can be quite fast, even when deploying complex virtual environments.

### Bandit Support

The security module exposes an ongoing, more experimental set of features. Introduced with the release [1.3.10], at the current stage exposes a basic [**bandit**](https://pypi.org/project/bandit/) scanner, that generates a **markdown** report file as the rest of the **venvctl** features, available in the __reports__ folder, within the virtual environments target path.

Here to follow, an example to trigger a bandit scan from the **CLI**, providing a target folder:

```bash
venvctl bandit --target ./target-folder
```

## Run it with Containers

It is possible to take advantage of a [**container image**](https://gitlab.com/hyperd/factory/-/tree/master/python/centos), built to ship **venvctl** and the whole toolchain to create virtual environments leveraging both **Python 2** and **Python 3**.
Here to follow, two examples running **Docker**.

**Build virtual environments in bulk, shipping Python 3.6.8:**

```bash
docker run -it --rm -v $(pwd)/conf.json:/opt/conf.json \
  -v $(pwd)/venvs:/opt/venvs:rw \
  eu.gcr.io/hyperd-containers/venv-builder:latest venvctl generate \
  --config /opt/conf.json \
  --out /opt/venvs \
```

**Build virtual environments in bulk, shipping Python 2.7.16:**

```bash
docker run -it --rm -v $(pwd)/conf.json:/opt/conf.json \
  -v $(pwd)/venvs:/opt/venvs:rw \
  eu.gcr.io/hyperd-containers/venv-builder:latest venvctl generate \
  --config /opt/conf.json \
  --out /opt/venvs \
  --python /usr/bin/python2
```

### Containers limitations

Currently, the container image available is based on **CentOS 8**. It fits the purpose of any **RHEL** based deployment; however, it won't be useful in other scenarios.
More kernels will be added, stay tuned, or feel free to build your own and poke me.

## License

[GNU General Public License v3 (GPLv3)](https://gitlab.com/hyperd/venvctl/blob/master/LICENSE)

## Report a Vulnerability

If you believe you have found a security vulnerability in **venvctl**, refer to the [Tidelift security policy](https://tidelift.com/docs/security).

The **Tidelift** team will coordinate the vunerability response and disclosure.

## About the author

[Francesco Cosentino](https://www.linkedin.com/in/francesco-cosentino/)

I'm a surfer, a crypto trader, and a DevSecOps Engineer with 15 years of experience designing highly-available distributed production environments and developing cloud-native apps in public and private clouds.
