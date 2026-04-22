import os

from binary_build_tools.data import (
    LibraryData,
    LibraryType,
    find_dependencies,
    MacOSArm64Runner,
    WindowX64Runner,
    WindowArm64Runner,
    PythonVersion,
)


def write(workflows_path: str, library_data: LibraryData) -> None:
    dependencies = find_dependencies(
        library_data.pypi_name,
        True,
        True,
        True,
        False,
        True,
        True,
        True,
        False,
    )

    shared_libs: tuple[LibraryData, ...] = tuple(
        lib for lib in dependencies if lib.library_type == LibraryType.Shared
    )

    with open(
        os.path.join(workflows_path, "python-build.yml"), "w", encoding="utf-8"
    ) as f:
        f.write(f"""name: Build

on:
  release:
    types: [published]

jobs:
  deploy:
    strategy:
      fail-fast: false
      matrix:
        cfg:
          - {{ os: {WindowX64Runner}, python-version: '{PythonVersion}', architecture: x64 }}
          - {{ os: {WindowArm64Runner}, python-version: '{PythonVersion}', architecture: arm64 }}
          - {{ os: {MacOSArm64Runner}, python-version: '{PythonVersion}', architecture: arm64 }}

    runs-on: ${{{{ matrix.cfg.os }}}}
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

    - name: Install dependencies
      shell: bash
      run: |
        pip install build twine

    - name: Build
      run: |
        python -m build .

    - name: Publish
      env:
        TWINE_USERNAME: ${{{{ secrets.PYPI_USERNAME }}}}
        TWINE_PASSWORD: ${{{{ secrets.{library_data.macro_name}_PYPI_PASSWORD }}}}
      run: |
        twine upload dist/* --skip-existing
""")
