import os
import sys
import shutil
import subprocess

from .data import LibraryData, shared_libraries

from . import (
    make_gitattributes,
    make_gitignore,
    make_manifest,
    make_mypy_ini,
    make_build_requires,
    make_setup,
    make_pyproject,
    make_package,
    make_tests,
    make_tools,
    make_cmakelists,
    make_github,
    make_requirements,
    make_get_compiler,
)


def write(project_path: str, library_data: LibraryData) -> None:
    os.makedirs(project_path, exist_ok=True)
    make_gitignore.write(project_path, library_data)
    make_gitattributes.write(project_path, library_data)
    make_manifest.write(project_path, library_data)
    make_mypy_ini.write(project_path, library_data)
    make_build_requires.write(project_path)
    make_setup.write(project_path, library_data)
    make_pyproject.write(project_path, library_data)
    make_cmakelists.write(project_path, library_data)
    make_requirements.write(project_path, library_data)
    make_get_compiler.write(project_path)

    package_path = os.path.join(
        project_path, "src", *library_data.import_name.split(".")
    )
    os.makedirs(package_path, exist_ok=True)
    make_package.write(package_path, library_data)

    tests_path = os.path.join(project_path, "tests")
    os.makedirs(tests_path, exist_ok=True)
    make_tests.write(tests_path, library_data)

    tools_path = os.path.join(project_path, "tools")
    os.makedirs(tools_path, exist_ok=True)
    make_tools.write(tools_path, library_data)

    github_path = os.path.join(project_path, ".github")
    os.makedirs(github_path, exist_ok=True)
    make_github.write(github_path, library_data)


def main(out_path: str) -> None:
    shutil.rmtree(out_path, ignore_errors=True)
    os.makedirs(out_path, exist_ok=True)
    for library_data in shared_libraries:
        project_path = os.path.join(out_path, library_data.repo_name)
        write(project_path, library_data)
    subprocess.run([sys.executable, "-m", "black", out_path])
