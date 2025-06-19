import os
import glob
import importlib.util
import sys
import subprocess
import re
import pybind11_stubgen
from pybind11_stubgen.structs import Identifier
from pybind11_stubgen.parser.mixins.filter import FilterClassMembers

UnionPattern = re.compile(
    r"^(?P<variable>[a-zA-Z_][a-zA-Z0-9_]*): types\.UnionType\s*#\s*value = (?P<value>.*)$",
    flags=re.MULTILINE,
)


def union_sub_func(match: re.Match) -> str:
    return f'{match.group("variable")}: typing.TypeAlias = {match.group("value")}'


VersionPattern = re.compile(r"(?P<var>[a-zA-Z0-9_].*): str = '.*?'")


def str_sub_func(match: re.Match) -> str:
    return f"{match.group('var')}: str"


EqPattern = re.compile(
    r"(?P<indent>[ \t]+)def __eq__\(self, arg0: (?P<other>[a-zA-Z1-9.]+)\) -> (?P<return>[a-zA-Z1-9.]+):"
    r"(?P<ellipsis_docstring>\s*((\.\.\.)|(\"\"\"(.|\n)*?\"\"\")))"
)


def eq_sub_func(match: re.Match) -> str:
    """
    if one - add @overload and overloaded signature

    """
    if match.string[: match.start()].endswith("@typing.overload\n"):
        # is overload
        if re.match(
            f"\\n{match.group('indent')}@typing.overload\\n{match.group('indent')}def __eq__\\(self, ",
            match.string[match.end() :],
        ):
            # is not last overload
            return match.group()
        else:
            return "\n".join(
                [
                    f"{match.group('indent')}def __eq__(self, arg0: {match.group('other')}) -> {match.group('return')}:{match.group('ellipsis_docstring')}",
                    f"{match.group('indent')}@typing.overload",
                    f"{match.group('indent')}def __eq__(self, arg0: typing.Any) -> bool | types.NotImplementedType: ...",
                ]
            )
    else:
        return "\n".join(
            [
                f"{match.group('indent')}@typing.overload",
                f"{match.group('indent')}def __eq__(self, arg0: {match.group('other')}) -> {match.group('return')}:{match.group('ellipsis_docstring')}",
                f"{match.group('indent')}@typing.overload",
                f"{match.group('indent')}def __eq__(self, arg0: typing.Any) -> bool | types.NotImplementedType: ...",
            ]
        )


GenericAliasPattern = re.compile(
    r"(?P<variable>[a-zA-Z0-9]+): types.GenericAlias\s*# value = (?P<value>.*)"
)


def generic_alias_sub_func(match: re.Match) -> str:
    return f"{match.group('variable')}: typing.TypeAlias = {match.group('value')}"


def get_module_path(name: str) -> str:
    spec = importlib.util.find_spec(name)
    assert spec is not None
    module_path = spec.origin
    assert module_path is not None
    return module_path


def get_package_dir(name: str) -> str:
    return os.path.realpath(os.path.dirname(get_module_path(name)))


def patch_stubgen():
    # Is there a better way to add items to the blacklist?
    # Pybind11
    FilterClassMembers._FilterClassMembers__class_member_blacklist.add(
        Identifier("_pybind11_conduit_v1_")
    )
    # Python
    FilterClassMembers._FilterClassMembers__class_member_blacklist.add(
        Identifier("__new__")
    )
    FilterClassMembers._FilterClassMembers__class_member_blacklist.add(
        Identifier("__subclasshook__")
    )
    # Pickle
    FilterClassMembers._FilterClassMembers__class_member_blacklist.add(
        Identifier("__getnewargs__")
    )
    FilterClassMembers._FilterClassMembers__class_member_blacklist.add(
        Identifier("__getstate__")
    )
    FilterClassMembers._FilterClassMembers__class_member_blacklist.add(
        Identifier("__setstate__")
    )
    # ABC
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("__abstractmethods__")
    )
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("__orig_bases__")
    )
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("__parameters__")
    )
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("_abc_impl")
    )
    # Protocol
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("__protocol_attrs__")
    )
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("__non_callable_proto_members__")
    )
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("_is_protocol")
    )
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("_is_runtime_protocol")
    )
    # dataclass
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("__dataclass_fields__")
    )
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("__dataclass_params__")
    )
    FilterClassMembers._FilterClassMembers__attribute_blacklist.add(
        Identifier("__match_args__")
    )
    # Buffer protocol
    FilterClassMembers._FilterClassMembers__class_member_blacklist.add(
        Identifier("__buffer__")
    )
    FilterClassMembers._FilterClassMembers__class_member_blacklist.add(
        Identifier("__release_buffer__")
    )


