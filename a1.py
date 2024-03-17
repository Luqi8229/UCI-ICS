
#user input format : [command] [input] -[option] [input]
# Possible commands:
# L - list contents of user specified directory
# Q - Quit program
# C - Create new file in the specified directory
# D - Delete the file
# R - Read the contents of a file

from pathlib import Path, PurePath

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
    # return Path('.').glob(f'**/*{ext}')

def convert_to_Path(str):
    return Path(PurePath(str))

def remove_list_info(ls, stride=1):
    return [ls[i] for i in range(len(ls)) if i > (stride-1)]

def check_if_dsu(path):
    if path.suffix != ".dsu":
        print("Unable to delete non-DSU files. Please input valid DSU file.")
        return False
    return True

def check_if_directory_file(path:str):
    path = convert_to_Path(path)
    if path.is_dir() is True or path.is_file() is True:
        return True
    else:
        print("Invalid directory.")
        return False

def print_info(info):
    for str in info:
        if type(str) is list:
            print_info(str)
        else:
            print(str)

def recursive_contents(path, options=[]):
    content = []
    directories = directory_list(path)
    numDirectory = len(directories)
    for i in range(numDirectory + 1):
        if len(options) == 0:
            content.append( path )
            content.append( file_list(path) )
        else:
            if "-f" in options:
                content.append( file_list(path) )
            elif "-s" in options:
                content.append( select_filename(path, options[1]) )
            elif "-e" in options:
                content.append( select_extension(path, options[1]) )
        if i == numDirectory:
            break
        else:
            path = convert_to_Path(directories[i])
    return content

def default_contents(path):
    content = file_list(path)
    content.append( directory_list(path) )
    return content

def list_contents(path, options):
    contents = []
    if len(options) == 0:
        print("Here are your file contents:")
        contents.append(default_contents(path))
    else:
        nOptions = remove_list_info(options)
        if options[0] == "-r":
            print("Here are all your files and directories:")
            if len(nOptions) > 0:
                contents.append(recursive_contents(path, nOptions))
            else:
                contents.append(recursive_contents(path))
        elif options[0] == "-f":
            print("Here are all your files:")
            contents.append(file_list(path))
        elif options[0] == "-s":
            print(f"Here are all your {options[1]} files:")
            contents.append(select_filename(path, options[1]))
        elif options[0] == "-e":
            print(f'Here are all your {options[1]} files')
            contents.append(select_extension(path, options[1]))
                
    contents = remove_input_directory(path, contents)
    print_info(contents)

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

def create_new_file(path, input):
    assert (input[0] == "-n"), "Incorrect function feature: must be -n (name)"
    assert len(input) > 0, "missing -n or name"

    file_name = input[1] + ".dsu"
    file = path / file_name
    file.touch()
        
def delete_DSU_file(path):
    if check_if_dsu(path) is True:
        path.unlink()
        print(path, "DELETED")
        
def read_file_contents(path):
    fileName = path.name
    
    if path.stat().st_size == 0:
        print("EMPTY")
        return

    with open(fileName, "r") as f:
        for line in f.readlines():
            print(line)

def run_command(ls):
    path = convert_to_Path( ls[1] )
    if check_if_directory_file(path) is True:
        nls = remove_list_info(ls, 2)

        if ls[0] == "L":
            list_contents(path, nls)
        elif ls[0] == "D":
            delete_DSU_file(path)

        elif ls[0] == "C":
            create_new_file(path, nls)
        elif ls[0] == "R":
            read_file_contents(path)
    
def getInput():
    userInput = input()
    userSplit = userInput.split()
    return userSplit

def main():
    userSplit = getInput()

    while userSplit[0][:1] != "Q":
        run_command(userSplit)
        print()
        userSplit = getInput()

if __name__ == "__main__":
    main()
