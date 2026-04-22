from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules("amulet.app")
datas = collect_data_files("amulet.app")
