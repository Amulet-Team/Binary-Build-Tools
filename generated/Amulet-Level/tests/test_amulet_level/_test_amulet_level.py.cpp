#include <pybind11/pybind11.h>

#include <amulet/pybind11_extensions/compatibility.hpp>

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

void init_test_amulet_level(py::module);

static void _init_test_amulet_level(py::module m){
    pyext::init_compiler_config(m);
    pyext::check_compatibility(py::module::import("amulet.level"), m);
    init_test_amulet_level(m);
}

PYBIND11_MODULE(_test_amulet_level, m) {
    m.def("init", &_init_test_amulet_level, py::arg("m"));
}
