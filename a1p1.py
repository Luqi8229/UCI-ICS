
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

def recursive(path):
    content = []
    files = file_list(path)
    if len(files) > 0:
        content.append(files)
    
    directories = directory_list(path)
    if len(directories) > 0:
        for dir in directories:
            dPath = convert_to_Path(dir)
            content.append(dPath)
            content.append( file_list(dPath) )

    return content

def convert_to_Path(str):
    return Path(PurePath(str))

def print_info(info):
    for str in info:
        if type(str) is list:
            for sub in str:
                print(sub)
        else:
            print(str)

def list_contents(path, **options):
    myPath = convert_to_Path(path)
    content = []
    # PathTypes = [Path(ls[1]), PurePath(ls[1]), myPath]
    # print(PathTypes)
    
    if options["Recursive"] is True:
        content = recursive(myPath)

    print(options)
    print()
    print(content)
    print()
    print_info(content)

def run_command(ls):
    if ls[0] == "L":
        if ls[2] == "-r":
            list_contents(ls[1], Recursive = True)
        else:
            list_contents(ls[1])


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

