
#user input format : [command] [input] -[option] [input]
# Possible commands:
# L - list contents of user specified directory
# Q - Quit program

from pathlib import Path, PurePath

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

def recursive_contents(path, options=[]):
    content = []
    files = file_list(path)
    if len(files) > 0:
        content.append(files)
    
    directories = directory_list(path)
    if len(directories) > 0:
        for dir in directories:
            dPath = convert_to_Path(dir)
            if "-f" not in options:
                content.append(dPath)
            else:
                content.append( file_list(dPath) )

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
            pass
        elif options[0] == "-e":
            pass
    print_info(contents)

def convert_to_Path(str):
    return Path(PurePath(str))

def remove_list_info(ls, stride=1):
    return [ls[i] for i in range(len(ls)) if i > (stride-1)]

def run_command(ls):
    if ls[0] == "L":
        path = convert_to_Path(ls[1])
        # if ls[2] == "-r":
        #     list_recursive_contents(path)
        #     if ls[3] == "-s":
        #         pass
        # elif ls[2] == "-f":
        #     list_file_contents(path)
        # else:
        nls = remove_list_info(ls, 2)
        list_contents(path, nls)

def discardPaths(ls):
    nls = []
    for i in range(len(ls)-2): #discard C:/Users && c:/Users
        if "&" in ls[i]:
            nls.append(ls[i][0: len(ls[i]) - 1])
    return nls 

def main():
    userSplit = input().split()
    print("og=", userSplit)
    
    # userSplit = discardPaths(userSplit)
    # print()
    # print(userSplit)
    # list_contents(userSplit)

    while userSplit[0] != "Q":
        run_command(userSplit)
        userSplit = input().split()
        userSplit = discardPaths(userSplit)

if __name__ == "__main__":
    main()
