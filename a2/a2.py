# a2.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Luqi Chen
# luqic2@uci.edu
# 69278864

import ui
import mc
import ps
from Profile import *

# process the first letter of the commandline

def runCommandLine(info, filePath, profile = None, admin = False):
    command = info[0]
    if command == "ADMIN":
        admin = True
        return filePath, profile, admin
    elif command == "MENU" or command == "HELP":
        ui.run_menu()
        return filePath, profile, admin
    elif command == "USER":
        admin = False
        return filePath, profile, admin

    nls = ui.remove_list_info(info)
    nls2 = ui.remove_list_info(info, 2)

    co = False
    # when a profile HAS NOT been loaded
    if (command == "E" or command == "P" or command == "PP") and profile == None:
        ui.print_admin_lines("Please create or load an existing file first.", admin)
    
    # when a profile has been loaded
    if profile != None and (command != "O" and command != "C") :
        if command == "E":
            mc.edit_DSU_file(profile.filePath, nls, admin)
        elif command == "P":
            mc.print_DSU_info(profile.filePath, nls, admin)
        elif command == "PP":
            mc.publish_post_command(profile, nls, admin)
        return filePath, profile, admin
    path = None
    # if first phrase is something other than the command letter, prompt for it
    ls = ["L", "R", "C", "D", "O", "P", "Q"]
    while ui.check_if_command(command, ls, "No command found") is False and admin is False:
        command = ui.prompt_info("Please enter a valid command", admin)
    if ps.check_if_directory_file(info[0], False) is True:
        path = ps.convert_to_Path(info[0])

    if path == None:
        if admin is True:
            try:
                path = ps.convert_to_Path(info[1])
            except Exception:
                print("Invalid directory.")
                return filePath, profile, admin
        else:
            try:
                path = ps.convert_to_Path(info[1])
            except Exception:
                path = ps.convert_to_Path(ui.prompt_info("Please enter a directory", admin))
            while ps.check_if_directory_file(path, True) is False:
                ui.print_admin_lines("Enter 'create' to create a new DSU file", admin)
                ans = ui.prompt_info("Please enter a valid directory", admin)
                if ans == "create":
                    path = ps.convert_to_Path(ui.prompt_info("Enter folder directory", admin))
                    name = ui.prompt_info("Enter new file name", admin)
                    name += ".dsu"
                    if mc.create_new_profile(path, ["-n", name], admin) is True:
                        profile = Profile()
                        path = profile.load_profile(path/name)
                path = ans

    # breaking down the command
    if command == "L":
        mc.list_contents(path, nls2, admin)
    elif command == "D":
        mc.delete_DSU_file(path, admin)
    elif command == "R":
        if ps.check_if_dsu(path, admin) is True:
            mc.print_DSU_info(path, ["-all"], admin)
    elif command == "C":
        print(nls2)
        if mc.create_new_profile(path, nls2, admin) is True:
            co = True
            fileName = info[-1]
            filePath = ps.get_filePath(path, fileName)
            if admin is False:
                ui.run_OC_menu("creating")
    elif command == "O":
        if mc.open_DSU_file(path, admin) is True:
            co = True
            filePath = path
            if admin is False:
                ui.run_OC_menu("opening")
    else:
        print("Invalid command")

    if co is True:
        profile = Profile()
        profile.load_profile(str(filePath))
        co = False

    return filePath, profile, admin
