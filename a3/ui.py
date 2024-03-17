# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Luqi Chen
# luqic2@uci.edu
# 69278864

import ps
import mc
import ds_client
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
        user = input("Enter a username:\n")
        pswd = input("Enter a password:\n")
        bio = input("Enter a bio (don't use ')\n(leave empty if you don't want to add one): ")
        if len(bio) == 0:
            bio = None
    return user, pswd, bio

def get_edit_info(command:str):
    info = {"-usr": "username", "-pwd": "password", "-bio":"bio", "-addpost":"post"}
    type = info[command]
    userInput = input(f"Please enter your new {type}:\n")
    return userInput

def confirm_change(tp:str, og:str, new:str, admin) -> bool:
    if admin == True:
        return True
    else:
        print(f'Confirm {tp} change: {og} -> {new}? (yes/no)')
        confirmation = input()
    if confirmation.lower() == "yes":
        print(f'{tp} has been changed.')
        return True
    return False

def prompt_info(message:str, str = False, admin=False, aInput = False):
    if admin is True:
        if aInput is True:
            userInput = input()
        else:
            print("Invalid command.")
            return
    else:
        userInput = input(f'\n{message}:\n')
    userInput = split_user_info(userInput)

    if str is True:
        st = ""
        for elem in userInput:
            st += elem
        userInput = st

    if len(userInput) == 0:
        print("Input can not be empty.")
        userInput = prompt_info(message, str, admin, aInput)

    return userInput

def continue_listing():
    userInput = yes_or_no("Would you like to continue using the L function")
    if userInput.lower() == "yes":
        print("\nEnter 'stop' to stop using L function.\n(Type 'menu' for the menu)\n")
        options = prompt_info("What would you like to try next?")
        if options[0].lower() == "menu":
            run_L_menu()
            options = prompt_info("Please enter your next input")
        return options
    return ["no"]


##########################################################

def check_if_other_command(com, admin=False):
    command = com.upper()
    if command in ["PP", "PUBLISH", "MM", "MENU", "MENUOC", "MENUL"]:
        if command == "ADMIN":
            admin = True
        elif command == "MENU" or command == "HELP" or command == "MM":
            run_menu()
        elif command == "MENUOC":
            run_OC_menu()
        elif command == "MENUL":
            run_L_menu()
        elif command == "USER":
            admin = False
        elif command in ["PP", "PUBLISH"]:
            ds_client.send(None, 3021, None, None, None, None)
        return True
    return False

def choose_profile():
    profile = Profile()
    use_ex = yes_or_no("Would you like to use an existing profile")

    if use_ex.lower() == "yes":
        print("(If you don't have an existing DSU file, enter 'create' to create a DSU file)")
        fp = prompt_info("Please input your DSU file path", True)
        filePath = Path(fp)
        while ps.check_if_DSU_file(filePath) is False:
            fp = prompt_info("Please enter a new directory", True)
            filePath = Path(fp)
            if fp.lower() == "create":
                path = prompt_info("Please enter the directory you want to save your file in", True)
                while ps.check_if_directory_file(path) is False:
                    path = prompt_info("Please enter a valid directory", True)
                fileName = prompt_info("What are you going to name your file?", True)
                if fileName.endswith(".dsu") is False:
                    fileName += ".dsu"
                mc.create_new_profile(Path(path), ["-n", fileName])
                filePath = Path(path)/fileName
                return filePath
            
        profile.load_profile(str(filePath))
        if len(profile._posts) ==  0:
            print("Looks like you don't have any posts to publish.")

    elif use_ex.lower() == "no":
        print("\nAlright! Let's make a new profile.\nFirst, we need to create a file to save your profile.")
        fileFolder = prompt_info("Enter the directory of the folder you want to save your profile into", True)
        fileFolder = Path(fileFolder)
        while ps.check_if_directory_file(fileFolder, False) is False:
            fileFolder = prompt_info("This file directory does not exist.\nPlease enter a new directory", True)
            fileFolder = Path(fileFolder)
        fileName = prompt_info("Give a name for the file", True)

        if fileName.endswith(".dsu") is False:
            fileName += ".dsu"
        filePath = fileFolder / fileName

        info = ["-n", fileName]
        mc.create_new_profile(fileFolder, info)

    profile.load_profile(str(filePath))
    if len(profile._posts) == 0:
        print("Let's create your first post!")
        create_post(filePath)

    return filePath

def yes_or_no(prompt:str):
    ip = input(f"\n{prompt}? (yes/no): ")
    while ip.lower() not in ["yes", "no"]:
        ip = input("That is not a valid response, please enter 'yes' or 'no': ")

    return ip

def confirm_publish(post_entry):
    change = yes_or_no(f'Confirm publish: {post_entry}')
    if change.lower() == "yes":
        return True
    return False

def continue_create_post(filePath, admin=False):
    cont = yes_or_no("Would you like to create another post")
    while cont.lower() != "no":
        create_post(filePath, True)
        cont = yes_or_no("Would you like to create another post")

def create_post(filePath, repeating = False, admin=False):
    profile = Profile()
    profile.load_profile(str(filePath))

    entry = prompt_info("Enter your new post", True, admin)
    profile.add_post(Post(entry))

    print_admin_lines("New post added!", admin)
    profile.save_profile(str(filePath))
    if repeating is False:
        continue_create_post(filePath)

def delete_post(profile, admin = False):
    posts = index_all_posts(profile.get_posts())
    if posts == "You have no posts.":
        print(posts) #prints 'You have no posts'
    else:
        print(posts)
        index = prompt_info("Which post would you like to delete?", False, admin)
        postTD = profile.get_post_by_ID(id = int(index)-1)
        if confirm_change("Post", "remove", postTD, admin) is True:
            deleted = profile.del_post(int(index)-1)
            print("deleted:", deleted)

def index_all_posts(info:list) -> str:
    contents = ""
    if len(info) > 0:
        for i in range(len(info)):
            post = Post(info[i])
            entry = post.get_entry()
            entry2 = entry["entry"]
            contents += f'{i+1}. {entry2}\n'
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
    userInput = prompt_info("What would you like to do?", False, admin, True)
    return userInput

def split_user_info(info:str):
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

#################### menus ##########################3

def run_menu():
    print("Main Menu",
          "\nL [DIR] | List contents for specific directory",
          "\nR [FILE DIR] | Reads the contents of a DSU file"
          "\nC [DIR] -n [fileName] | Create new DSU file in specific directory",
          "\nD [FILE DIR] | Delete the DSU file from the file directory",
          "\nO [FILE DIR] | Opens existing DSU file",
          "\nPP or Publish | Publishes to the ICS 32 DSU server",
          "\nMM or Main Menu | Prints this menu", 
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
          "\nMenuOC | Prints this menu"
    )

def run_L_menu():
    print()
    print(f"Here's some commands for listing contents:",
          "\n -r [OPTIONS] | for recursive output"
          "\n\t options: -f, -s, -e"
          "\n -f | for files only",
          "\n -s [FILENAME] | for files given file name (including extension)",
          "\n -e [EXTENSION] | for select extentions given ext",
          "\n MenuL | Prints this menu"
    )

