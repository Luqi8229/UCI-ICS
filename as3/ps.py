
from pathlib import Path

def file_list(path, extra=""):
    return [fil for fil in path.iterdir() if fil.is_file()]

def directory_list(path):
    return [dir for dir in path.iterdir() if dir.is_dir()]

def select_fileName(path, name):
    return [fil for fil in file_list(path) if fil.name == name]

def select_filestem(path, name):
    return [fil for fil in file_list(path) if fil.stem == name]
    
def select_extension(path, ext):
    if ext.startswith(".") is False:
        ext = "." + ext
    return [fil for fil in file_list(path) if fil.suffix == ext]

def path(str):
    return Path(str)

