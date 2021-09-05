# YAML Config

## Goal

The goal of the YAML Config package is to make nested configurations in YAML easier. The package supports a path like syntax for getting and setting configuration values. In addition, it offers support for configuration default settings. You can instantiate a configuration object directly from a YAML file or by providing a dict youself.

## Examples

The examples below demonstrate how you can use the YAML Config package:

```python
from yaml_config import Config

...
```

## Installation

Installing YAML Config is simple and works just like any other package. Clone the github repository and then install it:

```bash
git clone https://github.com/LFKoning/yaml-config.git
cd yaml-config
python -m pip install .
```

If you want to help develop YAML Config, use the `dev` option instead and also install the `pre-commit` hooks:

```bash
python -m pip install -e .[dev]
pre-commit install
```

The `-e` (`--editable`) flag allows you to make code changes to the package on the fly. Using `pre-commit` is optional, but helps you write clean code (using `black` and `pylint`) before commiting it to the `git` repo.

Linux users can also use the makefile for convenience, to install the package use:

```bash
make install
```

Or for development use:

```bash
make develop
```
