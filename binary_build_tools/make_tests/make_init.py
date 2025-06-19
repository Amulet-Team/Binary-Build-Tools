import os

from binary_build_tools.data import LibraryData


def write(test_package_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(test_package_path, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f"""if __name__ != "test_{library_data.import_name.replace('.', '_')}":
    raise RuntimeError(
        f"Module name is incorrect. Expected: 'test_{library_data.import_name.replace('.', '_')}' got '{{__name__}}'"
    )


import faulthandler

faulthandler.enable()


def _init() -> None:
    import sys

    # Import dependencies
    import {library_data.import_name}

    # This needs to be an absolute path otherwise it may get called twice
    # on different module objects and crash when the interpreter shuts down.
    from test_{library_data.import_name.replace('.', '_')}._test_{library_data.import_name.replace('.', '_')} import init

    init(sys.modules[__name__])


_init()
""")
