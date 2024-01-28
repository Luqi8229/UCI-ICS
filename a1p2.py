
#user input format : [command] [input] -[option] [input]
# Possible commands:
# L - list contents of user specified directory
# Q - Quit program

from pathlib import Path, PurePath, PurePosixPath

#sort contents for files
def file_list(path):
    return [i for i in path.iterdir() if i.is_file()]

#sort contents for directories/folders
def directory_list(path):
    return [i for i in path.iterdir() if i.is_dir()]

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
    return [fil for fil in file_list(path) if fil.suffix == ext]

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

def run_command(ls):
    if ls[0] == "L":
        path = convert_to_Path(ls[1])
        nls = remove_list_info(ls, 2)
        list_contents(path, nls)

def main():
    userSplit = input().split()

    while userSplit[0] != "Q":
        run_command(userSplit)
        print()
        userSplit = input().split()

if __name__ == "__main__":
    main()
