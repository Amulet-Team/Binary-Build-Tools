import os

from .data import LibraryData, libraries, library_order, find_dependencies


def write(project_path: str, library_data: LibraryData) -> None:
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

    py_dependencies: tuple[LibraryData, ...] = tuple(
        libraries[pypi_name]
        for pypi_name in sorted(
            library_data.runtime_dependencies, key=library_order.__getitem__
        )
    )

    with open(
        os.path.join(project_path, "requirements.py"), "w", encoding="utf-8"
    ) as f:
        f.write(
            f'''\
import os
from packaging.version import Version
import get_compiler

AMULET_COMPILER_TARGET_REQUIREMENT = "==2.0"

{
"\n".join(
    f'{lib.var_name.upper()}_REQUIREMENT = "{lib.specifier}"'
    for lib in dependencies + py_dependencies
)
}{
"".join(
    f"""

if os.environ.get("{lib.var_name.upper()}_REQUIREMENT", None):
    {lib.var_name.upper()}_REQUIREMENT = (
        f"{{{lib.var_name.upper()}_REQUIREMENT}},{{os.environ['{lib.var_name.upper()}_REQUIREMENT']}}"
    )"""
    for lib in dependencies if lib.pypi_name != "pybind11"
)
}


def get_specifier_set(version_str: str) -> str:
    """
    version_str: The PEP 440 version number of the library.
    """
    version = Version(version_str)
    if version.epoch != 0 or version.is_devrelease or version.is_postrelease:
        raise RuntimeError(f"Unsupported version format. {{version_str}}")

    return f"~={{version.major}}.{{version.minor}}.{{version.micro}}.0{{''.join(map(str, version.pre or ()))}}"

AMULET_COMPILER_VERSION_REQUIREMENT = get_compiler.main()

{
"".join(
f"""

try:
    import {lib.import_name}
except ImportError:
    pass
else:
    {lib.var_name.upper()}_REQUIREMENT = get_specifier_set({lib.import_name}.__version__)"""
for lib in dependencies if lib.pypi_name != "pybind11"
)
}


def get_build_dependencies() -> list:
    return [
        f"amulet-compiler-version{{AMULET_COMPILER_VERSION_REQUIREMENT}}",{
"".join(
    f"""
        f"{lib.pypi_name}{{{lib.var_name.upper()}_REQUIREMENT}}","""
    for lib in dependencies
)    
}
    ] * (not os.environ.get("AMULET_SKIP_COMPILE", None))


def get_runtime_dependencies() -> list[str]:
    return [
        f"amulet-compiler-target{{AMULET_COMPILER_TARGET_REQUIREMENT}}",
        f"amulet-compiler-version{{AMULET_COMPILER_VERSION_REQUIREMENT}}",{
"".join(
    f"""
        f"{lib.pypi_name}{{{lib.var_name.upper()}_REQUIREMENT}}","""
    for lib in dependencies + py_dependencies
)    
}
    ]
'''
        )
