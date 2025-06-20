import os


def write(package_path: str) -> None:
    with open(os.path.join(package_path, "py.typed"), "w", encoding="utf-8") as f:
        pass
