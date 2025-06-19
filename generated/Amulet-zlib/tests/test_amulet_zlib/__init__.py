def _init() -> None:
    import sys

    # Import dependencies
    import amulet.zlib

    # This needs to be an absolute path otherwise it may get called twice
    # on different module objects and crash when the interpreter shuts down.
    from tests.test_amulet_zlib._test_amulet_zlib import init

    init(sys.modules[__name__])


_init()
