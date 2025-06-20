import os

from .data import LibraryData, libraries, library_order


def write(project_path: str, library_data: LibraryData) -> None:
    found_dependencies: set[str] = set()
    lib_dependencies: list[tuple[LibraryData, bool]] = []
    for pypi_name in library_data.public_dependencies:
        if pypi_name in found_dependencies:
            continue
        lib_dependencies.append((libraries[pypi_name], True))
    for pypi_name in library_data.private_dependencies:
        if pypi_name in found_dependencies:
            continue
        lib_dependencies.append((libraries[pypi_name], False))
    lib_dependencies = sorted(lib_dependencies, key=lambda l: library_order[l[0].pypi_name])

    all_dependencies: list[LibraryData] = [
        libraries[pypi_name]
        for pypi_name in sorted(
            set(
                library_data.private_dependencies
                + library_data.public_dependencies
                + library_data.ext_dependencies
            ),
            key=library_order.__getitem__,
        )
    ]

    with open(os.path.join(project_path, "CMakeLists.txt"), "w", encoding="utf-8") as f:
        f.write(
            f"""cmake_minimum_required(VERSION 3.13)

project({library_data.cmake_package} LANGUAGES CXX)

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

if (MSVC)
    add_definitions("/MP")
endif()

# Find libraries{
f"".join(f"\nfind_package({lib.cmake_package} CONFIG REQUIRED)" for lib in all_dependencies)
}

# Find C++ files
file(REAL_PATH src SOURCE_PATH)
file(GLOB_RECURSE EXTENSION_SOURCES LIST_DIRECTORIES false ${{SOURCE_PATH}}/amulet/*.py.cpp)
file(GLOB_RECURSE EXTENSION_HEADERS LIST_DIRECTORIES false ${{SOURCE_PATH}}/amulet/*.py.hpp)
file(GLOB_RECURSE SOURCES LIST_DIRECTORIES false ${{SOURCE_PATH}}/amulet/*.cpp)
file(GLOB_RECURSE HEADERS LIST_DIRECTORIES false ${{SOURCE_PATH}}/amulet/*.hpp)
list(REMOVE_ITEM SOURCES ${{EXTENSION_SOURCES}})
list(REMOVE_ITEM HEADERS ${{EXTENSION_HEADERS}})

# Add implementation
add_library({library_data.lib_name} SHARED)
target_compile_definitions({library_data.lib_name} PRIVATE {library_data.export_symbol}){
    "".join(
        f"\ntarget_link_libraries({library_data.lib_name} {"PUBLIC" if public else "PRIVATE"} {lib.cmake_lib_name})"
        for lib, public in lib_dependencies
    )
}
target_include_directories({library_data.lib_name} PUBLIC ${{SOURCE_PATH}})
target_sources({library_data.lib_name} PRIVATE ${{SOURCES}} ${{HEADERS}})
foreach(FILE ${{SOURCES}} ${{HEADERS}})
    file(RELATIVE_PATH REL_PATH ${{SOURCE_PATH}} ${{FILE}})
    get_filename_component(GROUP ${{REL_PATH}} DIRECTORY)
    string(REPLACE "/" "\\\\" GROUP ${{GROUP}})
    source_group(${{GROUP}} FILES ${{FILE}})
endforeach()

# Add python extension
pybind11_add_module({library_data.ext_name}){
    "".join(
        f"\ntarget_link_libraries({library_data.ext_name} PRIVATE {libraries[lib].cmake_lib_name})"
        for lib in sorted(library_data.ext_dependencies + (library_data.pypi_name,), key=library_order.__getitem__)
        if lib != "pybind11"
    )
}
target_compile_definitions({library_data.ext_name} PRIVATE PYBIND11_DETAILED_ERROR_MESSAGES)
target_compile_definitions({library_data.ext_name} PRIVATE PYBIND11_VERSION="${{pybind11_VERSION}}")
target_compile_definitions({library_data.ext_name} PRIVATE COMPILER_ID="${{CMAKE_CXX_COMPILER_ID}}")
target_compile_definitions({library_data.ext_name} PRIVATE COMPILER_VERSION="${{CMAKE_CXX_COMPILER_VERSION}}")
target_sources({library_data.ext_name} PRIVATE ${{EXTENSION_SOURCES}} ${{EXTENSION_HEADERS}})
foreach(FILE ${{EXTENSION_SOURCES}} ${{EXTENSION_HEADERS}})
    file(RELATIVE_PATH REL_PATH ${{SOURCE_PATH}} ${{FILE}})
    get_filename_component(GROUP ${{REL_PATH}} DIRECTORY)
    string(REPLACE "/" "\\\\" GROUP ${{GROUP}})
    source_group(${{GROUP}} FILES ${{FILE}})
endforeach()

if(NOT DEFINED {library_data.var_name.upper()}_EXT_DIR)
    set({library_data.var_name.upper()}_EXT_DIR ${{{library_data.cmake_package}_DIR}})
endif()

# Install
install(TARGETS {library_data.lib_name} DESTINATION ${{{library_data.cmake_package}_DIR}})
install(TARGETS {library_data.ext_name} DESTINATION ${{{library_data.var_name.upper()}_EXT_DIR}})

if (DEFINED BUILD_{library_data.var_name.upper()}_TESTS)
    add_subdirectory(tests)
endif()
"""
        )
