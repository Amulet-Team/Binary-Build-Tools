import os

from binary_build_tools.data import LibraryData, libraries, library_order


def write(project_path: str, library_data: LibraryData) -> None:
    dependencies: list[LibraryData] = [
        libraries[pypi_name]
        for pypi_name in sorted(
            set(
                library_data.private_dependencies
                + library_data.public_dependencies
                + library_data.ext_dependencies
                + library_data.test_dependencies
            ),
            key=library_order.__getitem__,
        )
    ]

    with open(os.path.join(project_path, "cmake_generate.py"), "w", encoding="utf-8") as f:
        f.write(
            f"""import sys
import subprocess
import os
import shutil

{"\n".join(f"import {lib.import_name}" for lib in dependencies)}


def fix_path(path: str) -> str:
    return os.path.realpath(path).replace(os.sep, "/")


RootDir = fix_path(os.path.dirname(os.path.dirname(__file__)))


def main():
    platform_args = []
    if sys.platform == "win32":
        platform_args.extend(["-G", "Visual Studio 17 2022"])
        if sys.maxsize > 2**32:
            platform_args.extend(["-A", "x64"])
        else:
            platform_args.extend(["-A", "Win32"])
        platform_args.extend(["-T", "v143"])

    os.chdir(RootDir)
    shutil.rmtree(os.path.join(RootDir, "build", "CMakeFiles"), ignore_errors=True)

    if subprocess.run(["cmake", "--version"]).returncode:
        raise RuntimeError("Could not find cmake")
    if subprocess.run(
        [
            "cmake",
            *platform_args,
            f"-DPYTHON_EXECUTABLE={{sys.executable}}",{
                "".join(
                    '\n                f"-Dpybind11_DIR={fix_path(pybind11.get_cmake_dir())}",'
                    if lib.pypi_name == "pybind11" else
                    f'\n                f"-D{lib.cmake_package}_DIR={{fix_path({lib.import_name}.__path__[0])}}",' for lib in dependencies
                )}
            f"-D{library_data.cmake_package}_DIR={{fix_path(os.path.join(RootDir, 'src', {", ".join(f"'{name}'" for name in library_data.import_name.split("."))}))}}",
            f"-DCMAKE_INSTALL_PREFIX=install",
            f"-DBUILD_{library_data.var_name.upper()}_TESTS=",
            "-B",
            "build",
        ]
    ).returncode:
        raise RuntimeError("Error configuring {library_data.pypi_name}")


if __name__ == "__main__":
    main()
"""
        )
