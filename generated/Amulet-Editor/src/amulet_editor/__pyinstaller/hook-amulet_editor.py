from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules("amulet_editor")
datas = collect_data_files("amulet_editor")
