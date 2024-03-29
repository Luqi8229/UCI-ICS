
import ps

######################### List Functions #################################

def prompt_files(admin = False):
    return 'files'

def prompt_name(admin = False):
    name = prompt_info("What is the name of the file you want to find?", admin)
    if "." not in name:
        exAns = yes_or_no("Is there a specific extension you want to search?", admin)
        if exAns == "yes":
            ext = prompt_info("What is the extension you want to add?", admin)
            name += ext
        else:
            name += ".*"
    return name

def prompt_ext(admin = False):
    ext = prompt_info("What is the extension you want to find?", admin)
    return ext

def select_name(filePath, fileName):
    if "*" in fileName:
        name = fileName[:-2]
        contents = ps.select_filestem(filePath, name)
    else:
        contents = ps.select_filename(filePath, fileName)
    return contents

def add_heading(option, contents, searchInfo):
    messageDict = {'all': "Here are all your files and directories",
                   'files': "Here are your files:",
                   'name' : f"Here are your {searchInfo} files:",
                   'ext' : f"Here are your files with {searchInfo}:",
                   'empty' : f"You have no files with the {option} {searchInfo}"
                   }
    if len(contents) > 0:
        message = messageDict[option] + "\n"
    else:
        message = messageDict['empty'] + "\n"
    contents = "\n" + message + contents
    return contents

############################### DSU Functions #############################3

def profile_info(admin=False):
    user = prompt_info("Enter a username", admin)
    while len(user) < 3:
        aline("Username must be longer than 4 characters", admin)
        user = prompt_info("Enter a username", admin)

    pswd = prompt_info("Enter a password", admin)
    while len(pswd) < 3:
        aline("Password must be longer than 4 characters", admin)
        pswd = prompt_info("Enter a password", admin)
    
    if admin is False:
        bio = input("\nEnter a bio (don't use ')\nPlease enter if you don't want to add one")
    else:
        bio = input()
    if len(bio) == 0:
        bio = None
    return user, pswd, bio

############################################### Functions ######################

def prompt_directory(admin=False, dsu=False, prompt = "Please enter a directory"):
    dir = prompt_info(prompt, admin)
    try:
        path = ps.path(dir)
        if dsu is True and dir.endswith(".dsu") is False:
            dir = dir + ".dsu"
            path = ps.path(dir)
    except:
        if dsu is True:
            print("Invalid DSU file")
        else:
            print("Invalid directory")
        
        path = prompt_info("Please enter a valid directory", admin)
        while ps.pathExist( ps.path(path) ) is False:
            path = prompt_info("Please enter a valid directory", admin)
    return path

def prompt_folder(admin=False):
    dir = prompt_info("Please enter the directory of the folder you want to save in", admin)
    while ps.isFolder( ps.path(dir) ) is False:
        aline("That is not a directory")
        dir = prompt_info("Please enter a valid folder directory", admin)
    return dir

def prompt_info(prompt:str, admin = False, str = True, command = False, option = ''):
    if admin is True:
        userInput = input()
    else:
        userInput = input(f'\n{prompt}:\n')

    if len(userInput) == 0:
        aline("Input can not be empty.")
        userInput = prompt_info(prompt, admin, str, command, option)
    
    userInput = remove_quotations(userInput)

    if str is True:
        userInput = list_to_string(userInput)
        st = ""
        for elem in userInput:
            st += elem
        userInput = st
    
    if command is True:
        while command_exist(userInput, option) is False:
            userInput = input(f"\n{prompt}:\n")

    return userInput
    
def yes_or_no(prompt:str, admin=False):
    user = input(f'\n{prompt}? (yes/no):\n')
    while user.lower() not in ['yes', 'no']:
        if admin is False:
            user = input("That is not a valid response, please enter 'yes' or 'no':\n")
    return user

def aline(message:str, admin=False):
    if admin is False:
        print(message)

def command_exist(comm: str, option:str):
    mainList = ['list', 'dsu', 'publish', 'menu']
    lList = ['all', 'files', 'name', 'ext', 'menu']
    rList = ['files', 'name', 'ext', 'menu']
    edpr = ['edit', 'print']
    epList = ['username', 'password', 'bio', 'post', 'all', 'menu']

    opDict = {'main':mainList, 'list':lList, 'recur':rList, 'edpr': edpr, 'ep':epList}

    if comm.lower() in opDict[option]:
        return True
    print(f'{comm} does not exist')
    return False

def list_to_string(info:list):
    contents = ""
    for elm in info:
        if type(elm) is list:
            contents += list_to_string(elm) + "\n"
        elif elm != info[-1]:
            contents += str(elm) + "\n"
        else:
            contents += str(elm)
    return contents

def remove_quotations(info:str):
    contents = []
    quotationFound = False
    info = info.replace("'", '"', info.count("'"))

    currentStr = ""
    for i in range(len(info)):
        chr = info[i]
        if chr == '"':
            if quotationFound is False:
                quotationFound = True
            elif quotationFound is True:
                quotationFound = False
                contents.append(currentStr)
                currentStr = ""
        elif chr == " ":
            if quotationFound is False:
                if currentStr == "":
                    continue
                else:
                    contents.append(currentStr)
                    currentStr = ""
            elif quotationFound is True:
                currentStr += chr
        elif i == len(info)-1:
            currentStr += chr
            contents.append(currentStr)
        else:
            currentStr += chr
    return contents

##################### MENUS ##########################

def run_M_menu():
    print(f"{'Main Menu':-^50}",
          "\n list    | list contents from a directory",
          "\n DSU     | manage a DSU file",
          "\n publish | publish to the ICS 32 server",
          "\n menu    | to print this menu",
          "\n q | quit",
          )
    
def run_L_menu():
    print(f"\n{'Listing options':-^40}",
          "\n all   | to list all files and directories",
          "\n files | to list only files",
          "\n name  | to list a specific file name",
          "\n ext   | to list files under a specific extension",
          "\n menu  | to print this menu",
          )
    
def run_R_menu():
    print(f"\n{'Menu':-^40}",
          "\n files | list all files",
          "\n name  | list all files under specific file name",
          "\n ext   | list all specific extensions",
          "\n menu  | print this menu",
          )

# DSU file / profile created/loaded. What would you like to do?
def run_E_menu():
    print(f"\n{'Edit Menu':-^40}",
          "\n username | to edit username",
          "\n password | to edit password",
          "\n bio      | to edit bio",
          "\n post     | to edit your posts",
          "\n all      | to edit everything"
          "\n menu     | to print this menu",
          )

def run_P_menu():
    print(f"\n{'Print Menu':-^40}",
          "\n username | to print username",
          "\n password | to print password",
          "\n bio      | to print bio",
          "\n post     | to print your posts",
          "\n all      | to print everything",
          "\n menu     | to print this menu",
          )


