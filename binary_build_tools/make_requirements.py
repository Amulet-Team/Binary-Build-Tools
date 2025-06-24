import os

from .data import LibraryData, libraries, library_order


def write(project_path: str, library_data: LibraryData) -> None:
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
            f'''import os
import amulet_compiler_version
from packaging.version import Version

AMULET_COMPILER_TARGET_REQUIREMENT = "==2.0"
AMULET_COMPILER_VERSION_REQUIREMENT = "==3.0.0"

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


if os.environ.get("AMULET_FREEZE_COMPILER", None):
    AMULET_COMPILER_VERSION_REQUIREMENT = f"=={{amulet_compiler_version.__version__}}"{
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
