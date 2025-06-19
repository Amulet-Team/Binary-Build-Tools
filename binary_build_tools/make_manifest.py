import os

from .data import LibraryData


def write(project_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(project_path, "MANIFEST.in"), "w", encoding="utf-8") as f:
        f.write(
            f"""include build_requires.py
include requirements.py

recursive-include src/{library_data.root_import_name} *.cpp *.hpp *Config.cmake

include CMakeLists.txt

prune tests
"""
        )
