from enum import Enum


class LibraryType(Enum):
    Shared = "Shared"
    Interface = "Interface"


class LibraryData:
    def __init__(
        self,
        *,
        pypi_name: str,  # The PyPi hyphenated library name (amulet-nbt)
        repo_name: str,  # The name of the github repository (Amulet-NBT)
        short_var_name: str,  # A string for use in Python variables (amulet_nbt)
        import_name: str,  # The import name to the package (amulet.nbt)
        lib_name: str | None = None,  # The name of the shared library (leveldb_mcpe)
        cmake_lib_name: (
            str | None
        ) = None,  # The cmake library alias. Defaults to lib_name (pybind11::module)
        cmake_package: (
            str | None
        ) = None,  # The name of the library's cmake package. Defaults to cmake_lib_name.
        ext_name: (
            str | None
        ) = None,  # _amulet_nbt (The name of the python extension module)
        library_type: LibraryType,  # The type of library this library is.
        export_symbol: str | None = None,
        private_dependencies: tuple[
            str, ...
        ] = (),  # The C++ dependencies that are not exported by the shared library.
        public_dependencies: tuple[
            str, ...
        ] = (),  # The C++ dependencies that are exported by the shared library.
        ext_dependencies: tuple[
            str, ...
        ] = (),  # The C++ dependencies needed by the Python extension.
        runtime_dependencies: tuple[
            str, ...
        ] = (),  # The dependencies that are only needed at runtime.
        test_dependencies: tuple[str, ...] = ()
    ):
        self.pypi_name = pypi_name.replace("_", "-")
        self.repo_name = repo_name
        self.import_name = import_name
        self.root_import_name = import_name.split(".", 1)[0]
        self.var_name = import_name.replace(".", "_")
        self.short_var_name = short_var_name
        self.lib_name = lib_name
        self.cmake_lib_name = cmake_lib_name or lib_name
        self.cmake_package = cmake_package or self.cmake_lib_name
        self.ext_name = ext_name
        self.library_type = library_type
        self.export_symbol = export_symbol
        self.private_dependencies = private_dependencies
        self.public_dependencies = public_dependencies
        self.ext_dependencies = ext_dependencies
        self.runtime_dependencies = runtime_dependencies
        self.test_dependencies = test_dependencies


