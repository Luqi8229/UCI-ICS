# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Luqi Chen
# luqic2@uci.edu
# 69278864

import ui
from Profile import *

############### admin and input stuff ###########################
def print_admin_lines(message:str, admin=False, aMess:bool = False, aMessage:str = "Invalid command"):
    if admin == True:
        if aMess is True:
            print(f"{aMessage}.")
        else:
            pass
    else:
        print(f'\n{message}')

def get_profile_info(admin):
    user = ""
    pswd = ""
    bio = ""
    if admin is True:
        pass
    else:
        user = input("Enter username:\n")
        pswd = input("Enter password:\n")
        bio = input("Enter a bio (don't use '):\n")
    return user, pswd, bio

def get_edit_info(command:str):
    info = {"-usr": "username", "-pwd": "password", "-bio":"bio", "-addpost":"post"}
    type = info[command]
    userInput = input(f"Please enter your new {type}:\n")
    return userInput

def confirm_change(type:str, og:str, new:str, admin) -> bool:
    if admin == True:
        return True
    else:
        print(f'Confirm {type} change: {og} -> {new}? (yes/no)')
        confirmation = input()
    if confirmation.lower() == "yes":
        print(f'{type} has been changed.')
        return True
    return False

def prompt_info(message:str, admin, aInput = False):
    if admin is True:
        if aInput is True:
            userInput = input()
        else:
            print("Invalid command.")
            return
    else:
        userInput = input(f'\n{message}:\n')
    return userInput

def continue_listing():
    userInput = input("\nWould you like to continue using the L function? (yes/no)\n")
    while userInput.lower() not in ["yes", "no"]:
        userInput = input("Invalid response. Try again:")
    if userInput.lower() == "yes":
        print("\nEnter 'stop' to stop using L function.\n(Type 'menu' for the menu)\n")
        options = input("What would you like to try next?\n")
        if options.lower == "menu":
            run_L_menu()
            options = input("Please enter your next input:\n")
        return split_user_info(options)
    return "no"

# def continue_prompting():




##########################################################

def delete_post(profile, admin = False):
    posts = index_all_posts(profile.get_posts())
    if posts == "You have no posts.":
        print(posts) #prints 'You have no posts'
    else:
        print(posts)
        index = prompt_info("Which post would you like to delete?\n", admin)
        postTD = profile.get_post_by_ID(id = int(index)-1)
        if confirm_change("Post", "remove", postTD, admin) is True:
            deleted = profile.del_post(int(index)-1)
            print("deleted:", deleted)

def index_all_posts(info:list) -> str:
    contents = ""
    if len(info) > 0:
        for i in range(len(info)):
            contents += f'{i+1}. {info[i]}'
    else:
        contents = "\nYou have no posts."
    return contents

def check_if_command(comm:str, info:list, prin:bool = True, message:str = "Invalid command") -> bool:
    if comm in info:
        return True
    else:
        if prin is True:
            print(f"{message}.")
        return False

def remove_list_info(ls, stride=1):
    return [ls[i] for i in range(len(ls)) if i > (stride-1)]

def format_print(type, info) -> str:
    return f'\n{type}: {info}'

def print_info(info):
    for str in info:
        if type(str) is list:
            print_info(str)
        else:
            print(str)

############### starting functions #######################

def runStarter(admin = False):
    userInput = prompt_info("What would you like to do?", admin, True)
    userSplit = split_user_info(userInput)
    return userSplit

def split_user_info(info):
    contents = []
    quotationFound = False

    info = info.replace("'", '"', info.count("'")) + " "
    currentStr = ""
    for chr in info:
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
        else:
            currentStr += chr
    return contents

#################### menus ##########################3

def run_menu():
    print("Main Menu",
          "\nL [DIR] | List contents for specific directory",
          "\nR [FILE DIR] | Reads the contents of a DSU file"
          "\nC [DIR] -n [fileName] | Create new DSU file in specific directory",
          "\nD [FILE DIR] | Delete the DSU file from the file directory",
          "\nO [FILE DIR] | Opens existing DSU file",
          "\nMenu | Prints this menu", 
          "\nQ | Quit program"
          )

def run_OC_menu(type):
    print()
    print(f"Here's some commands for {type} the DSU file:",
          "\nE | Edit the DSU file", 
          "\n\t -usr [USERNAME] | to edit username",
          "\n\t -pwd [PASSWORD] | to edit password",
          "\n\t -bio [BIO] | to edit bio",
          "\n\t -addpost [NEW POST] | to create a new post (give string phrase)",
          "\n\t -delpost | delete post identified by ID",
          "\nP | Print data stored in the DSU file",
          "\n\t -usr | print username",
          "\n\t -pwd | print password",
          "\n\t -bio | print bio",    
          "\n\t -posts | prints all posts",
          "\n\t -post [ID] | print post identified by ID",
          "\n\t -all | print all contents",
          "\nMenu | Prints this menu" 
    )

def run_L_menu():
    print()
    print(f"Here's some commands for listing contents:",
          "\n -r [OPTIONS] | for recursive output"
          "\n\t options: -f, -s, -e"
          "\n -f | for files only",
          "\n -s [FILENAME] | for files given file name (including extension)",
          "\n -e [EXTENSION] | for select extentions given ext",
          "\n Menu | Prints this menu"
    )

