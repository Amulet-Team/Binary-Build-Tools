import os

from .data import LibraryData, LibraryType, find_dependencies


def write(project_path: str, library_data: LibraryData) -> None:
    with open(os.path.join(project_path, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(
            f"""# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec
!version_definitions/*/*.manifest

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/
docs_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
venv_37/
ENV/
env.bak/
venv.bak/
venv*

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# PyCharm settings
.idea/

# mkdocs documentation
/site

# mypy
.mypy_cache/

# Visual Studio
/install/
.vs
*.dll
*.so
*.dylib
*.lib
*.exp
*.pdb
*.ilk

/{library_data.import_name.replace(".", "_")}-*
"""
        )
        if any(
            lib.library_type == LibraryType.Shared
            for lib in find_dependencies(
                library_data.pypi_name,
                True,
                True,
                True,
                False,
                True,
                True,
                True,
                False,
            )
        ):
            f.write("/.github/actions/install-dependencies/*.json\n")
