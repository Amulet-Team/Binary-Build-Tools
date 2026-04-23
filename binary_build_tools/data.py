from enum import Enum
from functools import lru_cache
from packaging.specifiers import SpecifierSet
from collections.abc import Iterable, Mapping
from types import MappingProxyType

MacOSArm64Runner = "macos-15"
MacOSX64Runner = "macos-15-intel"
WindowX64Runner = "windows-2025"
WindowArm64Runner = "windows-11-arm"
UbuntuX64Runner = "ubuntu-24.04"
PythonVersion = "3.14"


class LibraryType(Enum):
    Shared = "Shared"
    Interface = "Interface"
    Python = "Python"


class LibraryData:
    def __init__(
        self,
        *,
        org_name: str,  # The github organisation/user name (Amulet-Team)
        repo_name: str,  # The name of the github repository (Amulet-NBT)
        pypi_name: str,  # The PyPi hyphenated library name (amulet-nbt)
        import_name: str,  # The import name to the package (amulet.nbt)
        short_var_name: str,  # A string for use in Python variables (amulet_nbt)
        ext_macro_name: str = "",  # Name used in extension macros. (AMULET_NBT) Defaults to import_name.replace(".", "_").upper()
        project_macro_name: str = "",  # Name used in project macros. (AMULET_NBT) Defaults to ext_macro_name
        lib_name: (
            str | None
        ) = None,  # The name of the shared library. None if there is no shared library. (amulet_nbt)
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
        include_dir: str = "../..",
        optional_dependencies: Mapping[str, Iterable[str]] = MappingProxyType({}),
        unittest_dep_groups: Iterable[str] = ("dev",),
        unittests_pre_build: str = "",
        unittests_pre_test: str = "",
        authors: Iterable[str] = ("James Clare",),
        console_scripts: Mapping[str, str] = MappingProxyType({}),
        gui_scripts: Mapping[str, str] = MappingProxyType({}),
    ):
        self.pypi_name = pypi_name.replace("_", "-")
        self.org_name = org_name
        self.repo_name = repo_name
        self.import_name = import_name
        self.root_import_name = import_name.split(".", 1)[0]
        self.short_var_name = short_var_name
        self.ext_macro_name = ext_macro_name or import_name.replace(".", "_").upper()
        self.project_macro_name = project_macro_name or self.ext_macro_name
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
        self.has_submodules = has_submodules
        self.specifier = specifier
        self.description = description
        self.gitignore = gitignore
        self.manifest = manifest
        self.package_data = package_data
        self.include_dir = include_dir
        self.optional_dependencies = optional_dependencies
        self.unittest_dep_groups = unittest_dep_groups
        self.unittests_pre_build = unittests_pre_build
        self.unittests_pre_test = unittests_pre_test
        self.authors = authors
        self.console_scripts = console_scripts
        self.gui_scripts = gui_scripts


Packaging = LibraryData(
    pypi_name="packaging",
    org_name="pypa",
    repo_name="packaging",
    short_var_name="packaging",
    import_name="packaging",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=25.0"),
)
Numpy = LibraryData(
    pypi_name="numpy",
    org_name="numpy",
    repo_name="numpy",
    short_var_name="numpy",
    import_name="numpy",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=2.0"),
)
Pillow = LibraryData(
    pypi_name="pillow",
    org_name="python-pillow",
    repo_name="Pillow",
    short_var_name="pillow",
    import_name="PIL",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=11.3"),
)
PyOpenGL = LibraryData(
    pypi_name="PyOpenGL",
    org_name="mcfletch",
    repo_name="pyopengl",
    short_var_name="pyopengl",
    import_name="OpenGL",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=3.1"),
)
RuntimeFinal = LibraryData(
    pypi_name="amulet-runtime-final",
    org_name="Amulet-Team",
    repo_name="runtime-final",
    short_var_name="runtime_final",
    import_name="runtime_final",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=1.1"),
)
PySide6 = LibraryData(
    pypi_name="PySide6-Essentials",
    org_name="THISDOESNOTEXIST",
    repo_name="THISDOESNOTEXIST",
    short_var_name="pyside6",
    import_name="PySide6",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("==6.10.1"),
)
Platformdirs = LibraryData(
    pypi_name="platformdirs",
    org_name="tox-dev",
    repo_name="platformdirs",
    short_var_name="platformdirs",
    import_name="platformdirs",
    library_type=LibraryType.Python,
    specifier=SpecifierSet("~=4.0"),
)

