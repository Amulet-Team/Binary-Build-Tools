import os

from binary_build_tools.data import LibraryData


def write(package_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(package_path, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f"""import logging

from . import _version

__version__ = _version.get_versions()["version"]

# init a default logger
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def _init() -> None:
    import os
    import sys
    import ctypes

    if sys.platform == "win32":
        lib_path = os.path.join(os.path.dirname(__file__), "{library_data.lib_name}.dll")
    elif sys.platform == "darwin":
        lib_path = os.path.join(os.path.dirname(__file__), "lib{library_data.lib_name}.dylib")
    elif sys.platform == "linux":
        lib_path = os.path.join(os.path.dirname(__file__), "lib{library_data.lib_name}.so")
    else:
        raise RuntimeError(f"Unsupported platform {{sys.platform}}")

    # Import dependencies

    # Load the shared library
    ctypes.cdll.LoadLibrary(lib_path)

    from .{library_data.ext_name} import init

    init(sys.modules[__name__])


_init()
""")
