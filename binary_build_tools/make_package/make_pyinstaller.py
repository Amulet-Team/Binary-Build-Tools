import os

from binary_build_tools.data import LibraryData


def write(package_path: str, library_data: LibraryData) -> None:
    pyinstaller_path = os.path.join(package_path, "__pyinstaller")
    os.makedirs(pyinstaller_path, exist_ok=True)
    with open(os.path.join(pyinstaller_path, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("""def get_hook_dirs() -> list[str]:
    return __path__
""")
    with open(os.path.join(pyinstaller_path, f"hook-{library_data.import_name}.py"), "w", encoding="utf-8") as f:
        f.write(
            f"""from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules("{library_data.import_name}")
datas = collect_data_files("{library_data.import_name}")
"""
        )
