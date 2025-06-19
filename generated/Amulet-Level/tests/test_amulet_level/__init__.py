if __name__ != "test_amulet_level":
    raise RuntimeError(
        f"Module name is incorrect. Expected: 'test_amulet_level' got '{__name__}'"
    )


import faulthandler

faulthandler.enable()


def _init() -> None:
    import sys

    # Import dependencies
    import amulet.level

    # This needs to be an absolute path otherwise it may get called twice
    # on different module objects and crash when the interpreter shuts down.
    from test_amulet_level._test_amulet_level import init

    init(sys.modules[__name__])


_init()
