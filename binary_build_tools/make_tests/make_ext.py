import os

from binary_build_tools.data import LibraryData


def write(test_package_path: str, library_data: LibraryData) -> None:
    if library_data.lib_name is None:
        return
    with open(
        os.path.join(
            test_package_path,
            f"_test_{library_data.import_name.replace('.', '_')}.py.cpp",
        ),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"""#include <pybind11/pybind11.h>

#include <amulet/pybind11_extensions/compatibility.hpp>

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

void init_test_{library_data.import_name.replace(".", "_")}(py::module);

static void _init_test_{library_data.import_name.replace(".", "_")}(py::module m){{
    pyext::init_compiler_config(m);
    pyext::check_compatibility(py::module::import("{library_data.import_name}"), m);
    init_test_{library_data.import_name.replace(".", "_")}(m);
}}

PYBIND11_MODULE(_test_{library_data.import_name.replace('.', '_')}, m) {{
    m.def("init", &_init_test_{library_data.import_name.replace(".", "_")}, py::arg("m"));
}}
""")
