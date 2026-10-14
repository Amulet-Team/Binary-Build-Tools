from enum import Enum
from functools import lru_cache
from packaging.specifiers import SpecifierSet
from collections.abc import Iterable, Mapping
from types import MappingProxyType

MacOSArm64Runner = "macos-15"
MacOSX64Runner = "macos-15-intel"
WindowX64Runner = "windows-2025-vs2026"
WindowArm64Runner = "windows-11-vs2026-arm"
UbuntuX64Runner = "ubuntu-24.04"
PythonVersion = "3.14"
CIBuildWheelVersion = "4.1"
CheckoutVersion = "7"
SetupPythonVersion = "6"
InstallQtVersion = "4"
QtVersion = "6.11.1"


class LibraryType(Enum):
    Static = "Static"
    Shared = "Shared"
    Interface = "Interface"
    Python = "Python"


class LibraryData:
    def __init__(
        self,
        *,
        name: str,
        org_name: str,  # The github organisation/user name (Amulet-Team)
        repo_name: str,  # The name of the github repository (Amulet-NBT)
        pypi_name: str | None = None,  # The PyPi hyphenated library name (amulet-nbt)
        import_name: str,  # The import name to the package (amulet.nbt)
        short_var_name: str,  # A string for use in Python variables (amulet_nbt)
        ext_macro_name: str = "",  # Name used in extension macros. (AMULET_NBT) Defaults to import_name.replace(".", "_").upper()
        project_macro_name: str = "",  # Name used in project macros. (AMULET_NBT) Defaults to ext_macro_name
        lib_name: (
            str | None
        ) = None,  # The name of the shared library. None if there is no shared library. (amulet_nbt)
        lib_major_version: int | None = None,
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
        test_dependencies: tuple[str, ...] = (),
        has_submodules: bool = False,
        specifier: SpecifierSet,
        description: str = "",
        gitignore: Iterable[str] = (),
        manifest: Iterable[str] = (),
        package_data: Iterable[str] = (),
        source_include_dirs: tuple[str, ...] = ("${SOURCE_PATH}",),
        config_include_dir: str = "../..",
        optional_dependencies: Mapping[str, Iterable[str]] = MappingProxyType({}),
        unittest_dep_groups: Iterable[str] = (),
        unittests_pre_build: str = "",
        unittests_linux_libs: Iterable[str] = (),
        unittests_pre_test: Iterable[str] = (),
        authors: Iterable[str] = ("James Clare",),
        console_scripts: Mapping[str, str] = MappingProxyType({}),
        gui_scripts: Mapping[str, str] = MappingProxyType({}),
        create_build_workflow: bool = True,
        thread_safety: bool = True,
        prebuilt: bool = True,
    ):
        self.name = name
        self.pypi_name = pypi_name.replace("_", "-") if pypi_name else pypi_name
        self.org_name = org_name
        self.repo_name = repo_name
        self.import_name = import_name
        self.root_import_name = import_name.split(".", 1)[0]
        self.short_var_name = short_var_name
        self.ext_macro_name = ext_macro_name or import_name.replace(".", "_").upper()
        self.project_macro_name = project_macro_name or self.ext_macro_name
        self.lib_name = lib_name
        self.lib_major_version = lib_major_version
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
        self.has_submodules = has_submodules
        self.specifier = specifier
        self.description = description
        self.gitignore = gitignore
        self.manifest = manifest
        self.package_data = package_data
        self.source_include_dirs = source_include_dirs
        self.config_include_dir = config_include_dir
        self.optional_dependencies = optional_dependencies
        self.unittest_dep_groups = unittest_dep_groups
        self.unittests_pre_build = unittests_pre_build
        self.unittests_linux_libs = unittests_linux_libs
        self.unittests_pre_test = unittests_pre_test
        self.authors = authors
        self.console_scripts = console_scripts
        self.gui_scripts = gui_scripts
        self.create_build_workflow = create_build_workflow
        self.thread_safety = thread_safety
        self.prebuilt = prebuilt

    def __repr__(self) -> str:
        return f"LibraryData({self.name})"