PyBind11 = LibraryData(
    pypi_name="pybind11",
    org_name="pybind",
    repo_name="pybind11",
    short_var_name="pybind11",
    import_name="pybind11",
    cmake_lib_name="pybind11::module",
    cmake_package="pybind11",
    library_type=LibraryType.Interface,
    specifier=SpecifierSet("==3.0.1"),
)
PyBind11Extensions = LibraryData(
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
    pypi_name="amulet-compiler-version",
    org_name="Amulet-Team",
    repo_name="Amulet-Compiler-Version",
    short_var_name="compiler_version",
    import_name="amulet_compiler_version",
    cmake_lib_name="amulet_compiler_version",
    library_type=LibraryType.Interface,
    specifier=SpecifierSet("~=3.0"),
)
AmuletTestUtils = LibraryData(
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
    pypi_name="amulet-io",
    org_name="Amulet-Team",
    repo_name="Amulet-IO",
    short_var_name="io",
    import_name="amulet.io",
    cmake_lib_name="amulet_io",
    library_type=LibraryType.Interface,
    private_dependencies=(),
    public_dependencies=(),
    ext_dependencies=(PyBind11.pypi_name,),
    runtime_dependencies=(),
    specifier=SpecifierSet("~=2.0.0.0a0"),
)
AmuletLevelDB = LibraryData(
    pypi_name="amulet-leveldb",
    org_name="Amulet-Team",
    repo_name="Amulet-LevelDB",
    short_var_name="leveldb",
    import_name="amulet.leveldb",
    lib_name="leveldb",
    cmake_package="amulet_leveldb",
    ext_name="_leveldb",
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
    ),
    specifier=SpecifierSet("~=3.0.6.0a0"),
    description="A pybind11 wrapper for Mojang's custom LevelDB.",
    gitignore=["/src/amulet/leveldb/include/leveldb"],
    include_dir="include",
)
AmuletUtils = LibraryData(
    pypi_name="amulet-utils",
    org_name="Amulet-Team",
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
    runtime_dependencies=(Platformdirs.pypi_name,),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletUtils",
    specifier=SpecifierSet("~=1.1.4.0a"),
    description="A C++ utility library with a python wrapper.",
    optional_dependencies={
        "numpy": ["numpy~=2.0"],
        "pillow": ["pillow~=11.0"],
        "pyside6": ["PySide6-Essentials~=6.9"],
    },
    unittest_dep_groups=("dev", "numpy", "pillow", "pyside6"),
    package_data=["**/*.png"],
    unittests_pre_build="""
    - name: Install Ubuntu Extra
      if: startsWith(matrix.cfg.os, 'ubuntu')
      run: |
        sudo apt install libegl1
""",
)
AmuletZlib = LibraryData(
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
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletZlib",
    specifier=SpecifierSet("~=1.0.9.0a0"),
    description="A Python and C++ wrapper around zlib.",
    optional_dependencies={
        "docs": [
            "Sphinx>=1.7.4",
            "sphinx-autodoc-typehints>=1.3.0",
            "sphinx_rtd_theme>=0.3.1",
        ]
    },
)
AmuletNBT = LibraryData(
    pypi_name="amulet-nbt",
    org_name="Amulet-Team",
    repo_name="Amulet-NBT",
    short_var_name="nbt",
    import_name="amulet.nbt",
    lib_name="amulet_nbt",
    ext_name="_amulet_nbt",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(AmuletIO.pypi_name,),
    runtime_dependencies=(Numpy.pypi_name,),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletZlib.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    export_symbol="ExportAmuletNBT",
    specifier=SpecifierSet("~=5.0.4.0a0"),
    description="Read and write Minecraft NBT and SNBT data.",
    optional_dependencies={
        "docs": [
            "Sphinx>=1.7.4",
            "sphinx-autodoc-typehints>=1.3.0",
            "sphinx_rtd_theme>=0.3.1",
        ]
    },
    authors=("James Clare", "Ben Gothard"),
)
AmuletCore = LibraryData(
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
        AmuletIO.pypi_name,
        AmuletNBT.pypi_name,
        AmuletUtils.pypi_name,
    ),
    runtime_dependencies=(Numpy.pypi_name,),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
        AmuletTestUtils.pypi_name,
    ),
    export_symbol="ExportAmuletCore",
    specifier=SpecifierSet("~=2.0.9.0a0"),
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
    pypi_name="amulet-resource-pack",
    org_name="Amulet-Team",
    repo_name="Amulet-Resource-Pack",
    short_var_name="resource_pack",
    import_name="amulet.resource_pack",
    lib_name="amulet_resource_pack",
    ext_name="_amulet_resource_pack",
    library_type=LibraryType.Shared,
    private_dependencies=(),
    public_dependencies=(
        AmuletUtils.pypi_name,
        AmuletCore.pypi_name,
    ),
    runtime_dependencies=(
        Numpy.pypi_name,
        Pillow.pypi_name,
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
    export_symbol="ExportAmuletResourcePack",
    specifier=SpecifierSet("~=1.0.5.0a0"),
    description="A Python and C++ library for interacting with Minecraft resource packs.",
    package_data=["**/*.json", "**/*.mcmeta", "**/*.png"],
    manifest=["recursive-include src/amulet *.json *.mcmeta *.png"],
)
AmuletGame = LibraryData(
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
    export_symbol="ExportAmuletGame",
    has_submodules=True,
    specifier=SpecifierSet("~=1.0.5.0a0"),
    description="A Minecraft metadata and low level translation library.",
    gitignore=["/src/amulet/game/versions.pkl.gz"],
    manifest=["recursive-include submodules/PyMCTranslate *.json"],
    package_data=["**/*.pkl.gz"],
)
AmuletAnvil = LibraryData(
    pypi_name="amulet-anvil",
    org_name="Amulet-Team",
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
    export_symbol="ExportAmuletAnvil",
    specifier=SpecifierSet("~=1.0.5.0a0"),
    description="A C++ library with Python wrapper for the Minecraft Anvil format.",
    unittests_pre_test="""
    - name: Install Minecraft Worlds
      run: |
        pip install git+https://github.com/Amulet-Team/Amulet-Minecraft-Worlds.git
""",
)
AmuletLevel = LibraryData(
    pypi_name="amulet-level",
    org_name="Amulet-Team",
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
    runtime_dependencies=(
        Numpy.pypi_name,
        Pillow.pypi_name,
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
    export_symbol="ExportAmuletLevel",
    specifier=SpecifierSet("~=1.0.6.0a0"),
    description="A Python and C++ library for interacting with Minecraft worlds and structures.",
    unittests_pre_test="""
    - name: Install Minecraft Worlds
      run: |
        pip install git+https://github.com/Amulet-Team/Amulet-Minecraft-Worlds.git
""",
)
AmuletEditor = LibraryData(
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
        AmuletLevel.pypi_name,
        AmuletResourcePack.pypi_name,
    ),
    public_dependencies=(),
    runtime_dependencies=(
        Numpy.pypi_name,
        Pillow.pypi_name,
        PyOpenGL.pypi_name,
        RuntimeFinal.pypi_name,
        PySide6.pypi_name,
        Packaging.pypi_name,
    ),
    ext_dependencies=(
        PyBind11.pypi_name,
        PyBind11Extensions.pypi_name,
    ),
    test_dependencies=(),
    specifier=SpecifierSet("~=1.0.3.0a0"),
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
        "recursive-include src/plugins *.cpp *.hpp *.json *.lang *.svg",
    ],
    package_data=[
        "**/*.png",
        "**/*.svg",
        "**/*.ico",
        "**/*.lang",
        "**/*.json",
        "**/*.qss",
    ],
    unittests_pre_build="""
    - name: Install Qt (Windows)
      if: matrix.os == 'windows-latest'
      uses: jurplel/install-qt-action@v4
      with:
        version: '6.10.1'
        arch: 'win64_msvc2022_64'

    - name: Install Qt (Linux/MacOS)
      if: matrix.os != 'windows-latest'
      uses: jurplel/install-qt-action@v4
      with:
        version: '6.10.1'
""",
    console_scripts={"amulet_editor": "amulet.app.__main__:main"},
    gui_scripts={"amulet_editor_no_console": "amulet.app.__main__:main"},
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
    lib.pypi_name: lib
    for lib in interface_libraries + shared_libraries + python_libraries
}

library_order: dict[str, int] = {
    lib.pypi_name: i for i, lib in enumerate(libraries.values())
}


@lru_cache(maxsize=None)
def find_dependencies(
    pypi_name: str,
    include_private: bool,
    include_public: bool,
    include_ext: bool,
    include_test: bool,
    include_private_recursive: bool,
    include_public_recursive: bool,
    include_ext_recursive: bool,
    include_test_recursive: bool,
) -> tuple[LibraryData, ...]:
    lib = libraries[pypi_name]
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
        libraries[pypi_name]
        for pypi_name in sorted(
            lib_names,
            key=library_order.__getitem__,
        )
    )
