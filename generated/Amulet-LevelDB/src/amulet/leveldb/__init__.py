from __future__ import annotations

from . import _version

__version__ = _version.get_versions()["version"]


def _init() -> None:
    import os
    import sys
    import ctypes

    if sys.platform == "win32":
        lib_path = os.path.join(os.path.dirname(__file__), "leveldb_mcpe.dll")
    elif sys.platform == "darwin":
        lib_path = os.path.join(os.path.dirname(__file__), "libleveldb_mcpe.dylib")
    elif sys.platform == "linux":
        lib_path = os.path.join(os.path.dirname(__file__), "libleveldb_mcpe.so")
    else:
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    # Load the shared library
    ctypes.cdll.LoadLibrary(lib_path)

    from ._leveldb import init

    init(sys.modules[__name__])


_init()
