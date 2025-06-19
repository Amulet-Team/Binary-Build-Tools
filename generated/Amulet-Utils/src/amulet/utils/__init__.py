import logging

from . import _version

__version__ = _version.get_versions()["version"]

# init a default logger
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def _init() -> None:
    import os
    import sys
    import ctypes

    if sys.platform == "win32":
        lib_path = os.path.join(os.path.dirname(__file__), "amulet_utils.dll")
    elif sys.platform == "darwin":
        lib_path = os.path.join(os.path.dirname(__file__), "libamulet_utils.dylib")
    elif sys.platform == "linux":
        lib_path = os.path.join(os.path.dirname(__file__), "libamulet_utils.so")
    else:
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    # Load the shared library
    ctypes.cdll.LoadLibrary(lib_path)

    from ._amulet_utils import init

    init(sys.modules[__name__])


_init()
