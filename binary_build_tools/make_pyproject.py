import os

from .data import LibraryData, libraries


def write(project_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(project_path, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(
            f"""[build-system]
requires = [
    "setuptools>=42",
    "versioneer",
    "packaging",
]
build-backend = "build_requires"
backend-path = [""]

[project]
name = "{library_data.pypi_name}"
authors = [
    {{name = "James Clare"}},
]
description = ""
dynamic = ["version", "readme", "dependencies"]
requires-python = ">=3.11"
classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]

[project.optional-dependencies]
dev = [
    "setuptools>=42",
    "types-setuptools",
    "versioneer",
    "types-versioneer",
    "packaging",
    "wheel",
    "pybind11_stubgen>=2.5.4",
    "black>=22.3",
    "isort",
    "autoflake",
    "mypy",
    "types-pyinstaller",{
        "".join(
            f'\n    "{lib_name}{libraries[lib_name].specifier}",'
            for lib_name in ("amulet-test-utils",)
            if lib_name in library_data.test_dependencies
        )
    }
]

[project.urls]
Homepage = "https://www.amuletmc.com"
Repository = "https://github.com/Amulet-Team/{library_data.repo_name}"
Issues = "https://github.com/Amulet-Team/{library_data.repo_name}/issues"

[tool.setuptools]
include-package-data = false

[tool.setuptools.package-data]
"*" = [
    "*Config.cmake",
    "**/*.hpp",
    "**/*.dll",
    "**/*.so",
    "**/*.dylib",
    "**/*.lib",
]

[tool.setuptools.dynamic]
readme = {{file = ["README.md"], content-type = "text/markdown"}}

[project.entry-points.pyinstaller40]
hook-dirs = "{library_data.import_name}.__pyinstaller:get_hook_dirs"

[tool.versioneer]
VCS = "git"
style = "pep440"
versionfile_source = "src/{library_data.import_name.replace(".", "/")}/_version.py"
versionfile_build = "{library_data.import_name.replace(".", "/")}/_version.py"
tag_prefix = ""
parentdir_prefix = "{library_data.pypi_name.replace("-", "_")}-"
"""
        )
