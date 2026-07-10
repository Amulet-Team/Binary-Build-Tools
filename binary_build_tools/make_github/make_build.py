import os

from binary_build_tools.data import (
    LibraryData,
    LibraryType,
    find_dependencies,
    MacOSX64Runner,
    MacOSArm64Runner,
    WindowX64Runner,
    WindowArm64Runner,
    UbuntuX64Runner,
    PythonVersion,
    CIBuildWheelVersion,
    CheckoutVersion,
    SetupPythonVersion,
)


def write(workflows_path: str, library_data: LibraryData) -> None:
    if not library_data.create_build_workflow:
        return
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
          - {{ os: {WindowX64Runner}, python-version: '{PythonVersion}', architecture: x64, whl: 'cp{PythonVersion.replace(".", "")}-win_amd64' }}
          - {{ os: {WindowArm64Runner}, python-version: '{PythonVersion}', architecture: arm64, whl: 'cp{PythonVersion.replace(".", "")}-win_arm64' }}
          - {{ os: {MacOSX64Runner}, python-version: '{PythonVersion}', architecture: x64, whl: 'cp{PythonVersion.replace(".", "")}-macosx_x86_64' }}
          - {{ os: {MacOSArm64Runner}, python-version: '{PythonVersion}', architecture: arm64, whl: 'cp{PythonVersion.replace(".", "")}-macosx_arm64' }}
          - {{ os: {UbuntuX64Runner}, python-version: '{PythonVersion}', architecture: x64, whl: 'cp{PythonVersion.replace(".", "")}-manylinux_x86_64' }}

    runs-on: ${{{{ matrix.cfg.os }}}}
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

    - name: Build sdist
      run: |
        pip install build
        python -m build --sdist --outdir dist .

    - name: Build
      env:
        CIBW_TEST_COMMAND: ""
      run: |
        pip install cibuildwheel~={CIBuildWheelVersion}
        cibuildwheel --only ${{{{ matrix.cfg.whl }}}} --output-dir dist .

    - name: Install twine
      shell: bash
      run: |
        pip install twine

    - name: Publish
      env:
        TWINE_USERNAME: ${{{{ secrets.PYPI_USERNAME }}}}
        TWINE_PASSWORD: ${{{{ secrets.{library_data.project_macro_name}_PYPI_PASSWORD }}}}
      run: |
        twine upload dist/* --skip-existing
""")
