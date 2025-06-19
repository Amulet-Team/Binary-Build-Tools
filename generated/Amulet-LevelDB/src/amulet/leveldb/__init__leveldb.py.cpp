#include <pybind11/pybind11.h>

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

static void init_module(py::module m)
{
    py::dict compiler_config;
    compiler_config["pybind11_version"] = PYBIND11_VERSION;
    compiler_config["compiler_id"] = COMPILER_ID;
    compiler_config["compiler_version"] = COMPILER_VERSION;
    m.attr("compiler_config") = compiler_config;
}

PYBIND11_MODULE(_leveldb, m)
{
    py::options options;
    options.disable_function_signatures();
    m.def("init", &init_module, py::doc("init(arg0: types.ModuleType) -> None"));
    options.enable_function_signatures();
}
