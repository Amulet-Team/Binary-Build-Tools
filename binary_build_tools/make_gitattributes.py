import os

from .data import LibraryData


def write(project_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(project_path, ".gitattributes"), "w", encoding="utf-8") as f:
        f.write(
            f"""# Auto detect text files and perform LF normalization
* text=auto
src/{library_data.import_name.replace(".", "/")}/_version.py export-subst
"""
        )
