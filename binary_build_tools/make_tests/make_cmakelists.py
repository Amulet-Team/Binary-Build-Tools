import os

from binary_build_tools.data import LibraryData, libraries, library_order


def get_module_properties(module_name: str, library_data: LibraryData, indent: str = "") -> str:
    return f"""\
set_target_properties({module_name} PROPERTIES CXX_VISIBILITY_PRESET hidden)
{indent}set_target_properties({module_name} PROPERTIES FOLDER "Tests")
{indent}target_compile_definitions({module_name} PRIVATE PYBIND11_DETAILED_ERROR_MESSAGES)
{indent}target_compile_definitions({module_name} PRIVATE PYBIND11_VERSION="${{pybind11_VERSION}}")
{indent}target_compile_definitions({module_name} PRIVATE COMPILER_ID="${{CMAKE_CXX_COMPILER_ID}}")
{indent}target_compile_definitions({module_name} PRIVATE COMPILER_VERSION="${{CMAKE_CXX_COMPILER_VERSION}}"){
"".join(
    f"""
{indent}target_link_libraries({module_name} PRIVATE {libraries[lib_name].cmake_lib_name})"""
    for lib_name in sorted(library_data.test_dependencies + (library_data.pypi_name,), key=library_order.__getitem__)
    if lib_name != "pybind11" and libraries[lib_name].cmake_lib_name is not None
)
}
{indent}target_sources({module_name} PRIVATE ${{SOURCES}})
"""

def write(tests_path: str, library_data: LibraryData) -> None:
    if library_data.lib_name is None:
        return
    with open(os.path.join(tests_path, "CMakeLists.txt"), "w", encoding="utf-8") as f:
        f.write(f"""cmake_minimum_required(VERSION 4.1)

project({library_data.cmake_package}_tests LANGUAGES CXX)

option(THREAD_SAFETY_ANALYSIS "Run clang thread safety analysis over the sources before building" OFF)

if(THREAD_SAFETY_ANALYSIS AND NOT CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    message(FATAL_ERROR "THREAD_SAFETY_ANALYSIS requires Clang")
endif()

# Set C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set platform variables
if (WIN32)
	# set windows 7 as the minimum version
	add_definitions(-D_WIN32_WINNT=0x0601)
elseif(APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.15")
elseif(UNIX)
    set(CMAKE_POSITION_INDEPENDENT_CODE ON)
else()
    message( FATAL_ERROR "Unsupported platform. Please submit a pull request to support this platform." )
endif()

find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)

# Find dependencies{
"".join(
    f"""
if (NOT TARGET {libraries[lib_name].cmake_lib_name})
    find_package({libraries[lib_name].cmake_package} CONFIG REQUIRED)
endif()"""
    for lib_name in sorted(library_data.test_dependencies + (library_data.pypi_name,), key=library_order.__getitem__)
    if libraries[lib_name].cmake_lib_name is not None
)
}

# Find sources
file(GLOB_RECURSE SOURCES LIST_DIRECTORIES false "${{CMAKE_CURRENT_LIST_DIR}}/*.py.cpp")

pybind11_add_module(_test_{library_data.cmake_package})
{get_module_properties(f"_test_{library_data.cmake_package}", library_data)}\
foreach(FILE ${{SOURCES}})
    file(RELATIVE_PATH REL_PATH ${{CMAKE_CURRENT_LIST_DIR}} ${{FILE}})
    get_filename_component(GROUP ${{REL_PATH}} DIRECTORY)
    string(REPLACE "/" "\\\\" GROUP "${{GROUP}}")
    source_group(${{GROUP}} FILES ${{FILE}})
endforeach()

if(THREAD_SAFETY_ANALYSIS)
    add_library(_test_{library_data.cmake_package}_thread_analysis OBJECT)
    target_link_libraries({library_data.cmake_package}_thread_analysis PRIVATE pybind11::module)
    {get_module_properties(f"{library_data.cmake_package}_thread_analysis", library_data, indent="\t")}\
    target_compile_options({library_data.cmake_package}_thread_analysis PRIVATE -fsyntax-only -Wthread-safety -Werror=thread-safety)
    add_dependencies(_test_{library_data.cmake_package} _test_{library_data.cmake_package}_thread_analysis)
endif()

# Install
install(TARGETS _test_{library_data.cmake_package} DESTINATION "${{CMAKE_CURRENT_LIST_DIR}}/test_{library_data.cmake_package}")
""")