Packaging = LibraryData(
    name="packaging",
    pypi_name="packaging",
    org_name="pypa",
    repo_name="packaging",
    short_var_name="packaging",
    import_name="packaging",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=25.0"),
)
Numpy = LibraryData(
    name="numpy",
    pypi_name="numpy",
    org_name="numpy",
    repo_name="numpy",
    short_var_name="numpy",
    import_name="numpy",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=2.0"),
)
Pillow = LibraryData(
    name="pillow",
    pypi_name="pillow",
    org_name="python-pillow",
    repo_name="Pillow",
    short_var_name="pillow",
    import_name="PIL",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=11.3"),
)
PyOpenGL = LibraryData(
    name="PyOpenGL",
    pypi_name="PyOpenGL",
    org_name="mcfletch",
    repo_name="pyopengl",
    short_var_name="pyopengl",
    import_name="OpenGL",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=3.1"),
)
RuntimeFinal = LibraryData(
    name="amulet-runtime-final",
    pypi_name="amulet-runtime-final",
    org_name="Amulet-Team",
    repo_name="runtime-final",
    short_var_name="runtime_final",
    import_name="runtime_final",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=1.1"),
)
PySide6 = LibraryData(
    name="PySide6-Essentials",
    pypi_name="PySide6-Essentials",
    org_name="THISDOESNOTEXIST",
    repo_name="THISDOESNOTEXIST",
    short_var_name="pyside6",
    import_name="PySide6",
    library_type=LibraryType.Python,
    specifier=SpecifierSet(f"=={QtVersion}"),
)
Platformdirs = LibraryData(
    name="platformdirs",
    pypi_name="platformdirs",
    org_name="tox-dev",
    repo_name="platformdirs",
    short_var_name="platformdirs",
    import_name="platformdirs",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=4.0"),
)