PyBind11 = LibraryData(
    pypi_name="pybind11",
    repo_name="pybind11",
    short_var_name="pybind11",
    import_name="pybind11",
    cmake_lib_name="pybind11::module",
    cmake_package="pybind11",
    library_type=LibraryType.Interface,
)
PyBind11Extensions = LibraryData(
    pypi_name="amulet-pybind11-extensions",
    repo_name="Amulet-pybind11-extensions",
    short_var_name="pybind11_extensions",
    import_name="amulet.pybind11_extensions",
    cmake_lib_name="amulet_pybind11_extensions",
    library_type=LibraryType.Interface,
)
AmuletCompilerVersion = LibraryData(
    pypi_name="amulet-compiler-version",
    repo_name="Amulet-Compiler-Version",
    short_var_name="compiler_version",
    import_name="amulet_compiler_version",
    cmake_lib_name="amulet_compiler_version",
    library_type=LibraryType.Interface,
)
AmuletTestUtils = LibraryData(
    pypi_name="amulet-test-utils",
    repo_name="Amulet-Test-Utils",
    short_var_name="test_utils",
    import_name="amulet.test_utils",
    cmake_lib_name="amulet_test_utils",
    library_type=LibraryType.Interface,
)
AmuletIO = LibraryData(
    pypi_name="amulet-io",
    repo_name="Amulet-IO",
    short_var_name="io",
    import_name="amulet.io",
    cmake_lib_name="amulet_io",
    library_type=LibraryType.Interface,
    private_dependencies=(),
    public_dependencies=(),
    ext_dependencies=(PyBind11.pypi_name,),
    runtime_dependencies=(),
)
AmuletLevelDB = LibraryData(
    pypi_name="amulet-leveldb",
    repo_name="Amulet-LevelDB",
    short_var_name="leveldb",
    import_name="amulet.leveldb",
    lib_name="leveldb_mcpe",
    ext_name="_leveldb",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
)
AmuletUtils = LibraryData(
    pypi_name="amulet-utils",
    repo_name="Amulet-Utils",
    short_var_name="utils",
    import_name="amulet.utils",
    lib_name="amulet_utils",
    ext_name="_amulet_utils",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletUtils",
)
AmuletZlib = LibraryData(
    pypi_name="amulet-zlib",
    repo_name="Amulet-zlib",
    short_var_name="zlib",
    import_name="amulet.zlib",
    lib_name="amulet_zlib",
    ext_name="_amulet_zlib",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletZlib"
)
AmuletNBT = LibraryData(
    pypi_name="amulet-nbt",
    repo_name="Amulet-NBT",
    short_var_name="nbt",
    import_name="amulet.nbt",
    lib_name="amulet_nbt",
    ext_name="_amulet_nbt",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(AmuletIO.pypi_name,),
    runtime_dependencies=(),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletZlib.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    export_symbol="ExportAmuletNBT"
)
AmuletCore = LibraryData(
    pypi_name="amulet-core",
    repo_name="Amulet-Core",
    short_var_name="core",
    import_name="amulet.core",
    lib_name="amulet_core",
    ext_name="_amulet_core",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(
        AmuletIO.pypi_name,
        AmuletNBT.pypi_name,
    ),
    runtime_dependencies=(),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletCore"
)
AmuletGame = LibraryData(
    pypi_name="amulet-game",
    repo_name="Amulet-Game",
    short_var_name="game",
    import_name="amulet.game",
    lib_name="amulet_game",
    ext_name="_amulet_game",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(
        PyBind11.pypi_name,
        AmuletIO.pypi_name,
        AmuletNBT.pypi_name,
        AmuletCore.pypi_name,
    ),
    runtime_dependencies=(),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletGame"
)
AmuletAnvil = LibraryData(
    pypi_name="amulet-anvil",
    repo_name="Amulet-Anvil",
    short_var_name="anvil",
    import_name="amulet.anvil",
    lib_name="amulet_anvil",
    ext_name="_amulet_anvil",
    library_type=LibraryType.Shared,
    private_dependencies=(AmuletZlib.pypi_name,),
    public_dependencies=(
        AmuletIO.pypi_name,
        AmuletNBT.pypi_name,
        AmuletCore.pypi_name,
        AmuletUtils.pypi_name,
    ),
    runtime_dependencies=(),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletAnvil"
)
AmuletLevel = LibraryData(
    pypi_name="amulet-level",
    repo_name="Amulet-Level",
    short_var_name="level",
    import_name="amulet.level",
    lib_name="amulet_level",
    ext_name="_amulet_level",
    library_type=LibraryType.Shared,
    private_dependencies=(AmuletZlib.pypi_name,),
    public_dependencies=(
        AmuletIO.pypi_name,
        AmuletLevelDB.pypi_name,
        AmuletUtils.pypi_name,
        AmuletNBT.pypi_name,
        AmuletCore.pypi_name,
        AmuletGame.pypi_name,
        AmuletAnvil.pypi_name,
    ),
    runtime_dependencies=(),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletLevel"
)
AmuletResourcePack = LibraryData(
    pypi_name="amulet-resource-pack",
    repo_name="Amulet-Resource-Pack",
    short_var_name="resource_pack",
    import_name="amulet.resource_pack",
    lib_name="amulet_resource_pack",
    ext_name="_amulet_resource_pack",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(AmuletUtils.pypi_name,),
    runtime_dependencies=(),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletResourcePack"
)


interface_libraries: list[LibraryData] = [
    PyBind11,
    PyBind11Extensions,
    AmuletCompilerVersion,
    AmuletIO,
    AmuletTestUtils,
]

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

library_order: dict[str, int] = {
    lib.pypi_name: i for i, lib in enumerate(libraries.values())
}
