# ps.py
# Path commands

# Luqi Chen
# luqic2@uci.edu
# 69278864

import ui
from Profile import *
from pathlib import Path

#sort contents for files
def file_list(path):
    return [fil for fil in path.iterdir() if fil.is_file()]

#sort contents for directories/folders
def directory_list(path):
    return [dir for dir in path.iterdir() if dir.is_dir()]

def select_filename(path, name):
    return [fil for fil in file_list(path) if fil.name == name]
    
def select_extension(path, ext):
    if ext.startswith(".") is False:
        ext = "." + ext
    return [fil for fil in file_list(path) if fil.suffix == ext]

def convert_to_Path(str):
    return Path(str)

def check_if_dsu(p:str, admin=False):
    path = Path(p)
    if path.suffix != ".dsu":
        ui.print_admin_lines("Unable to detect DSU file. Please input valid DSU file.\n(should end with .dsu)", admin)
        return False
    return True

def check_if_DSU_file(fp:str):
    filePath = Path(fp)
    if filePath.is_dir() is True:
        print("Looks like this is a folder.")
    elif check_if_dsu(filePath) is True and check_if_directory_file(filePath) is True:
        return True
    return False

def check_if_directory_file(p:str, mess: bool = True, message:str = "Directory does not exist"):
    try:
        path = Path(p)
        if path.is_dir() is True or path.is_file() is True:
            return True
        else:
            if mess is True:
                print(f"\n{message}.")
            return False
    except:
        if mess is True:
            print(f"\n{message}.")
        return False

def create_new_file(path, input):
    assert (input[0] == "-n"), "Incorrect function feature: must be -n (name)"
    assert len(input) > 0, "missing -n or name"

    try:
        file_name = input[1]
    except:
        file_name = input("Give a name for the file:\n")

    if file_name.endswith(".dsu") is False:
        file_name = input[1] + ".dsu"
    file = path / file_name
    file.touch()

def get_filePath(path:str, fileName):
    p = convert_to_Path(path)
    if fileName.endswith(".dsu") is False:
        fileName += ".dsu"
    filePath = p / fileName
    profile = Profile()
    profile.load_profile(str(filePath))
    return filePath

def remove_input_directory(path, contents:list):
    newContents = []
    for info in contents:
        if info == path:
            continue
        if type(info) is list:
            newContents.append(remove_input_directory(path, info))
        else:
            newContents.append(info)
    return newContents
