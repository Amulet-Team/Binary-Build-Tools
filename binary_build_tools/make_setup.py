import os

from .data import LibraryData, find_dependencies


def write(project_path: str, library_data: LibraryData) -> None:
    dependencies = find_dependencies(
        library_data.pypi_name,
        True,
        True,
        True,
        False,
        False,
        True,
        False,
        False,
    )

    with open(os.path.join(project_path, "setup.py"), "w", encoding="utf-8") as f:
        f.write(
            f"""import os
import subprocess
import sys
from pathlib import Path
import platform
from tempfile import TemporaryDirectory
from typing import TypeAlias, TYPE_CHECKING

from setuptools import setup, Extension, Command
from setuptools.command.build_ext import build_ext

import versioneer

import requirements


def fix_path(path: str | os.PathLike[str]) -> str:
    return os.path.realpath(path).replace(os.sep, "/")


cmdclass: dict[str, type[Command]] = versioneer.get_cmdclass()

if TYPE_CHECKING:
    BuildExt: TypeAlias = build_ext
else:
    BuildExt = cmdclass.get("build_ext", build_ext)


class CMakeBuild(BuildExt):
    def build_extension(self, ext: Extension) -> None:
        {"\n        ".join(f"import {lib.import_name}" for lib in dependencies)}
    
        ext_dir = (Path.cwd() / self.get_ext_fullpath("")).parent.resolve() / {" / ".join(f"\"{name}\"" for name in library_data.import_name.split("."))}
        {library_data.short_var_name}_src_dir = Path.cwd() / "src" / {" / ".join(f"\"{name}\"" for name in library_data.import_name.split("."))} if self.editable_mode else ext_dir

        platform_args = []
        if sys.platform == "win32":
            platform_args.extend(["-G", "Visual Studio 17 2022"])
            if sys.maxsize > 2**32:
                platform_args.extend(["-A", "x64"])
            else:
                platform_args.extend(["-A", "Win32"])
            platform_args.extend(["-T", "v143"])
        elif sys.platform == "darwin":
            if platform.machine() == "arm64":
                platform_args.append("-DCMAKE_OSX_ARCHITECTURES=x86_64;arm64")

        if subprocess.run(["cmake", "--version"]).returncode:
            raise RuntimeError("Could not find cmake")
        with TemporaryDirectory() as tempdir:
            if subprocess.run(
                [
                    "cmake",
                    *platform_args,
                    f"-DPYTHON_EXECUTABLE={{sys.executable}}",
                    {"".join(
                        """
                    f"-Dpybind11_DIR={fix_path(pybind11.get_cmake_dir())}","""
                        if lib.pypi_name == "pybind11" else
                        f"""
                    f"-D{lib.cmake_package}_DIR={{fix_path({lib.import_name}.__path__[0])}}",""" for lib in dependencies
                    )}
                    f"-D{library_data.cmake_package}_DIR={{fix_path({library_data.short_var_name}_src_dir)}}",
                    f"-D{library_data.import_name.replace(".", "_").upper()}_EXT_DIR={{fix_path(ext_dir)}}",
                    f"-DCMAKE_INSTALL_PREFIX=install",
                    "-B",
                    tempdir,
                ]
            ).returncode:
                raise RuntimeError("Error configuring {library_data.pypi_name}")
            if subprocess.run(
                ["cmake", "--build", tempdir, "--config", "Release"]
            ).returncode:
                raise RuntimeError("Error building {library_data.pypi_name}")
            if subprocess.run(
                ["cmake", "--install", tempdir, "--config", "Release"]
            ).returncode:
                raise RuntimeError("Error installing {library_data.pypi_name}")


cmdclass["build_ext"] = CMakeBuild  # type: ignore


setup(
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    ext_modules=[Extension("{library_data.import_name}.{library_data.ext_name}", [])] * (not os.environ.get("AMULET_SKIP_COMPILE", None)),
    install_requires=requirements.get_runtime_dependencies(),
)
"""
        )
