cmake_minimum_required(VERSION 3.13)

project(amulet_zlib_tests LANGUAGES CXX)

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
find_package(amulet_zlib CONFIG REQUIRED)
find_package(amulet_test_utils CONFIG REQUIRED)

# Find sources
file(REAL_PATH test_amulet_zlib SOURCE_PATH)
file(GLOB_RECURSE SOURCES LIST_DIRECTORIES false ${SOURCE_PATH}/*.py.cpp)

pybind11_add_module(_test_amulet_zlib)
target_compile_definitions(_test_amulet_zlib PRIVATE PYBIND11_DETAILED_ERROR_MESSAGES)
target_compile_definitions(_test_amulet_zlib PRIVATE PYBIND11_VERSION="${pybind11_VERSION}")
target_compile_definitions(_test_amulet_zlib PRIVATE COMPILER_ID="${CMAKE_CXX_COMPILER_ID}")
target_compile_definitions(_test_amulet_zlib PRIVATE COMPILER_VERSION="${CMAKE_CXX_COMPILER_VERSION}")
target_link_libraries(_test_amulet_zlib PRIVATE amulet_pybind11_extensions)
target_link_libraries(_test_amulet_zlib PRIVATE amulet_zlib)
target_link_libraries(_test_amulet_zlib PRIVATE amulet_test_utils)
target_sources(_test_amulet_zlib PRIVATE ${SOURCES})

install(TARGETS _test_amulet_zlib DESTINATION ${TEST_AMULET_ZLIB_DIR})
