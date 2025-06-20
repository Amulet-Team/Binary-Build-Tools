import os

from binary_build_tools.data import LibraryData

from . import make_stubgen, make_cmake_generate


def write(tools_path: str, library_data: LibraryData) -> None:
    make_stubgen.write(tools_path, library_data)
    make_cmake_generate.write(tools_path, library_data)