PyBind11 = LibraryData(
    name="pybind11",
    pypi_name="pybind11",
    org_name="pybind",
    repo_name="pybind11",
    short_var_name="pybind11",
    import_name="pybind11",
    cmake_lib_name="pybind11::module",
    cmake_package="pybind11",
    library_type=LibraryType.Interface,
    specifier=SpecifierSet("==3.0.4"),
)
PyBind11Extensions = LibraryData(
    name="amulet-pybind11-extensions",
    pypi_name="amulet-pybind11-extensions",
    org_name="Amulet-Team",
    repo_name="Amulet-pybind11-extensions",
    short_var_name="pybind11_extensions",
    import_name="amulet.pybind11_extensions",
    cmake_lib_name="amulet_pybind11_extensions",
    library_type=LibraryType.Interface,
    specifier=SpecifierSet("~=1.2.0.0a2"),
)
AmuletCompilerVersion = LibraryData(
    name="amulet-compiler-version",
    pypi_name="amulet-compiler-version",
    org_name="Amulet-Team",
    repo_name="Amulet-Compiler-Version",
    short_var_name="compiler_version",
    import_name="amulet_compiler_version",
    cmake_lib_name="amulet_compiler_version",
    library_type=LibraryType.Interface,
    specifier=SpecifierSet("~=4.0"),
)
AmuletTestUtils = LibraryData(
    name="amulet-test-utils",
    pypi_name="amulet-test-utils",
    org_name="Amulet-Team",
    repo_name="Amulet-Test-Utils",
    short_var_name="test_utils",
    import_name="amulet.test_utils",
    cmake_lib_name="amulet_test_utils",
    library_type=LibraryType.Interface,
    specifier=SpecifierSet("~=1.3"),
)
AmuletIO = LibraryData(
    name="amulet-io",
    pypi_name="amulet-io",
    org_name="Amulet-Team",
    repo_name="Amulet-IO",
    short_var_name="io",
    import_name="amulet.io",
    cmake_lib_name="amulet_io",
    library_type=LibraryType.Interface,
    private_dependencies=(),
    public_dependencies=(),
    ext_dependencies=(PyBind11.name,),
    runtime_dependencies=(),
    specifier=SpecifierSet("~=2.0.0.0a0"),
)
AmuletUtils = LibraryData(
    name="amulet-utils",
    pypi_name="amulet-utils",
    org_name="Amulet-Team",
    repo_name="Amulet-Utils",
    short_var_name="utils",
    import_name="amulet.utils",
    lib_name="amulet_utils",
    ext_name="_amulet_utils",
    library_type=LibraryType.Shared,
    private_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    public_dependencies=(),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    runtime_dependencies=(Platformdirs.name,),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
        AmuletTestUtils.name,
    ),
    export_symbol="ExportAmuletUtils",
    specifier=SpecifierSet("~=1.1.8.0a0"),
    description="A C++ utility library with a python wrapper.",
    optional_dependencies={
        "numpy": ["numpy~=2.0"],
        "pillow": ["pillow~=11.0"],
        "pyside6": ["PySide6-Essentials~=6.9"],
    },
    unittest_dep_groups=("numpy", "pillow", "pyside6"),
    package_data=["**/*.png"],
    unittests_linux_libs=["libxkbcommon"],
)
AmuletLevelDB = LibraryData(
    name="amulet-leveldb",
    pypi_name="amulet-leveldb",
    org_name="Amulet-Team",
    repo_name="Amulet-LevelDB",
    short_var_name="leveldb",
    import_name="amulet.leveldb",
    lib_name="leveldb",
    lib_major_version=1,
    cmake_package="amulet_leveldb",
    ext_name="_leveldb",
    library_type=LibraryType.Shared,
    private_dependencies=(
        AmuletUtils.name,
    ),
    public_dependencies=(),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    specifier=SpecifierSet("~=3.0.8.0a0"),
    description="A pybind11 wrapper for Mojang's custom LevelDB.",
    gitignore=["/src/amulet/leveldb/include/leveldb"],
    source_include_dirs=("${leveldb_SOURCE_DIR}/include", "${amulet_leveldb_DIR}/include"),
    config_include_dir="include",
)
AmuletRocksDB = LibraryData(
    name="amulet-rocksdb",
    pypi_name="amulet-rocksdb",
    org_name="Amulet-Team",
    repo_name="Amulet-RocksDB",
    short_var_name="amulet.rocksdb",
    import_name="amulet.rocksdb",
    lib_name="rocksdb",
    lib_major_version=1,
    cmake_package="amulet_rocksdb",
    ext_name="_rocksdb",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    specifier=SpecifierSet("~=2.0.0.0a0"),
    description="A pybind11 wrapper for Facebook's RocksDB.",
)
AmuletZlib = LibraryData(
    name="amulet-zlib",
    pypi_name="amulet-zlib",
    org_name="Amulet-Team",
    repo_name="Amulet-zlib",
    short_var_name="zlib",
    import_name="amulet.zlib",
    lib_name="amulet_zlib",
    ext_name="_amulet_zlib",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
        AmuletTestUtils.name,
    ),
    export_symbol="ExportAmuletZlib",
    specifier=SpecifierSet("~=1.0.11.0a0"),
    description="A Python and C++ wrapper around zlib.",
    optional_dependencies={
        "docs": [
            "Sphinx>=1.7.4",
            "sphinx-autodoc-typehints>=1.3.0",
            "sphinx_rtd_theme>=0.3.1",
        ]
    },
    thread_safety=False
)
AmuletNBT = LibraryData(
    name="amulet-nbt",
    pypi_name="amulet-nbt",
    org_name="Amulet-Team",
    repo_name="Amulet-NBT",
    short_var_name="nbt",
    import_name="amulet.nbt",
    lib_name="amulet_nbt",
    ext_name="_amulet_nbt",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(AmuletIO.name,),
    runtime_dependencies=(Numpy.name,),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
        AmuletZlib.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    export_symbol="ExportAmuletNBT",
    specifier=SpecifierSet("~=5.0.5.0a0"),
    description="Read and write Minecraft NBT and SNBT data.",
    optional_dependencies={
        "docs": [
            "Sphinx>=1.7.4",
            "sphinx-autodoc-typehints>=1.3.0",
            "sphinx_rtd_theme>=0.3.1",
        ]
    },
    authors=("James Clare", "Ben Gothard"),
    thread_safety=False
)
AmuletCore = LibraryData(
    name="amulet-core",
    pypi_name="amulet-core",
    org_name="Amulet-Team",
    repo_name="Amulet-Core",
    short_var_name="core",
    import_name="amulet.core",
    lib_name="amulet_core",
    ext_name="_amulet_core",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(
        AmuletIO.name,
        AmuletNBT.name,
        AmuletUtils.name,
    ),
    runtime_dependencies=(Numpy.name,),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
        AmuletTestUtils.name,
    ),
    export_symbol="ExportAmuletCore",
    specifier=SpecifierSet("~=2.0.11.0a0"),
    description="A Python library for reading/writing Minecraft's various save formats.",
    optional_dependencies={
        "docs": [
            "Sphinx>=1.7.4",
            "sphinx-autodoc-typehints>=1.3.0",
            "sphinx_rtd_theme>=0.3.1",
        ]
    },
    authors=("James Clare", "Ben Gothard"),
)
AmuletResourcePack = LibraryData(
    name="amulet-resource-pack",
    pypi_name="amulet-resource-pack",
    org_name="Amulet-Team",
    repo_name="Amulet-Resource-Pack",
    short_var_name="resource_pack",
    import_name="amulet.resource_pack",
    lib_name="amulet_resource_pack",
    ext_name="_amulet_resource_pack",
    library_type=LibraryType.Shared,
    private_dependencies=(
        PyBind11.name,
    ),
    public_dependencies=(
        AmuletUtils.name,
        AmuletCore.name,
    ),
    runtime_dependencies=(
        Numpy.name,
        Pillow.name,
    ),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
        AmuletTestUtils.name,
    ),
    export_symbol="ExportAmuletResourcePack",
    specifier=SpecifierSet("~=1.0.6.0a0"),
    description="A Python and C++ library for interacting with Minecraft resource packs.",
    package_data=["**/*.json", "**/*.mcmeta", "**/*.png"],
    manifest=["recursive-include src/amulet *.json *.mcmeta *.png"],
)
AmuletGame = LibraryData(
    name="amulet-game",
    pypi_name="amulet-game",
    org_name="Amulet-Team",
    repo_name="Amulet-Game",
    short_var_name="game",
    import_name="amulet.game",
    lib_name="amulet_game",
    ext_name="_amulet_game",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(
        PyBind11.name,
        AmuletIO.name,
        AmuletNBT.name,
        AmuletCore.name,
    ),
    runtime_dependencies=(),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
        AmuletTestUtils.name,
    ),
    export_symbol="ExportAmuletGame",
    has_submodules=True,
    specifier=SpecifierSet("~=1.0.6.0a0"),
    description="A Minecraft metadata and low level translation library.",
    gitignore=["/src/amulet/game/versions.pkl.gz"],
    manifest=["recursive-include submodules/PyMCTranslate *.json"],
    package_data=["**/*.pkl.gz"],
)
AmuletAnvil = LibraryData(
    name="amulet-anvil",
    pypi_name="amulet-anvil",
    org_name="Amulet-Team",
    repo_name="Amulet-Anvil",
    short_var_name="anvil",
    import_name="amulet.anvil",
    lib_name="amulet_anvil",
    ext_name="_amulet_anvil",
    library_type=LibraryType.Shared,
    private_dependencies=(
        LZ4.name,
        AmuletZlib.name,
    ),
    public_dependencies=(
        AmuletIO.name,
        AmuletNBT.name,
        AmuletUtils.name,
    ),
    runtime_dependencies=(),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
        AmuletTestUtils.name,
    ),
    export_symbol="ExportAmuletAnvil",
    specifier=SpecifierSet("~=1.0.7.0a0"),
    description="A C++ library with Python wrapper for the Minecraft Anvil format.",
    unittests_pre_test=[
        "pip install git+https://github.com/Amulet-Team/Amulet-Minecraft-Worlds.git",
    ],
)
AmuletLevel = LibraryData(
    name="amulet-level",
    pypi_name="amulet-level",
    org_name="Amulet-Team",
    repo_name="Amulet-Level",
    short_var_name="level",
    import_name="amulet.level",
    lib_name="amulet_level",
    ext_name="_amulet_level",
    library_type=LibraryType.Shared,
    private_dependencies=(AmuletZlib.name,),
    public_dependencies=(
        AmuletIO.name,
        AmuletLevelDB.name,
        AmuletUtils.name,
        AmuletNBT.name,
        AmuletCore.name,
        AmuletGame.name,
        AmuletAnvil.name,
    ),
    runtime_dependencies=(
        Numpy.name,
        Pillow.name,
    ),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
        AmuletTestUtils.name,
    ),
    export_symbol="ExportAmuletLevel",
    specifier=SpecifierSet("~=1.0.8.0a0"),
    description="A Python and C++ library for interacting with Minecraft worlds and structures.",
    unittests_pre_test=[
        "pip install git+https://github.com/Amulet-Team/Amulet-Minecraft-Worlds.git"
    ],
)
AmuletEditor = LibraryData(
    name="amulet-editor",
    org_name="Amulet-Team",
    repo_name="Amulet-Editor",
    pypi_name="amulet-editor",
    import_name="amulet.app",
    short_var_name="app",
    ext_macro_name="AMULET_APP",
    project_macro_name="AMULET_EDITOR",
    cmake_package="amulet_app",
    ext_name="_amulet_app",
    library_type=LibraryType.Shared,
    private_dependencies=(
        AmuletLevel.name,
        AmuletResourcePack.name,
    ),
    public_dependencies=(),
    runtime_dependencies=(
        Numpy.name,
        Pillow.name,
        PyOpenGL.name,
        RuntimeFinal.name,
        PySide6.name,
        Packaging.name,
    ),
    ext_dependencies=(
        PyBind11.name,
        PyBind11Extensions.name,
    ),
    test_dependencies=(),
    specifier=SpecifierSet("~=1.0.4.0a0"),
    authors=("James Clare", "Ben Gothard"),
    gitignore=[
        "",
        "# Visual Studio Code extensions",
        ".qt_for_python",
        "",
        "# Qt Creator",
        "*.pyproject.user",
        "*.ui.autosave",
        "",
        "working/",
    ],
    description="A Minecraft world editor and converter that supports all versions since Java 1.12 and Bedrock 1.7.",
    manifest=[
        "recursive-include src/amulet *.png *.svg *.ico *.lang *.json",
        "recursive-include src/plugins *.cpp *.hpp CMakeLists.txt *.json *.lang *.svg",
    ],
    package_data=[
        "**/*.png",
        "**/*.svg",
        "**/*.ico",
        "**/*.lang",
        "**/*.json",
        "**/*.qss",
    ],
    unittests_pre_build=f"""
    - name: Install Qt
      uses: jurplel/install-qt-action@v{InstallQtVersion}
      with:
        version: '{QtVersion}'
""",
    console_scripts={"amulet_editor": "amulet.app.__main__:main"},
    gui_scripts={"amulet_editor_no_console": "amulet.app.__main__:main"},
    create_build_workflow=False,
)


