import os

from binary_build_tools.data import (
    LibraryData,
    MacOSArm64Runner,
    MacOSX64Runner,
    WindowX64Runner,
    WindowArm64Runner,
    UbuntuX64Runner,
    PythonVersion,
)


def write(workflows_path: str, library_data: LibraryData) -> None:
    with open(
        os.path.join(workflows_path, "python-unittests.yml"), "w", encoding="utf-8"
    ) as f:
        f.write(f"""name: Unittests

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
        cfg:
          - {{ os: {WindowX64Runner}, python-version: '{PythonVersion}', architecture: x64 }}
          - {{ os: {WindowArm64Runner}, python-version: '{PythonVersion}', architecture: arm64 }}
          - {{ os: {MacOSX64Runner}, python-version: '{PythonVersion}', architecture: x64 }}
          - {{ os: {MacOSArm64Runner}, python-version: '{PythonVersion}', architecture: arm64 }}
          - {{ os: {UbuntuX64Runner}, python-version: '{PythonVersion}', architecture: x64 }}

    runs-on: ${{{{ matrix.cfg.os }}}}
    timeout-minutes: 45
    defaults:
      run:
        shell: bash

    steps:
    - name: Clone
      uses: actions/checkout@v6{
"""
      with:
        submodules: 'true'""" * library_data.has_submodules
}

    - name: Setup cmake
      uses: jwlawson/actions-setup-cmake@v2

    - name: Set up Python
      uses: actions/setup-python@v6
      with:
        python-version: ${{{{ matrix.cfg.python-version }}}}
        architecture: ${{{{ matrix.cfg.architecture }}}}
{library_data.unittests_pre_build}
    - name: Build
      run: |
        pip install -v .{f"[{",".join(library_data.unittest_dep_groups)}]" if library_data.unittest_dep_groups else ""}
{"" if library_data.lib_name is None else "        python tools/compile_tests.py\n"}\
{library_data.unittests_pre_test}
    - name: Test with unittest
      run: python -m unittest discover -v -s tests
""")
