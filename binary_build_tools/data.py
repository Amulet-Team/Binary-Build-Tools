from enum import Enum


class LibraryType(Enum):
    Shared = "Shared"
    Interface = "Interface"


class LibraryData:
    def __init__(
        self,
        pypi_name: str,  # amulet-nbt
        repo_name: str,  # Amulet-NBT
        root_import_name: str,  # amulet
        import_name: str,  # amulet.nbt
        ext_name: str | None,  # _amulet_nbt
        library_type: LibraryType,  # Shared
        private_dependencies: list[str],
        public_dependencies: list[str],
        # short_name_lower: str,
        # short_name_pretty: str,
    ):
        self.pypi_name = pypi_name.replace("_", "-")
        self.repo_name = repo_name
        self.root_import_name = root_import_name
        self.import_name = import_name
        self.ext_name = ext_name
        self.library_type = library_type
        self.private_dependencies = private_dependencies
        self.public_dependencies = public_dependencies
        # self.short_name_lower = short_name_lower
        # self.short_name_pretty = short_name_pretty


PyBind11 = LibraryData(
    "pybind11",
    "pybind11",
    "pybind11",
    "pybind11",
    None,
    LibraryType.Interface,
    [],
    [],
)
PyBind11Extensions = LibraryData(
    "amulet-pybind11-extensions",
    "Amulet-pybind11-extensions",
    "amulet",
    "amulet.pybind11_extensions",
    None,
    LibraryType.Interface,
    [],
    [],
)
AmuletCompilerVersion = LibraryData(
    "amulet-compiler-version",
    "Amulet-Compiler-Version",
    "amulet",
    "amulet_compiler_version",
    None,
    LibraryType.Interface,
    [],
    [],
)
AmuletIO = LibraryData(
    "amulet-io",
    "Amulet-IO",
    "amulet",
    "amulet.io",
    None,
    LibraryType.Interface,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletLevelDB = LibraryData(
    "amulet-leveldb",
    "Amulet-LevelDB",
    "amulet",
    "amulet.leveldb",
    "_amulet_leveldb",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletUtils = LibraryData(
    "amulet-utils",
    "Amulet-Utils",
    "amulet",
    "amulet.utils",
    "_amulet_utils",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletZlib = LibraryData(
    "amulet-zlib",
    "Amulet-zlib",
    "amulet",
    "amulet.zlib",
    "_amulet_zlib",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletNBT = LibraryData(
    "amulet-nbt",
    "Amulet-NBT",
    "amulet",
    "amulet.nbt",
    "_amulet_nbt",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletCore = LibraryData(
    "amulet-core",
    "Amulet-Core",
    "amulet",
    "amulet.core",
    "_amulet_core",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletGame = LibraryData(
    "amulet-game",
    "Amulet-Game",
    "amulet",
    "amulet.game",
    "_amulet_game",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletAnvil = LibraryData(
    "amulet-anvil",
    "Amulet-Anvil",
    "amulet",
    "amulet.anvil",
    "_amulet_anvil",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletLevel = LibraryData(
    "amulet-level",
    "Amulet-Level",
    "amulet",
    "amulet.level",
    "_amulet_level",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
    [],
)
AmuletResourcePack = LibraryData(
    "amulet-resource-pack",
    "Amulet-Resource-Pack",
    "amulet",
    "amulet.resource_pack",
    "_amulet_resource_pack",
    LibraryType.Shared,
    [
        PyBind11.pypi_name,
    ],
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
