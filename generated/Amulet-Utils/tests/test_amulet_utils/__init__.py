if __name__ != "test_amulet_utils":
    raise RuntimeError(
        f"Module name is incorrect. Expected: 'test_amulet_utils' got '{__name__}'"
    )


import faulthandler as _faulthandler

_faulthandler.enable()


def _init() -> None:
    import sys

    # Import dependencies
    import amulet.utils

    # This needs to be an absolute path otherwise it may get called twice
    # on different module objects and crash when the interpreter shuts down.
    from test_amulet_utils._test_amulet_utils import init

    init(sys.modules[__name__])


_init()
