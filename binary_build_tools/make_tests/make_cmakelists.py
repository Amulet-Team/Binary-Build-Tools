import os

from binary_build_tools.data import LibraryData


def write(tests_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(tests_path, "CMakeLists.txt"), "w", encoding="utf-8") as f:
        f.write(
            f"""cmake_minimum_required(VERSION 3.13)

project({library_data.var_name}_tests LANGUAGES CXX)

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
else()
    set(CMAKE_POSITION_INDEPENDENT_CODE ON)
endif()

# Find dependencies
find_package(pybind11 CONFIG REQUIRED)
find_package(amulet_pybind11_extensions CONFIG REQUIRED)
find_package({library_data.lib_name} CONFIG REQUIRED)
find_package(amulet_test_utils CONFIG REQUIRED)

# Find sources
file(GLOB_RECURSE SOURCES LIST_DIRECTORIES false "${{CMAKE_CURRENT_LIST_DIR}}/*.py.cpp")

pybind11_add_module(_test_{library_data.var_name})
target_compile_definitions(_test_{library_data.var_name} PRIVATE PYBIND11_DETAILED_ERROR_MESSAGES)
target_compile_definitions(_test_{library_data.var_name} PRIVATE PYBIND11_VERSION="${{pybind11_VERSION}}")
target_compile_definitions(_test_{library_data.var_name} PRIVATE COMPILER_ID="${{CMAKE_CXX_COMPILER_ID}}")
target_compile_definitions(_test_{library_data.var_name} PRIVATE COMPILER_VERSION="${{CMAKE_CXX_COMPILER_VERSION}}")
target_link_libraries(_test_{library_data.var_name} PRIVATE amulet_pybind11_extensions)
target_link_libraries(_test_{library_data.var_name} PRIVATE {library_data.lib_name})
target_link_libraries(_test_{library_data.var_name} PRIVATE amulet_test_utils)
target_sources(_test_{library_data.var_name} PRIVATE ${{SOURCES}})
foreach(FILE ${{SOURCES}})
    file(RELATIVE_PATH REL_PATH ${{CMAKE_CURRENT_LIST_DIR}} ${{FILE}})
    get_filename_component(GROUP ${{REL_PATH}} DIRECTORY)
    string(REPLACE "/" "\\\\" GROUP "${{GROUP}}")
    source_group(${{GROUP}} FILES ${{FILE}})
endforeach()

# Install
install(TARGETS _test_{library_data.var_name} DESTINATION "${{CMAKE_CURRENT_LIST_DIR}}/test_{library_data.var_name}")
"""
        )
