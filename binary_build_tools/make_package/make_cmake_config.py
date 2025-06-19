import os

from binary_build_tools.data import LibraryData


def write(package_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(package_path, f"{library_data.lib_name}Config.cmake"), "w", encoding="utf-8") as f:
        f.write(f"""if (NOT TARGET {library_data.lib_name})
    message(STATUS "Finding {library_data.lib_name}")

    set({library_data.lib_name}_INCLUDE_DIR "${{CMAKE_CURRENT_LIST_DIR}}/../..")
    find_library({library_data.lib_name}_LIBRARY NAMES {library_data.lib_name} PATHS "${{CMAKE_CURRENT_LIST_DIR}}")
    message(STATUS "{library_data.lib_name}_LIBRARY: ${{{library_data.lib_name}_LIBRARY}}")

    add_library({library_data.lib_name}_bin SHARED IMPORTED)
    set_target_properties({library_data.lib_name}_bin PROPERTIES
        IMPORTED_IMPLIB "${{{library_data.lib_name}_LIBRARY}}"
    )

    add_library({library_data.lib_name} INTERFACE)
    target_link_libraries({library_data.lib_name} INTERFACE {library_data.lib_name}_bin)
    target_include_directories({library_data.lib_name} INTERFACE ${{{library_data.lib_name}_INCLUDE_DIR}})
endif()
""")
