import sys
import subprocess
import os
import shutil

import pybind11
import amulet.pybind11_extensions
import amulet.io
import amulet.nbt
import amulet.core
import amulet.test_utils


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

    if subprocess.run(
        [
            "cmake",
            *platform_args,
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-Dpybind11_DIR={fix_path(pybind11.get_cmake_dir())}",
            f"-Damulet_pybind11_extensions_DIR={fix_path(amulet.pybind11_extensions.__path__[0])}",
            f"-Damulet_io_DIR={fix_path(amulet.io.__path__[0])}",
            f"-Damulet_nbt_DIR={fix_path(amulet.nbt.__path__[0])}",
            f"-Damulet_core_DIR={fix_path(amulet.core.__path__[0])}",
            f"-Damulet_game_DIR={fix_path(os.path.join(RootDir, 'src', 'amulet', 'game'))}",
            f"-Damulet_test_utils_DIR={fix_path(amulet.test_utils.__path__[0])}",
            f"-DCMAKE_INSTALL_PREFIX=install",
            f"-DBUILD_AMULET_GAME_TESTS=",
            "-B",
            "build",
        ]
    ).returncode:
        raise RuntimeError("Error configuring amulet_game")


if __name__ == "__main__":
    main()
