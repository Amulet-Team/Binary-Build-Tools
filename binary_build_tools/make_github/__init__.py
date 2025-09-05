import os

from binary_build_tools.data import LibraryData

from . import (
    make_build,
    make_stylecheck,
    make_unittests,
)


def write(github_path: str, library_data: LibraryData) -> None:
    workflows_path = os.path.join(github_path, "workflows")
    os.makedirs(workflows_path, exist_ok=True)
    make_build.write(workflows_path, library_data)
    make_stylecheck.write(workflows_path)
    make_unittests.write(workflows_path, library_data)
