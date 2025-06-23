import os

from binary_build_tools.data import LibraryData

from . import (
    make_install,
    make_install_dependencies,
    make_stylecheck,
)


def write(github_path: str, library_data: LibraryData) -> None:
    actions_path = os.path.join(github_path, "actions")
    os.makedirs(actions_path, exist_ok=True)
    make_install.write(actions_path, library_data)
    make_install_dependencies.write(actions_path, library_data)
    workflows_path = os.path.join(github_path, "workflows")
    os.makedirs(workflows_path, exist_ok=True)
    make_stylecheck.write(workflows_path)
