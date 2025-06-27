import os

from binary_build_tools.data import LibraryData, LibraryType, find_dependencies


def write_from_source(workflows_path: str) -> None:
    with open(
        os.path.join(workflows_path, "python-unittests.yml"), "w", encoding="utf-8"
    ) as f:
        f.write(
            """# This workflow will install Python dependencies, run tests and lint with a variety of Python versions
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
        os: [ macos-latest, windows-latest, ubuntu-latest ]

    runs-on: ${{ matrix.os }}
    timeout-minutes: 30
    defaults:
      run:
        shell: bash

    steps:
    - name: Clone
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install
      run: |
        pip install -v .[dev]
        python tools/compile_tests.py

    - name: Test with unittest
      run: python -m unittest discover -v -s tests
"""
        )


def write_compiled(
    workflows_path: str, library_data: LibraryData, shared_libs: tuple[LibraryData, ...]
) -> None:
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
  unittests-first:
    if: github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository
  
    strategy:
      fail-fast: false
      matrix:
        python-version: [ '3.11', '3.12' ]
        os: [ macos-latest, windows-latest ]

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
)}
        rest-token: ${{{{ secrets.GITHUB_TOKEN }}}}

    - name: Install
      env:
        AMULET_FREEZE_COMPILER: 1
      run: |
        pip install --only-binary amulet-compiler-version,{",".join(lib.pypi_name for lib in shared_libs)} -v .[dev]
        python tools/compile_tests.py

    - name: Test with unittest
      run: python -m unittest discover -v -s tests

  unittests-first-ubuntu:
    if: github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository

    strategy:
      fail-fast: false
      matrix:
        python-version: [ '3.11', '3.12' ]
        os: [ ubuntu-latest ]

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

      - name: Build and run unittests
        uses: ./.github/actions/unittests-src
        with:
          python-version: ${{{{ matrix.python-version }}}}

  unittests-third:
    if: github.event_name == 'pull_request' && github.event.pull_request.head.repo.full_name != github.repository

    strategy:
      fail-fast: false
      matrix:
        python-version: [ '3.11', '3.12' ]
        os: [ windows-latest, macos-latest, ubuntu-latest ]

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

      - name: Build and run unittests
        uses: ./.github/actions/unittests-src
        with:
          python-version: ${{{{ matrix.python-version }}}}
"""
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

    if shared_libs:
        write_compiled(workflows_path, library_data, shared_libs)
    else:
        write_from_source(workflows_path)