interface_libraries: list[LibraryData] = [
    PyBind11,
    PyBind11Extensions,
    AmuletCompilerVersion,
    AmuletIO,
    AmuletTestUtils,
]

static_libraries: list[LibraryData] = [
]

shared_libraries: list[LibraryData] = [
    AmuletLevelDB,
    AmuletRocksDB,
    AmuletUtils,
    AmuletZlib,
    AmuletNBT,
    AmuletCore,
    AmuletResourcePack,
    AmuletGame,
    AmuletAnvil,
    AmuletLevel,
    AmuletEditor,
]

python_libraries: list[LibraryData] = [
    Numpy,
    Pillow,
    Platformdirs,
    PyOpenGL,
    RuntimeFinal,
    PySide6,
    Packaging,
]

libraries: dict[str, LibraryData] = {
    lib.name: lib
    for lib in interface_libraries + static_libraries + shared_libraries + python_libraries
}

library_order: dict[str, int] = {
    lib.name: i for i, lib in enumerate(libraries.values())
}


@lru_cache(maxsize=None)
def find_dependencies(
    name: str,
    include_private: bool,
    include_public: bool,
    include_ext: bool,
    include_test: bool,
    include_private_recursive: bool,
    include_public_recursive: bool,
    include_ext_recursive: bool,
    include_test_recursive: bool,
) -> tuple[LibraryData, ...]:
    lib = libraries[name]
    lib_names: set[str] = set()
    lib_names_todo: set[str] = set()
    if include_private:
        lib_names_todo.update(lib.private_dependencies)
    if include_public:
        lib_names_todo.update(lib.public_dependencies)
    if include_ext:
        lib_names_todo.update(lib.ext_dependencies)
    if include_test:
        lib_names_todo.update(lib.test_dependencies)

    while lib_names_todo:
        lib_name = lib_names_todo.pop()
        if lib_name in lib_names:
            continue
        lib_names.add(lib_name)
        lib2 = libraries[lib_name]
        if include_private_recursive:
            lib_names_todo.update(lib2.private_dependencies)
        if include_public_recursive:
            lib_names_todo.update(lib2.public_dependencies)
        if include_ext_recursive:
            lib_names_todo.update(lib2.ext_dependencies)
        if include_test_recursive:
            lib_names_todo.update(lib2.test_dependencies)

    return tuple(
        libraries[lib_name]
        for lib_name in sorted(
            lib_names,
            key=library_order.__getitem__,
        )
    )
