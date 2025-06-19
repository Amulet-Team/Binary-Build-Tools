if __name__ != "test_amulet_game":
    raise RuntimeError(
        f"Module name is incorrect. Expected: 'test_amulet_game' got '{__name__}'"
    )


import faulthandler

faulthandler.enable()


def _init() -> None:
    import sys

    # Import dependencies
    import amulet.game

    # This needs to be an absolute path otherwise it may get called twice
    # on different module objects and crash when the interpreter shuts down.
    from test_amulet_game._test_amulet_game import init

    init(sys.modules[__name__])


_init()
