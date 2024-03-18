


def prompt_info(prompt:str, admin = False, str = True, command = False, option = ''):
    if admin is True:
        userInput = input()
    else:
        userInput = input(f'{prompt}:\n')

    if len(userInput) == 0:
        aline("Input can not be empty.")
        userInput = prompt_info(prompt, admin, str, command, option)
    
    userInput = remove_quotations(userInput)

    if str is True:
        st = ""
        for elem in userInput:
            st += elem
        userInput = st

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
    mainList = ['list', 'dsu', 'publish', 'admin']
    lList = ['all', 'files', 'name', 'ext']
    rList = ['files', 'name', 'ext']
    epList = ['username', 'password', 'bio', 'post', 'all']

    opDict = {'main':mainList, 'list':lList, 'recur':rList, 'ep':epList}

    if comm in opDict[option]:
        return True
    print(f'{comm} does not exist')
    return False

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
    print(f"{"Main Menu":-^50}",
          "\n list | list contents from a directory",
          "\n DSU | manage a DSU file",
          "\n publish | publish to the ICS 32 server",
          "\n menu | to print this menu",
          "\n q | quit",
          )
    
def run_L_menu():
    print("\nListing options",
          "\n all | to list all files and directories",
          "\n files | to list only files",
          "\n name | to list a specific file name",
          "\n ext | to list files under a specific extension",
          "\n menu | to print this menu",
          )
    
def run_R_menu():
    print("\nMenu",
          "\n files | list all files",
          "\n name | list all files under specific file name",
          "\n ext | list all specific extensions",
          "\n menu | print this menu",
          )

# DSU file / profile created/loaded. What would you like to do?
def run_E_menu():
    print("\nEdit Menu",
          "\n username | to edit username",
          "\n password | to edit password",
          "\n bio | to edit bio",
          "\n post | to edit your posts",
          "\n all | to edit everything"
          "\n menu | to print this menu",
          )

def run_P_menu():
    print("\nPrint Menu",
          "\n username | to print username",
          "\n password | to print password",
          "\n bio | to print bio",
          "\n post | to print your posts",
          "\n all | to print everything",
          "\n menu | to print this menu",
          )


