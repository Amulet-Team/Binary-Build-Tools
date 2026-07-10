import os

from .data import LibraryData, libraries, PythonVersion, find_dependencies


def write(project_path: str, library_data: LibraryData) -> None:
    dependencies = find_dependencies(library_data.pypi_name, True, True, True, False, True, True, False, False)
    shared_libs = [lib.lib_name for lib in dependencies if lib.lib_name]
    with open(os.path.join(project_path, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(f"""[build-system]
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
{"\n".join(f"    {{name = \"{name}\"}}," for name in library_data.authors)}
]
description = "{library_data.description}"
dynamic = ["version", "readme", "dependencies"]
requires-python = ">={PythonVersion}"
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
]{"".join(f"\n{group} = [\n{"".join(f"    \"{dep}\",\n" for dep in deps)}]" for group, deps in library_data.optional_dependencies.items())}

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
{"".join(f"    \"{line}\",\n" for line in library_data.package_data)}]

[tool.setuptools.dynamic]
readme = {{file = ["README.md"], content-type = "text/markdown"}}

[project.entry-points.pyinstaller40]
hook-dirs = "{library_data.import_name}.__pyinstaller:get_hook_dirs"

{
f"""\
[project.entry-points.console_scripts]
{"\n".join(f"{name} = \"{func}\"" for name, func in library_data.console_scripts.items())}

""" if library_data.console_scripts else ""
}\
{
f"""\
[project.entry-points.gui_scripts]
{"\n".join(f"{name} = \"{func}\"" for name, func in library_data.gui_scripts.items())}

""" if library_data.gui_scripts else ""
}\
[tool.versioneer]
VCS = "git"
style = "pep440"
versionfile_source = "src/{library_data.import_name.replace(".", "/")}/_version.py"
versionfile_build = "{library_data.import_name.replace(".", "/")}/_version.py"
tag_prefix = ""
parentdir_prefix = "{library_data.pypi_name.replace("-", "_")}-"

[tool.cibuildwheel]
test-sources = ["tests", "tools/compile_tests.py"]
{f"test-extras = [{",".join(map("\"{}\"".format, library_data.unittest_dep_groups))}]\n" if library_data.unittest_dep_groups else ""}\
{f"before-test = [{",".join(map("\"{}\"".format, library_data.unittests_pre_test))}]\n" if library_data.unittests_pre_test else ""}\
test-command = [
    "python -m venv venv_build",
    "venv_build/bin/pip install {{wheel}}[dev]",
    "venv_build/bin/python tools/compile_tests.py",
    "python -m unittest discover -s tests"
]

manylinux-x86_64-image = "manylinux_2_34"

[tool.cibuildwheel.linux]
before-all = "yum install -y cmake{"".join(f" {lib}" for lib in library_data.unittests_linux_libs)}"
{f"""repair-wheel-command = "auditwheel repair{"".join(f" --exclude lib{lib}.so" for lib in shared_libs)} -w {{dest_dir}} {{wheel}}"
""" if shared_libs else ""}\

{f"""\
[tool.cibuildwheel.macos]
repair-wheel-command = "delocate-wheel --require-archs {{delocate_archs}} --ignore-missing-dependencies{"".join(f" --exclude lib{lib}.dylib" for lib in shared_libs)} -w {{dest_dir}} -v {{wheel}}"

""" if shared_libs else ""}\
[tool.cibuildwheel.windows]
repair-wheel-command = "delvewheel repair --ignore-existing --exclude {f"\\\"msvcp140.dll{"".join(f";{lib}.dll" for lib in shared_libs)}\\\"" if shared_libs else "msvcp140.dll"} -w {{dest_dir}} -v {{wheel}}"
test-command = [
    "python -m venv venv_build",
    "venv_build\\\\Scripts\\\\pip install {{wheel}}[dev]",
    "venv_build\\\\Scripts\\\\python tools/compile_tests.py",
    "python -m unittest discover -s tests"
]
""")
