import os

from .data import LibraryData, PythonVersion


def write(project_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(project_path, "mypy.ini"), "w", encoding="utf-8") as f:
        f.write(f"""[mypy]
disallow_untyped_defs = True
check_untyped_defs = True
warn_return_any = True
python_version = {PythonVersion}
explicit_package_bases = True
mypy_path = $MYPY_CONFIG_FILE_DIR/src,$MYPY_CONFIG_FILE_DIR/tests
files =
    src,
    tests,
    tools,
    get_compiler,
    build_requires.py,
    requirements.py,
    setup.py
""")
