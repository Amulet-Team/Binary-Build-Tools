import logging as _logging

from . import _version

__version__ = _version.get_versions()["version"]

# init a default logger
_logging.basicConfig(level=_logging.INFO, format="%(levelname)s - %(message)s")


def _init() -> None:
    import os
    import sys
    import ctypes

    if sys.platform == "win32":
        lib_path = os.path.join(os.path.dirname(__file__), "amulet_editor.dll")
    elif sys.platform == "darwin":
        lib_path = os.path.join(os.path.dirname(__file__), "libamulet_editor.dylib")
    elif sys.platform == "linux":
        lib_path = os.path.join(os.path.dirname(__file__), "libamulet_editor.so")
    else:
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    # Import dependencies
    import amulet.leveldb
    import amulet.utils
    import amulet.zlib
    import amulet.nbt
    import amulet.core
    import amulet.resource_pack
    import amulet.game
    import amulet.anvil
    import amulet.level

    # Load the shared library
    ctypes.cdll.LoadLibrary(lib_path)

    from ._amulet_editor import init

    init(sys.modules[__name__])


_init()
