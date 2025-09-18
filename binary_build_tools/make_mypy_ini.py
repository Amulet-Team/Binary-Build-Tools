import os

from .data import LibraryData


def write(project_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(project_path, "mypy.ini"), "w", encoding="utf-8") as f:
        f.write(
            f"""[mypy]
disallow_untyped_defs = True
check_untyped_defs = True
warn_return_any = True
python_version = 3.12
mypy_path = $MYPY_CONFIG_FILE_DIR/src
packages = {library_data.root_import_name}
"""
        )
