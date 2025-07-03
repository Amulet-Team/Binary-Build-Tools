if (NOT TARGET amulet_editor)
    message(STATUS "Finding amulet_editor")

    set(amulet_editor_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/../..")
    find_library(amulet_editor_LIBRARY NAMES amulet_editor PATHS "${CMAKE_CURRENT_LIST_DIR}")
    message(STATUS "amulet_editor_LIBRARY: ${amulet_editor_LIBRARY}")

    add_library(amulet_editor_bin SHARED IMPORTED)
    set_target_properties(amulet_editor_bin PROPERTIES
        IMPORTED_IMPLIB "${amulet_editor_LIBRARY}"
    )

    add_library(amulet_editor INTERFACE)
    target_link_libraries(amulet_editor INTERFACE amulet_editor_bin)
    target_include_directories(amulet_editor INTERFACE ${amulet_editor_INCLUDE_DIR})
endif()
