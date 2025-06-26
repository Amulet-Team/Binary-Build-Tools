import os

from binary_build_tools.data import LibraryData, LibraryType, find_dependencies


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
        f.write(
            f"""# This workflow will install Python dependencies, run tests and lint with a variety of Python versions
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Build

on:
  release:
    types: [published]

jobs:
  deploy:
    strategy:
      fail-fast: false
      matrix:
        python-version: [ '3.11', '3.12' ]
        os: [ macos-14, windows-latest ]

    runs-on: ${{{{ matrix.os }}}}
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

    - name: Install dependencies
      uses: ./.github/actions/install-dependencies
      with:
        python-version: ${{{{ matrix.python-version }}}}
        username: ${{{{ secrets.PYPI_USERNAME }}}}
        compiler-version-password: ${{{{ secrets.AMULET_COMPILER_VERSION_PYPI_PASSWORD }}}}{
"".join(
f"""
        {lib.short_var_name.replace("_", "-")}-password: ${{{{ secrets.{lib.var_name.upper()}_PYPI_PASSWORD }}}}"""
    for lib in shared_libs
)}{
"\n        rest-token: ${{ secrets.GITHUB_TOKEN }}" * bool(shared_libs)
}

    - name: Build SDist
      run: |
        python -m build --sdist .

    - name: Build Wheel
      env:
        AMULET_FREEZE_COMPILER: 1
      run: |
        python -m build --wheel .

    - name: Publish
      env:
        TWINE_USERNAME: ${{{{ secrets.PYPI_USERNAME }}}}
        TWINE_PASSWORD: ${{{{ secrets.{library_data.var_name.upper()}_PYPI_PASSWORD }}}}
      run: |
        twine upload dist/* --skip-existing
"""
        )
