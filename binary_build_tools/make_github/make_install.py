import os

from binary_build_tools.data import LibraryData, find_dependencies


def write(actions_path: str, library_data: LibraryData) -> None:
    action_dir = os.path.join(actions_path, "install")
    os.makedirs(action_dir, exist_ok=True)

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

    with open(os.path.join(action_dir, "action.yml"), "w", encoding="utf-8") as f:
        f.write(
            f"""name: 'Install Specialised {library_data.repo_name}'
description: 'Build, publish and install this library specialised for the installed compiler. Requires Python, build and twine.'
inputs:
  twine-username:
    description: 'The twine username'
    required: true
  twine-password:
    description: 'The twine password'
    required: true
  compiler-specifier:
    description: 'The PEP 440 version specifier for the compiler library'
    required: true{
"".join(f"""
  {lib.short_var_name.replace("_", "-")}-specifier:
    description: 'The PEP 440 version specifier for the {lib.repo_name} library'
    required: true"""
        for lib in dependencies
        )
}{
f"""
  {library_data.short_var_name.replace("_", "-")}-specifier:
    description: 'The PEP 440 version specifier for the {library_data.repo_name} library'
    required: true"""
}
outputs:
  version:
    description: "The version number of the installed library."
    value: ${{{{ steps.get-version.outputs.version }}}}
runs:
  using: "composite"
  steps:
    - name: Validate Inputs
      shell: bash
      run: |
        if [ -z "${{{{ inputs.twine-username }}}}" ]; then
          echo "twine-username is empty"
          exit 1
        fi
        
        if [ -z "${{{{ inputs.twine-password }}}}" ]; then
          echo "twine-password is empty"
          exit 1
        fi
        
        if [ -z "${{{{ inputs.compiler-specifier }}}}" ]; then
          echo "compiler-specifier is empty"
          exit 1
        fi{
"".join(f"""

        if [ -z "${{{{ inputs.{lib.short_var_name.replace("_", "-")}-specifier }}}}" ]; then
          echo "{lib.short_var_name.replace("_", "-")}-specifier is empty"
          exit 1
        fi""" for lib in dependencies)
}

        if [ -z "${{{{ inputs.{library_data.short_var_name.replace("_", "-")}-specifier }}}}" ]; then
          echo "{library_data.short_var_name.replace("_", "-")}-specifier is empty"
          exit 1
        fi

    - name: Install Prebuilt
      id: install
      shell: bash
      continue-on-error: true
      run: |
        python -m pip install --only-binary {library_data.pypi_name} amulet-compiler-version${{{{ inputs.compiler-specifier }}}} {" ".join(f"{lib.pypi_name}${{{{ inputs.{lib.short_var_name.replace("_", "-")}-specifier }}}}" for lib in dependencies)} {library_data.pypi_name}${{{{ inputs.{library_data.short_var_name.replace("_", "-")}-specifier }}}}

    - name: Build
      if: steps.install.outcome == 'failure'
      shell: bash
      env:
        AMULET_FREEZE_COMPILER: 1{
"".join(
    f"""
        {lib.var_name.upper()}_REQUIREMENT: ${{{{ inputs.{lib.short_var_name.replace("_", "-")}-specifier }}}}"""
    for lib in dependencies
)
        }
      run: |
        python -m build --wheel "${{{{ github.action_path }}}}"/../../..

    - name: Publish
      if: steps.install.outcome == 'failure'
      shell: bash
      env:
        TWINE_USERNAME: ${{{{ inputs.twine-username }}}}
        TWINE_PASSWORD: ${{{{ inputs.twine-password }}}}
      run: |
        twine upload "${{{{ github.action_path }}}}"/../../../dist/* --skip-existing

    - name: Install
      if: steps.install.outcome == 'failure'
      shell: bash
      run: |
        python -m pip install "${{{{ github.action_path }}}}"/../../../dist/{library_data.pypi_name.replace("-", "_")}-*.whl

    - name: Get __version__
      id: get-version
      shell: bash
      run: |
        version=$(python -c "import {library_data.import_name}; print({library_data.import_name}.__version__)")
        echo "version=$version" >> "$GITHUB_OUTPUT"
"""
        )
