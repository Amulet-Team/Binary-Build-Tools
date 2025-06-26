import os

from binary_build_tools.data import LibraryData, LibraryType, find_dependencies


def write(actions_path: str, library_data: LibraryData) -> None:
    if not any(
        lib.library_type == LibraryType.Shared
        for lib in find_dependencies(
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
    ):
        return

    action_dir = os.path.join(actions_path, "unittests-src")
    os.makedirs(action_dir, exist_ok=True)

    with open(os.path.join(action_dir, "action.yml"), "w", encoding="utf-8") as f:
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
