import os

from binary_build_tools.data import (
    LibraryData,
    MacOSArm64Runner,
    MacOSX64Runner,
    WindowX64Runner,
    WindowArm64Runner,
    UbuntuX64Runner,
    PythonVersion,
    CheckoutVersion,
    SetupPythonVersion,
    CIBuildWheelVersion,
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
          - {{ os: {WindowX64Runner}, python-version: '{PythonVersion}', architecture: x64, whl: 'cp{PythonVersion.replace(".", "")}-win_amd64' }}
          - {{ os: {WindowArm64Runner}, python-version: '{PythonVersion}', architecture: arm64, whl: 'cp{PythonVersion.replace(".", "")}-win_arm64' }}
          - {{ os: {MacOSX64Runner}, python-version: '{PythonVersion}', architecture: x64, whl: 'cp{PythonVersion.replace(".", "")}-macosx_x86_64' }}
          - {{ os: {MacOSArm64Runner}, python-version: '{PythonVersion}', architecture: arm64, whl: 'cp{PythonVersion.replace(".", "")}-macosx_arm64' }}
          - {{ os: {UbuntuX64Runner}, python-version: '{PythonVersion}', architecture: x64, whl: 'cp{PythonVersion.replace(".", "")}-manylinux_x86_64' }}

    runs-on: ${{{{ matrix.cfg.os }}}}
    timeout-minutes: 45
    defaults:
      run:
        shell: bash

    steps:
    - name: Clone
      uses: actions/checkout@v{CheckoutVersion}{
"""
      with:
        submodules: 'true'""" * library_data.has_submodules
}

    - name: Set up Python
      uses: actions/setup-python@v{SetupPythonVersion}
      with:
        python-version: ${{{{ matrix.cfg.python-version }}}}
        architecture: ${{{{ matrix.cfg.architecture }}}}

    - name: Build and Test
      run: |
        pip install cibuildwheel~={CIBuildWheelVersion}
        cibuildwheel --only ${{{{ matrix.cfg.whl }}}} --output-dir dist .

    - name: Upload artifacts
      uses: actions/upload-artifact@v7
      with:
        path: dist/*
""")
