from binary_build_tools.data import LibraryData

from . import (
    make_pyinstaller,
    make_versioneer,
    make_init,
    make_ext,
    make_cmake_config,
    make_py_typed,
)

def write(package_path: str, library_data: LibraryData) -> None:
    make_pyinstaller.write(package_path, library_data)
    make_versioneer.write(package_path, library_data)
    make_init.write(package_path, library_data)
    make_ext.write(package_path, library_data)
    make_cmake_config.write(package_path, library_data)
    make_py_typed.write(package_path)
