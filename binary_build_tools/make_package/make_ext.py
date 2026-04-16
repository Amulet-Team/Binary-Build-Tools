import os

from binary_build_tools.data import LibraryData, LibraryType, find_dependencies


def write(package_path: str, library_data: LibraryData) -> None:
    dependencies = tuple(
        lib
        for lib in find_dependencies(
            library_data.pypi_name,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            False,
        )
        if lib.library_type == LibraryType.Shared
    )

    with open(
        os.path.join(package_path, f"{library_data.ext_name}.py.cpp"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"""\
#include <pybind11/pybind11.h>

#include <amulet/pybind11_extensions/compatibility.hpp>

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

void init_{library_data.import_name.replace(".", "_")}(py::module);

static void _init_{library_data.import_name.replace(".", "_")}(py::module m)
{{
    pyext::init_compiler_config(m);{
    "".join(f'\n    pyext::check_compatibility(py::module::import("{lib.import_name}"), m);' for lib in dependencies) if dependencies else ""}
    init_{library_data.import_name.replace(".", "_")}(m);
}}

PYBIND11_MODULE({library_data.ext_name}, m)
{{
    m.def("init", &_init_{library_data.import_name.replace(".", "_")}, py::arg("m"));
}}
""")