def main() -> None:
    package_name = "amulet.utils"
    package_path = get_package_dir(package_name)
    src_path = os.path.dirname(os.path.dirname(package_path))

    # Remove all existing stub files
    print("Removing stub files...")
    for stub_path in glob.iglob(
        os.path.join(glob.escape(package_path), "**", "*.pyi"), recursive=True
    ):
        os.remove(stub_path)

    # Extend pybind11-stubgen
    patch_stubgen()

    # Call pybind11-stubgen
    print("Running pybind11-stubgen...")
    sys.argv = [
        "pybind11_stubgen",
        f"--output-dir={src_path}",
        package_name,
    ]
    pybind11_stubgen.main()
    # If pybind11_stubgen adds args to main
    # pybind11_stubgen.main([
    #     f"--output-dir={src_path}",
    #     package_name,
    # ])

    # Run normal stubgen on the python files
    # print("Running stubgen...")
    # stubgen.main([
    #     *glob.glob(
    #         os.path.join(glob.escape(package_path), "**", "*.py"), recursive=True
    #     ),
    #     "-o",
    #     package_path,
    #     "--include-docstrings",
    # ])

    # Remove stub files generated for python modules
    for stub_path in glob.iglob(
        os.path.join(glob.escape(package_path), "**", "*.pyi"), recursive=True
    ):
        if os.path.isfile(stub_path[:-1]):
            os.remove(stub_path)

    print("Patching stub files...")
    # Fix some issues and reformat the stub files.
    stub_paths = glob.glob(
        os.path.join(glob.escape(package_path), "**", "*.pyi"), recursive=True
    )
    for stub_path in stub_paths:
        with open(stub_path, encoding="utf-8") as f:
            pyi = f.read()
        pyi = UnionPattern.sub(union_sub_func, pyi)
        pyi = VersionPattern.sub(str_sub_func, pyi)
        pyi = GenericAliasPattern.sub(generic_alias_sub_func, pyi)
        pyi = pyi.replace(
            "__hash__: typing.ClassVar[None] = None",
            "__hash__: typing.ClassVar[None] = None  # type: ignore",
        )
        pyi = EqPattern.sub(eq_sub_func, pyi)
        pyi = pyi.replace("**kwargs)", "**kwargs: typing.Any)")
        pyi_split = [l.rstrip("\r") for l in pyi.split("\n")]
        for hidden_import in []:
            if hidden_import in pyi and f"import {hidden_import}" not in pyi_split:
                pyi_split.insert(2, f"import {hidden_import}")
        if "import typing" not in pyi_split:
            pyi_split.insert(2, "import typing")
        if "import types" not in pyi_split:
            pyi_split.insert(2, "import types")
        pyi = "\n".join(pyi_split)
        with open(stub_path, "w", encoding="utf-8") as f:
            f.write(pyi)

    subprocess.run(
        [
            "isort",
            *stub_paths,
        ]
    )

    subprocess.run(
        [
            "autoflake",
            "--in-place",
            "--remove-unused-variables",
            *stub_paths,
        ]
    )

    subprocess.run([sys.executable, "-m", "black", package_path])


if __name__ == "__main__":
    main()
