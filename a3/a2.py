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
    if ui.check_if_other_command(command, admin) is True:
        return filePath, profile, admin

    nls = ui.remove_list_info(info)

    co = False
    # when a profi  le HAS NOT been loaded
    if (command == "E" or command == "P") and profile == None:
        ui.print_admin_lines("Please create or load an existing file first.", admin)
    
    # when a profile has been loaded
    if profile != None and (command != "O" and command != "C"):
        if command == "E":
            mc.edit_DSU_file(profile.filepath, nls, admin)
        elif command == "P":
            mc.print_DSU_info(profile.filepath, nls, admin)
        elif command in ["-usr", "-pwd", "-bio", "-addpost", "-delpost", "-posts", "-post", "-all"]:
            RC = ui.prompt_info("Are you trying to Edit or Print? (E\P)", False, admin)
            runCommandLine([RC, command], filePath, profile, admin)
        return filePath, profile, admin
    path = None
    # if first phrase is something other than the command letter, prompt for it
    ls = ["L", "R", "C", "D", "O", "Q", "PP", "PUBLISH", "MM", "MENU", "MENUOC", "MENUL"]
    while ui.check_if_command(command.upper(), ls, "No command found") is False and admin is False:
        command = ui.prompt_info("Please enter a valid command", True, admin)
        if ui.check_if_other_command(command, admin) is True:
                return filePath, profile, admin
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
                p = ui.prompt_info("Please enter a valid directory", True, admin)
                path = Path(p)
                while ps.check_if_directory_file(path, True) is False:
                    ui.print_admin_lines("Enter 'create' to create a new DSU file", admin)
                    ans = ui.prompt_info("Please enter a valid directory", True, admin)
                    if ans == "create":
                        path = ui.prompt_info("Enter folder directory", True, admin)
                        name = ui.prompt_info("Enter new file name", True, admin)
                        name += ".dsu"
                        if mc.create_new_profile(path, ["-n", name], admin) is True:
                            profile = Profile()
                            path = profile.load_profile(path/name)
                    path = ui.split_user_info(ans)

    nls2 = ui.remove_list_info(info, 2)

    # breaking down the command
    if command == "L":
        mc.list_contents(path, nls2, admin)
    elif command == "D":
        mc.delete_DSU_file(path, admin)
    elif command == "R":
        if ps.check_if_dsu(path, admin) is True:
            mc.print_DSU_info(path, ["-all"], admin)
    elif command == "C":
        fPath = mc.create_new_profile(path, nls2, admin)
        if fPath != None:
            co = True
            filePath = fPath
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

