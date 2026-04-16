#include <pybind11/pybind11.h>

#include <amulet/pybind11_extensions/compatibility.hpp>

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

void init_amulet_level(py::module);

static void _init_amulet_level(py::module m)
{
    pyext::init_compiler_config(m);
    pyext::check_compatibility(py::module::import("amulet.leveldb"), m);
    pyext::check_compatibility(py::module::import("amulet.utils"), m);
    pyext::check_compatibility(py::module::import("amulet.zlib"), m);
    pyext::check_compatibility(py::module::import("amulet.nbt"), m);
    pyext::check_compatibility(py::module::import("amulet.core"), m);
    pyext::check_compatibility(py::module::import("amulet.game"), m);
    pyext::check_compatibility(py::module::import("amulet.anvil"), m);
    init_amulet_level(m);
}

PYBIND11_MODULE(_amulet_level, m)
{
    m.def("init", &_init_amulet_level, py::arg("m"));
}
