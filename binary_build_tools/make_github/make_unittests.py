import os

from binary_build_tools.data import LibraryData, MacOSRunner, WindowRunner, UbuntuRunner


def write(workflows_path: str, library_data: LibraryData) -> None:
    with open(
        os.path.join(workflows_path, "python-unittests.yml"), "w", encoding="utf-8"
    ) as f:
        f.write(
            f"""# This workflow will install Python dependencies, run tests and lint with a variety of Python versions
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Unittests

on:
  push:
    branches:
      - master
      - main
      - '[0-9]+.[0-9]+'
      - '[0-9]+.[0-9]+.[0-9]+'
  pull_request:

jobs:
  unittests:
    strategy:
      fail-fast: false
      matrix:
        python-version: [ '3.11', '3.12' ]
        os: [ {MacOSRunner}, {WindowRunner}, {UbuntuRunner} ]

    runs-on: ${{{{ matrix.os }}}}
    timeout-minutes: 30
    defaults:
      run:
        shell: bash

    steps:
    - name: Clone
      uses: actions/checkout@v4{
"""
      with:
        submodules: 'true'""" * library_data.has_submodules
}

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{{{ matrix.python-version }}}}
        
    - name: Build
      run: |
        pip install -v .[dev]
        python tools/compile_tests.py
        
    - name: Test with unittest
      run: python -m unittest discover -v -s tests
"""
        )
