import os

from binary_build_tools.data import LibraryData, libraries, library_order, LibraryType


def write(workflows_path: str, library_data: LibraryData) -> None:
    library_dependencies: dict[str, tuple[LibraryData, ...]] = {}

    def get_library_dependencies(pypi_name: str) -> tuple[LibraryData, ...]:
        if pypi_name not in library_dependencies:
            root_lib = libraries[pypi_name]

            # find all shared dependencies recursively
            lib_names: set[str] = set()
            lib_names_todo: set[str] = set(
                root_lib.private_dependencies
                + root_lib.public_dependencies
                + root_lib.ext_dependencies
            )

            while lib_names_todo:
                lib_name = lib_names_todo.pop()
                if lib_name in lib_names:
                    continue
                lib_names.add(lib_name)
                lib = libraries[lib_name]
                lib_names_todo.update(
                    lib.private_dependencies
                    + lib.public_dependencies
                    + lib.ext_dependencies
                )

            library_dependencies[pypi_name] = tuple(
                libraries[pypi_name]
                for pypi_name in sorted(lib_names, key=library_order.__getitem__)
            )

        return library_dependencies[pypi_name]

    dependencies: tuple[LibraryData, ...] = get_library_dependencies(
        library_data.pypi_name
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
      uses: actions/checkout@v4

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
