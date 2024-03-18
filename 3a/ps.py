
from ui import prompt_info, aline
from pathlib import Path

def file_list(path, name=''):
    return [fil for fil in path.iterdir() if fil.is_file()]

def directory_list(path):
    return [dir for dir in path.iterdir() if dir.is_dir()]

def select_filename(path, name):
    return [fil for fil in file_list(path) if fil.name == name]

def select_filestem(path, stem):
    return [fil for fil in file_list(path) if fil.stem == stem]

def select_extension(path, ext):
    if ext.startswith(".") is False:
        ext = "." + ext
    return [fil for fil in file_list(path) if fil.suffix == ext]

def path(str):
    return Path(str)

def pathExist(str):
    p = path(str)
    if p.exists() is True:
        return True
    print("Invalid directory.")
    return False

def isFolder(str):
    p = path(str)
    if p.is_dir() is True:
        return True
    return False

def create_file(folder, admin = False, dsu=False):
    fileName = prompt_info("Give a name for the file", admin)
    if dsu is True and ".dsu" not in fileName:
        fileName += ".dsu"
    filePath = Path(folder) / fileName
    if filePath.exists():
        aline(f"DSU file with {fileName} already exists")
        create_file(folder, admin, dsu)
    filePath.touch()
    return filePath

