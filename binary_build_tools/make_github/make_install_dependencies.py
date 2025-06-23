import os

from binary_build_tools.data import LibraryData, libraries, library_order, LibraryType


def write(actions_path: str, library_data: LibraryData) -> None:
    action_dir = os.path.join(actions_path, "install-dependencies")
    os.makedirs(action_dir, exist_ok=True)

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
                    lib.private_dependencies + lib.public_dependencies + lib.ext_dependencies
                )

            library_dependencies[pypi_name] = tuple(
                libraries[pypi_name]
                for pypi_name in sorted(lib_names, key=library_order.__getitem__)
            )

        return library_dependencies[pypi_name]

    dependencies: tuple[LibraryData, ...] = get_library_dependencies(library_data.pypi_name)

    shared_libs: tuple[LibraryData, ...] = tuple(
        lib for lib in dependencies if lib.library_type == LibraryType.Shared
    )

    with open(os.path.join(action_dir, "action.yml"), "w", encoding="utf-8") as f:
        f.write(
            f"""name: 'Install dependencies'
description: 'Build if needed and install the library dependencies'
inputs:
  python-version:
    description: 'The version of Python to install'
    required: true
  username:
    description: 'The pypi username'
    required: true
  compiler-version-password:
    description: 'The password for the compiler-version library'
    required: true{
# We only need passwords for shared libraries
"".join(f"""
  {lib.short_var_name.replace("_", "-")}-password:
    description: 'The password for the {lib.short_var_name.replace("_", "-")} library'
    required: true""" for lib in shared_libs)
}{
"""
  rest-token:
    description: 'The Github authentication token to use to access the REST API.'
    required: true""" * bool(shared_libs)
}
runs:
  using: "composite"
  steps:
    - name: Validate Inputs
      shell: bash
      run: |
        if [ -z "${{{{ inputs.python-version }}}}" ]; then
          echo "python-version is empty"
          exit 1
        fi

        if [ -z "${{{{ inputs.username }}}}" ]; then
          echo "username is empty"
          exit 1
        fi

        if [ -z "${{{{ inputs.compiler-version-password }}}}" ]; then
          echo "compiler-version-password is empty"
          exit 1
        fi{
"".join(f"""

        if [ -z "${{{{ inputs.{lib.short_var_name.replace("_", "-")}-password }}}}" ]; then
          echo "{lib.short_var_name.replace("_", "-")}-password is empty"
          exit 1
        fi""" for lib in shared_libs)
}{
"""

        if [ -z "${{ inputs.rest-token }}" ]; then
          echo "rest-token is empty"
          exit 1
        fi""" * bool(shared_libs)
}

    - name: Set up Python ${{{{ inputs.python-version }}}}
      uses: actions/setup-python@v5
      with:
        python-version: ${{{{ inputs.python-version }}}}

    - name: Install dependencies
      shell: bash
      run: |
        pip install build twine packaging

    - name: Clone Amulet-Compiler-Version
      uses: actions/checkout@v4
      with:
        repository: 'Amulet-Team/Amulet-Compiler-Version'
        ref: '3.0'
        path: 'build/pylib/Amulet-Compiler-Version'

    - name: Install Amulet-Compiler-Version
      id: compiler
      uses: ./build/pylib/Amulet-Compiler-Version/.github/actions/install
      with:
        twine-username: ${{{{ inputs.username }}}}
        twine-password: ${{{{ inputs.compiler-version-password }}}}
""")
        if not shared_libs:
            return
        f.write(f"""
    - name: Get Dependencies
      id: dep
      shell: bash
      env:
        REST_TOKEN: ${{{{ inputs.rest-token }}}}
      run: |
        python -c "import sys; sys.path.append(r'${{{{ github.action_path }}}}'); import dependency_resolver; import requirements; dependency_resolver.find_and_save_compatible_libraries([{", ".join(f"('{lib.pypi_name}', '{lib.org_name}/{lib.repo_name}')" for lib in shared_libs)}], requirements.get_runtime_dependencies())"{
"".join(
    f"""
        {lib.short_var_name.replace("_", "-")}=$(python -c "import os; f = open(os.path.join(r'${{{{ github.action_path }}}}', 'libraries.json'), encoding='utf-8'); import json; print(json.load(f)['{lib.pypi_name}'])")
        echo "{lib.short_var_name.replace("_", "-")}=${lib.short_var_name.replace("_", "-")}" >> "$GITHUB_OUTPUT"\
"""
    for lib in dependencies
)
        }

    - name: Specialise Specifiers
      id: dep2
      shell: bash
      run: |{
"".join(
    f"""
        {lib.short_var_name.replace("_", "-")}=$(python -c "import requirements; print(requirements.get_specifier_set('${{{{ steps.dep.outputs.{lib.short_var_name.replace("_", "-")} }}}}'))")
        echo "{lib.short_var_name.replace("_", "-")}=${lib.short_var_name.replace("_", "-")}" >> "$GITHUB_OUTPUT"\
"""
    for lib in dependencies
)
      }

{
"".join(
    f"""
    - name: Clone {lib.repo_name}
      uses: Amulet-Team/checkout-pep440@v1
      with:
        repository: '{lib.org_name}/{lib.repo_name}'
        specifier: '==${{{{ steps.dep.outputs.{lib.short_var_name.replace("_", "-")} }}}}'
        path: 'build/pylib/{lib.repo_name}'
        rest-token: ${{{{ inputs.rest-token }}}}

    - name: Install {lib.repo_name}
      uses: ./build/pylib/{lib.repo_name}/.github/actions/install
      with:
        twine-username: ${{{{ inputs.username }}}}
        twine-password: ${{{{ inputs.{lib.short_var_name.replace("_", "-")}-password }}}}
        compiler-specifier: '==${{{{ steps.compiler.outputs.version }}}}'{
"".join(
    f"""
        {lib2.short_var_name.replace("_", "-")}-specifier: ${{{{ steps.dep2.outputs.{lib2.short_var_name.replace("_", "-")} }}}}\
""" for lib2 in get_library_dependencies(lib.pypi_name)
)
        }
        {lib.short_var_name.replace("_", "-")}-specifier: ${{{{ steps.dep2.outputs.{lib.short_var_name.replace("_", "-")} }}}}
"""
    for lib in shared_libs
)
}
"""
        )

    with open(
        os.path.join(action_dir, "dependency_resolver.py"), "w", encoding="utf-8"
    ) as f:
        f.write(
            """import os
import json
import itertools
from typing import Any
from types import MappingProxyType
from collections.abc import Iterable, Mapping, Iterator
import urllib.request
import urllib.parse
from dataclasses import dataclass
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet
from packaging.requirements import Requirement
from functools import lru_cache


github_api_url = os.environ.get("GITHUB_API_URL", "https://api.github.com")


@lru_cache(maxsize=None)
def _get_github_releases(repo: str, page: int):
    print(f"Github REST request {repo} page {page}")
    query = urllib.parse.urlencode({"per_page": 100, "page": page})
    url = f"{github_api_url}/repos/{repo}/releases?{query}"
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("REST_TOKEN"):
        headers["Authorization"] = f"token {os.environ.get('REST_TOKEN')}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return data


@lru_cache(maxsize=None)
def _get_tags(repo: str) -> Iterator[Version]:
    for page in itertools.count(1):
        data = _get_github_releases(repo, page)
        if not data:
            break
        for release in data:
            try:
                v = Version(release["tag_name"])
            except InvalidVersion:
                continue
            else:
                yield v


def _get_compatible_tags(repo: str, specifier: SpecifierSet) -> Iterator[Version]:
    return (v for v in _get_tags(repo) if v in specifier)


@dataclass(frozen=True)
class Library:
    lib_name: str
    repo_name: str


@lru_cache(maxsize=None)
def _exec_module(module_str: str) -> dict[str, Any]:
    m = {}
    exec(module_str, m, m)
    return m


@lru_cache(maxsize=None)
def _get_requirements_module(repo: str, tag: str) -> dict[str, Any]:
    url = f"https://raw.githubusercontent.com/{repo}/{tag}/requirements.py"
    with urllib.request.urlopen(url) as resp:
        module_str = resp.read().decode()
    return _exec_module(module_str)


def parse_requirements(requirements: Iterable[str]) -> Mapping[str, SpecifierSet]:
    split_requirements = {}
    for req_s in requirements:
        req = Requirement(req_s)
        split_requirements[_fix_library_name(req.name)] = req.specifier
    return MappingProxyType(split_requirements)


@lru_cache(maxsize=None)
def _get_requirements(repo: str, tag: str) -> Mapping[str, SpecifierSet]:
    m = _get_requirements_module(repo, tag)
    return parse_requirements(m["get_runtime_dependencies"]())


@lru_cache(maxsize=None)
def _get_pypi_releases(lib_name: str) -> MappingProxyType[str, Any]:
    print(f"Getting PyPI releases for {lib_name}")
    url = f"https://pypi.org/pypi/{lib_name}/json"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode())
    return data["releases"]


class NoValidVersion(Exception):
    pass


@lru_cache(maxsize=None)
def _get_pypi_release(lib_name: str, specifier: SpecifierSet) -> Version:
    releases = _get_pypi_releases(lib_name)
    for version_str, files in releases.items():
        version = Version(version_str)
        # release must match the specifier and have a source distribution
        if version in specifier and any(
            file.get("packagetype", None) == "sdist" for file in files
        ):
            return version
    raise NoValidVersion


def _fix_library_name(name: str) -> str:
    return name.replace("_", "-")


def _find_compatible_libraries(
    libraries: tuple[Library, ...],
    requirements: Mapping[str, SpecifierSet],
    libraries_todo: tuple[Library, ...],
    libraries_frozen: Mapping[str, Version] = MappingProxyType({}),
) -> Mapping[str, Version]:
    # Get the library to freeze and the libraries left to freeze
    library_freeze = libraries_todo[0]
    libraries_todo = tuple(libraries_todo[1:])

    # Verify that this library has not already been frozen
    if library_freeze.lib_name in libraries_frozen:
        raise RuntimeError(f"Library {library_freeze.lib_name} listed more than once.")

    processed_requirement_configurations = []

    # Iterate through all versions that match the specifier
    for v in _get_compatible_tags(
        library_freeze.repo_name,
        requirements.get(library_freeze.lib_name, SpecifierSet()),
    ):
        print(f"Trying {library_freeze.lib_name}=={v}")
        # Get the requirements this library adds
        library_requirements = _get_requirements(library_freeze.repo_name, str(v))

        # If the library_requirements match a previous version, skip
        if library_requirements in processed_requirement_configurations:
            continue
        else:
            processed_requirement_configurations.append(library_requirements)

        # Extend the existing requirements.
        new_requirements = dict(requirements)
        for name, specifier in library_requirements.items():
            if name in new_requirements:
                specifier = new_requirements[name] & specifier

            # check the frozen requirements are still valid.
            if name in libraries_frozen and libraries_frozen[name] not in specifier:
                raise NoValidVersion

            new_requirements[name] = specifier

        # Add the library to the frozen libraries
        new_libraries_frozen = {**libraries_frozen, library_freeze.lib_name: v}

        if libraries_todo:
            # if we have more libraries to freeze go to the next one
            try:
                return _find_compatible_libraries(
                    libraries,
                    MappingProxyType(new_requirements),
                    libraries_todo,
                    MappingProxyType(new_libraries_frozen),
                )
            except NoValidVersion:
                # If dependency resolution failed below this, try the next version of the library
                continue
        else:
            # Make sure all libraries have a compatible pypi release
            try:
                for name, specifier in new_requirements.items():
                    if name not in new_libraries_frozen:
                        new_libraries_frozen[name] = _get_pypi_release(name, specifier)
            except NoValidVersion:
                continue
            # No more libraries to freeze.
            return MappingProxyType(new_libraries_frozen)
    # Raise if no version matched
    raise NoValidVersion


def find_compatible_libraries(
    libraries: Iterable[tuple[str, str]], requirements: Iterable[str]
) -> Mapping[str, Version]:
    libraries_ = tuple(
        Library(_fix_library_name(lib_name), repo_name)
        for lib_name, repo_name in libraries
    )
    return _find_compatible_libraries(
        libraries_,
        parse_requirements(requirements),
        libraries_,
    )


def find_and_save_compatible_libraries(
    compiled_library_data: Iterable[tuple[str, str]], requirements: Iterable[str]
) -> None:
    libraries = find_compatible_libraries(compiled_library_data, requirements)
    print(libraries)
    with open(
        os.path.join(os.path.dirname(__file__), "libraries.json"), "w", encoding="utf-8"
    ) as f:
        json.dump({name: str(specifier) for name, specifier in libraries.items()}, f)


if __name__ == "__main__":
    find_and_save_compatible_libraries(
        [
            ("amulet-game", "Amulet-Team/Amulet-Game"),
            ("amulet-core", "Amulet-Team/Amulet-Core"),
            ("amulet-nbt", "Amulet-Team/Amulet-NBT"),
            ("amulet-zlib", "Amulet-Team/Amulet-zlib"),
        ],
        [
            f"amulet-compiler-target==1.0",
            f"amulet-io~=1.0",
            f"amulet-compiler-version==3.0.0",
            f"amulet-nbt~=5.0.0.0a0",
            f"amulet-core~=2.0.2.0a0",
            f"amulet-game~=1.0.0.0a0",
        ],
    )
"""
        )
