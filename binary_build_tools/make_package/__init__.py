from binary_build_tools.data import LibraryData

from . import (
    make_pyinstaller,
    make_versioneer,
)

def write(package_path: str, library_data: LibraryData) -> None:
    make_pyinstaller.write(package_path, library_data)
    make_versioneer.write(package_path, library_data)
