import os

from binary_build_tools.data import LibraryData, libraries, library_order


def write(tests_path: str, library_data: LibraryData) -> None:
    if library_data.lib_name is None:
        return
    with open(os.path.join(tests_path, "CMakeLists.txt"), "w", encoding="utf-8") as f:
        f.write(f"""cmake_minimum_required(VERSION 4.1)

project({library_data.cmake_package}_tests LANGUAGES CXX)

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

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

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
set_target_properties(_test_{library_data.cmake_package} PROPERTIES CXX_VISIBILITY_PRESET hidden)
set_target_properties(_test_{library_data.cmake_package} PROPERTIES FOLDER "Tests")
target_compile_definitions(_test_{library_data.cmake_package} PRIVATE PYBIND11_DETAILED_ERROR_MESSAGES)
target_compile_definitions(_test_{library_data.cmake_package} PRIVATE PYBIND11_VERSION="${{pybind11_VERSION}}")
target_compile_definitions(_test_{library_data.cmake_package} PRIVATE COMPILER_ID="${{CMAKE_CXX_COMPILER_ID}}")
target_compile_definitions(_test_{library_data.cmake_package} PRIVATE COMPILER_VERSION="${{CMAKE_CXX_COMPILER_VERSION}}"){
"".join(
    f"""
target_link_libraries(_test_{library_data.cmake_package} PRIVATE {libraries[lib_name].cmake_lib_name})"""
    for lib_name in sorted(library_data.test_dependencies + (library_data.pypi_name,), key=library_order.__getitem__)
    if lib_name != "pybind11" and libraries[lib_name].cmake_lib_name is not None
)
}
target_sources(_test_{library_data.cmake_package} PRIVATE ${{SOURCES}})
foreach(FILE ${{SOURCES}})
    file(RELATIVE_PATH REL_PATH ${{CMAKE_CURRENT_LIST_DIR}} ${{FILE}})
    get_filename_component(GROUP ${{REL_PATH}} DIRECTORY)
    string(REPLACE "/" "\\\\" GROUP "${{GROUP}}")
    source_group(${{GROUP}} FILES ${{FILE}})
endforeach()

# Install
install(TARGETS _test_{library_data.cmake_package} DESTINATION "${{CMAKE_CURRENT_LIST_DIR}}/test_{library_data.cmake_package}")
""")
