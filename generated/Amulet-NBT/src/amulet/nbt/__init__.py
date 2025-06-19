from __future__ import annotations
from . import _version

__version__ = _version.get_versions()["version"]


def _init() -> None:
    import os
    import sys
    import ctypes

    if sys.platform == "win32":
        lib_path = os.path.join(os.path.dirname(__file__), "amulet_nbt.dll")
    elif sys.platform == "darwin":
        lib_path = os.path.join(os.path.dirname(__file__), "libamulet_nbt.dylib")
    elif sys.platform == "linux":
        lib_path = os.path.join(os.path.dirname(__file__), "libamulet_nbt.so")
    else:
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    # Import dependencies
    import amulet.zlib

    # Load the shared library
    ctypes.cdll.LoadLibrary(lib_path)

    from ._amulet_nbt import init

    init(sys.modules[__name__])


_init()
