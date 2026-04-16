import os

from binary_build_tools.data import UbuntuX64Runner, PythonVersion


def write(workflows_path: str) -> None:
    with open(
        os.path.join(workflows_path, "python-stylecheck.yml"), "w", encoding="utf-8"
    ) as f:
        f.write(
            f"""# This workflow will install Python dependencies, run tests and lint with a variety of Python versions
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Stylecheck

on:
  push:
    branches:
      - master
      - main
      - '[0-9]+.[0-9]+'
      - '[0-9]+.[0-9]+.[0-9]+'
  pull_request:

jobs:
  stylecheck:
    runs-on: {UbuntuX64Runner}

    steps:
    - name: Clone
      uses: actions/checkout@v6

    - name: Set up Python
      uses: actions/setup-python@v6
      with:
        python-version: {PythonVersion}

    - name: Install dependencies
      run: |
        pip install black

    - name: run stylecheck
      run: |
        python -m black --check --diff .
"""
        )
