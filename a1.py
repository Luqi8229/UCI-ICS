
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

def print_info(info):
    for str in info:
        if type(str) is list:
            print_info(str)
        else:
            print(str)

def select_filename(path, name):
    return [fil for fil in file_list(path) if fil.name == name]
    
def select_extension(path, ext):
    if ext.startswith(".") is False:
        ext = "." + ext
    # return [fil for fil in file_list(path) if fil.suffix == ext]
    return Path('.').glob(f'**/*{ext}')

def recursive_contents(path, options=[]):
    content = []
    directories = directory_list(path)
    numDirectory = len(directories)
    for i in range(numDirectory + 1):
        if len(options) == 0:
            content.append( path )
            content.append( file_list(path) )
        else:
            if "f" in options:
                content.append( file_list(path) )
            elif "s" in options:
                content.append( select_filename(path, options[1]) )
            elif "e" in options:
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
        contents.append( default_contents(path) )
    else:
        nOptions = remove_list_info(options)
        if options[0] == "-r":
            if len(nOptions) > 0:
                contents.append( recursive_contents(path, nOptions) )
            else:
                contents.append( recursive_contents(path) )
        elif options[0] == "-f":
            contents.append( file_list(path) )
        elif options[0] == "-s":
            contents.append( select_filename(path, options[1]) )
        elif options[0] == "-e":
            contents.append( select_extension(path, options[1]) )
    print_info(contents)

def convert_to_Path(str):
    return Path(PurePath(str))

def remove_list_info(ls, stride=1):
    return [ls[i] for i in range(len(ls)) if i > (stride-1)]

def create_new_file(path, input):
    if input[0] != "-n":
        print("Incorrect feature; must be -n (name)")
        return
    else:
        file_name = input[1] + ".dsu"
        file = path / file_name
        file.touch()
        
def delete_DSU_file(path):
    if check_if_dsu(path) is True:
        path.unlink()
        print(path, "DELETED")
        
def print_dsu_content(path):
    file = path.parts[-1]
    
    if path.stat().st_size == 0:
        print("EMPTY")
        return

    with open(file, "r") as f:
        for line in f.readlines():
            print(line)

def check_if_dsu(path):
    if path.suffix != ".dsu":
        print("ERROR: not a dsu file, try again")
        return False
    return True

def check_if_directory_file(path):
    if path.is_dir() is True or path.is_file() is True:
        return
    else:
        print("ERROR: no directory given")

def run_command(ls):
    path = convert_to_Path( ls[1] )
    check_if_directory_file(path)
    nls = remove_list_info(ls, 2)

    if ls[0].startswith("L"):
        list_contents(path, nls)
    elif ls[0].startswith("C"):
        create_new_file(path, nls)
    elif ls[0].startswith("D"):
        delete_DSU_file(path)
    elif ls[0].startswith("R"):
        print_dsu_content(path)
    
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
