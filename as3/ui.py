
import ps

def prompt_info(message, admin=False, string = True, command=False, option=''):
    userInput = ""
    if admin is False:
        userInput = input(f'{message}:\n')
    else:
        userInput = input()
    
    while len(userInput) == 0:
        aline("Input can not be empty")
        userInput = prompt_info(message, admin)

    if command is True:
        while command_exist(userInput, option, admin) is False:
            userInput = input("Please select an option from the menu:\n")

    content = remove_quotations(userInput)
    if string is True:
        response = ''
        for elem in content:
            response += elem
        content = response
        
    return content

def aline(message, admin=False):
    if admin is False:
        print(message)

def yes_or_no(message, admin = False):
    message += "? (yes/no)"
    ans = prompt_info(message, admin, True)
    while ans.lower() not in ['yes', 'no']:
        ans = prompt_info("That is not a valid response. Please enter either 'yes' or 'no'", admin, True)
    return ans

def remove_info(info:list, nElements = 1):
    nl = []
    for index in range(len(info)):
        if index > (nElements-1):
            nl.append(info[index])
    return nl

def command_exist(com, option, admin = False):
    commandList = ['list', 'dsu', 'publish', 'menu', 'admin']
    L_list = ['all', 'files', 'name', 'ext', 'menu', 'q']
    LR_list = ['files', 'name', 'ext']
    EP_list = ['username', 'password', 'bio', 'post', 'all', 'menu', 'q']

    lists = {"command": commandList, "list": L_list, "LR": LR_list, "edit": EP_list, "print":EP_list}
    opList = lists[option]

    if com in opList:
        return True
    if admin is False:
        print("Command does not exist.")
    return False

def remove_quotations(info:str) -> list:
    contents = []
    qFound = False
    info = info.replace("'", '"', info.count("'"))

    curStr = ""
    for i in range(len(info)):
        chr = info[i]
        if chr == '"':
            if qFound is False:
                qFound = True
            elif qFound is True:
                qFound = False
                contents.append(curStr)
                curStr = ""
        elif chr == " ":
            if qFound is False:
                if curStr == "":
                    continue
                else:
                    contents.append(curStr)
                    curStr = ""
            else:
                curStr += chr
        elif (i + 1) == len(info):
            curStr += chr
            contents.append(curStr)
        else:
            curStr += chr
    return contents

def list_to_string(info:list):
    contents = ""
    for elm in info:
        if type(elm) is list:
            contents += list_to_string(elm)
        else:
            contents += str(elm) + "\n"
    return contents

##################### MC Options ##########################3

def add_heading(option, con:str, searchInfo):
    content = ''
    if len(con) > 0:
        messageDict = {'files': "Here are all your files:",
                       'name': f"Here are all your files under the name '{searchInfo}':",
                       'ext': f"Here are all your files with the '{searchInfo}' extension:"
                       }
        message = "\n" + messageDict[option] + "\n"
        content = message + con
    else:
        content = f"\nYou have no files under {searchInfo}." + con
    return content

def prompt_name(admin=False):
    fName = prompt_info("What file are you looking for?", admin)
    if "." not in fName:
        extAns = yes_or_no("Is there a specific extension you want to add", admin)
        if extAns == "yes":
            fExt = prompt_info("What is the extension?", admin)
            if fExt.startswith(".") is False:
                fExt = "." + fExt
        else:
            fExt = ".*"
        fileName = fName + fExt
    else:
        fileName = fName
    
    return fileName

def select_name(filePath, fileName):
    contents = []

    if "*" in fileName:
        contents.append( ps.select_filestem(filePath, fileName) )
    else:
        contents.append( ps.select_fileName(filePath, fileName) )
    
    return contents

def prompt_ext(admin=False):
    fExt = prompt_info("What extension are you looking for?", admin)
    return fExt
    
def prompt_files(admin):
    return 'files'

################## MENUS ########################################

def run_menu():
    print(f"{'Main Menu':-^50}",
          "\n  list    | List contents for specific directory",
          "\n  DSU     | to manage a DSU file",
          "\n  publish | Publish to the ICS 32 DSU server",
          "\n  menu    | Prints this menu", 
          "\n  Q | Quit program"
          )
    
def run_L_menu():
    print("\nHere's some options for listing contents:",
          "\n  all   | to print all files and directories",
          "\n  files | for files only",
          "\n  name  | for files given file name (including extension)",
          "\n  ext   | for select extentions given ext",
          "\n  menu  | Prints this menu", 
          "\n  Q | to exit this menu"
    )

def run_R_menu():
    print(f"{'Menu':-^60}",
          "\n  files | list all the files",
          "\n  name  | list all files with a specific name",
          "\n  ext   | list all files with a specific extension"
          )

def run_E_menu():
    print("What would you like to edit?",
          "\n  username | to edit username",
          "\n  password | to edit password",
          "\n  bio      | to edit bio",
          "\n  post     | to edit your posts",
          "\n  all      | to edit all of the above",
          "\n  menu     | Prints this menu", 
          "\n  Q | to exit this menu"
          )
    
def run_P_menu():
    print("What would you like to print?",
          "\n  username | to print username",
          "\n  password | to print password",
          "\n  bio      | to print bio",
          "\n  post     | to print your posts",
          "\n  all      | to print everything",
          "\n  menu     | Prints this menu", 
          "\n  Q | to exit this menu"
    )