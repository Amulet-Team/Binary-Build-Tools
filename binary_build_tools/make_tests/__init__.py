import os

from binary_build_tools.data import LibraryData
from . import (
    make_init,
    make_ext,
)


def write(tests_path: str, library_data: LibraryData) -> None:
    test_package_path = os.path.join(
        tests_path, f"test_{library_data.import_name.replace('.', '_')}"
    )
    os.makedirs(test_package_path, exist_ok=True)
    make_init.write(test_package_path, library_data)
    make_ext.write(test_package_path, library_data)
