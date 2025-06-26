import os

from binary_build_tools.data import (
    LibraryData,
    libraries,
    library_order,
    find_dependencies,
)


def write(tools_path: str, library_data: LibraryData) -> None:
    dependencies = find_dependencies(
        library_data.pypi_name,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        False,
    )

    with open(os.path.join(tools_path, "compile_tests.py"), "w", encoding="utf-8") as f:
        f.write(
            f"""import subprocess
import sys
import shutil
import os

{"\n".join(f"import {lib.import_name}" for lib in dependencies)}
import {library_data.import_name}


def fix_path(path: str) -> str:
    return os.path.realpath(path).replace(os.sep, "/")


RootDir = os.path.dirname(os.path.dirname(__file__))
TestsDir = os.path.join(RootDir, "tests")


def main() -> None:
    platform_args = []
    if sys.platform == "win32":
        platform_args.extend(["-G", "Visual Studio 17 2022"])
        if sys.maxsize > 2**32:
            platform_args.extend(["-A", "x64"])
        else:
            platform_args.extend(["-A", "Win32"])
        platform_args.extend(["-T", "v143"])

    os.chdir(TestsDir)
    shutil.rmtree(os.path.join(TestsDir, "build", "CMakeFiles"), ignore_errors=True)

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
            f"-D{library_data.cmake_package}_DIR={{fix_path({library_data.import_name}.__path__[0])}}",
            f"-DCMAKE_INSTALL_PREFIX=install",
            "-B",
            "build",
        ]
    ).returncode:
        raise RuntimeError("Error configuring test-{library_data.pypi_name}")
    if subprocess.run(
        ["cmake", "--build", "build", "--config", "RelWithDebInfo"]
    ).returncode:
        raise RuntimeError("Error building test-{library_data.pypi_name}")
    if subprocess.run(
        ["cmake", "--install", "build", "--config", "RelWithDebInfo"]
    ).returncode:
        raise RuntimeError("Error installing test-{library_data.pypi_name}")


if __name__ == "__main__":
    main()
"""
        )
