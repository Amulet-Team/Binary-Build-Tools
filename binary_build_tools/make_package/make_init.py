import os

from binary_build_tools.data import LibraryData, LibraryType, find_dependencies


def write(package_path: str, library_data: LibraryData) -> None:
    dependencies = tuple(
        lib
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
        if lib.library_type == LibraryType.Shared
    )

    with open(os.path.join(package_path, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f"""import logging as _logging

from . import _version

__version__ = _version.get_versions()["version"]

# init a default logger
_logging.basicConfig(level=_logging.INFO, format="%(levelname)s - %(message)s")


def _init() -> None:
    import os
    import sys

    if os.environ.get("AMULET_SKIP_COMPILE", None):
        return

{f"""\
    # Import dependencies
{"".join(f"    import {lib.import_name}\n" for lib in dependencies)}
""" if dependencies else ""}\

    from .{library_data.ext_name} import init

    init(sys.modules[__name__])


_init()
del _init
""")
