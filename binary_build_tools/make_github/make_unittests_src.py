import os

from binary_build_tools.data import LibraryData, libraries, library_order, LibraryType

def write(actions_path: str, library_data: LibraryData) -> None:
    # find all shared dependencies recursively
    lib_names: set[str] = set()
    lib_names_todo: set[str] = set(
        library_data.private_dependencies
        + library_data.public_dependencies
        + library_data.ext_dependencies
    )

    while lib_names_todo:
        lib_name = lib_names_todo.pop()
        if lib_name in lib_names:
            continue
        lib_names.add(lib_name)
        lib = libraries[lib_name]
        lib_names_todo.update(
            lib.private_dependencies + lib.public_dependencies + lib.ext_dependencies
        )

    dependencies: tuple[LibraryData, ...] = tuple(
        libraries[pypi_name]
        for pypi_name in sorted(lib_names, key=library_order.__getitem__)
    )

    shared_libs: tuple[LibraryData, ...] = tuple(
        lib for lib in dependencies if lib.library_type == LibraryType.Shared
    )

    if not shared_libs:
        return

    action_dir = os.path.join(actions_path, "unittests-src")
    os.makedirs(action_dir, exist_ok=True)

    with open(
        os.path.join(action_dir, "action.yml"), "w", encoding="utf-8"
    ) as f:
        f.write(
            """\
name: 'Src Unit-tests'
description: 'Build from source and run unittests.'
inputs:
  python-version:
    description: 'The version of Python to install'
    required: true
runs:
  using: "composite"
  steps:
    - name: Validate Inputs
      shell: bash
      run: |
        if [ -z "${{ inputs.python-version }}" ]; then
          echo "python-version is empty"
          exit 1
        fi 

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}

    - name: Build
      shell: bash
      run: |
        pip install -v .[dev]
        python tools/compile_tests.py

    - name: Test with unittest
      shell: bash
      run: python -m unittest discover -v -s tests
"""
        )
