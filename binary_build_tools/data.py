from enum import Enum


class LibraryType(Enum):
    Shared = "Shared"
    Interface = "Interface"


class LibraryData:
    def __init__(
        self,
        pypi_name: str,
        root_import_name: str,
        import_name: str,
        ext_import_name: str | None,
        interface_dependencies: list[str],
        shared_dependencies: list[str],
        exported_dependencies: list[str],
        # short_name_lower: str,
        # short_name_pretty: str,
    ):
        self.pypi_name = pypi_name.replace("_", "-")
        self.root_import_name = root_import_name
        self.import_name = import_name
        self.ext_import_name = ext_import_name
        self.interface_dependencies = interface_dependencies
        self.shared_dependencies = shared_dependencies
        self.exported_dependencies = exported_dependencies
        # self.short_name_lower = short_name_lower
        # self.short_name_pretty = short_name_pretty

PyBind11 = LibraryData(
    "pybind11",
    "pybind11",
    "pybind11",
    None,
    [],
    [],
    [],
)
PyBind11Extensions = LibraryData(
    "amulet-pybind11-extensions",
    "amulet",
    "amulet.pybind11_extensions",
    None,
    [],
    [],
    [],
)
AmuletCompilerVersion = LibraryData(
    "amulet-compiler-version",
    "amulet",
    "amulet_compiler_version",
    None,
    [],
    [],
    [],
)
AmuletIO = LibraryData(
    "amulet-io",
    "amulet",
    "amulet.io",
    None,
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletLevelDB = LibraryData(
    "amulet-leveldb",
    "amulet",
    "amulet.leveldb",
    "amulet.leveldb._amulet_leveldb",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletUtils = LibraryData(
    "amulet-utils",
    "amulet",
    "amulet.utils",
    "amulet.utils._amulet_utils",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletZlib = LibraryData(
    "amulet-zlib",
    "amulet",
    "amulet.zlib",
    "amulet.zlib._amulet_zlib",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletNBT = LibraryData(
    "amulet-nbt",
    "amulet",
    "amulet.nbt",
    "amulet.nbt._amulet_nbt",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletCore = LibraryData(
    "amulet-core",
    "amulet",
    "amulet.core",
    "amulet.core._amulet_core",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletGame = LibraryData(
    "amulet-game",
    "amulet",
    "amulet.game",
    "amulet.game._amulet_game",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletAnvil = LibraryData(
    "amulet-anvil",
    "amulet",
    "amulet.anvil",
    "amulet.anvil._amulet_anvil",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletLevel = LibraryData(
    "amulet-level",
    "amulet",
    "amulet.level",
    "amulet.level._amulet_level",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)
AmuletResourcePack = LibraryData(
    "amulet-resource-pack",
    "amulet",
    "amulet.resource_pack",
    "amulet.resource_pack._amulet_resource_pack",
    [
        PyBind11.pypi_name,
    ],
    [],
    [],
)


interface_libraries: list[LibraryData] = []

shared_libraries: list[LibraryData] = [
    AmuletLevelDB,
    AmuletUtils,
    AmuletZlib,
    AmuletNBT,
    AmuletCore,
    AmuletGame,
    AmuletAnvil,
    AmuletLevel,
    AmuletResourcePack,
]

libraries: dict[str, LibraryData] = {
    lib.pypi_name: lib for lib in interface_libraries + shared_libraries
}
