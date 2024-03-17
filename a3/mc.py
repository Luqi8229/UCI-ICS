# mc.py
# main commands break down

# Luqi Chen
# luqic2@uci.edu
# 69278864

import ui
import ps
from Profile import *
import ds_client


def print_DSU_info(path, info, admin):
    print_info = ""
    profile = Profile()
    profile.load_profile(str(path))
    ls = ["-usr", "-pwd", "-bio", "-posts", "-post", "-all"]
    for index in range(len(info)):
        command = info[index]
        if ui.check_if_command(command, ls) is True:
            if command == "-usr":
                print_info += ui.format_print("Username", profile.username)
            elif command == "-pwd":
                print_info += ui.format_print("Password", profile.password)
            elif command == "-bio":
                print_info += ui.format_print("Bio", profile.bio)
            elif command == "-posts":
                print_info +=  ui.index_all_posts(profile.get_posts())
            elif command == "-post":
                try:
                    print_info += profile.get_post_by_ID(info[index+1]) + "\n"
                except IndexError as ex:
                    ui.print_admin_lines("Index is not within the range to delete.\nUse 'P -posts' to see all posts.", admin, True, )
            elif command == "-all":
                print_info += ui.format_print("Username", profile.username)
                print_info += ui.format_print("Password", profile.password)
                print_info += ui.format_print("Bio", profile.bio)
                print_info += ui.index_all_posts(profile.get_posts())
            else:
                print(f'{command} is an invalid feature.')
    print(print_info)

def edit_DSU_file(path, info, admin):
    profile = Profile()
    profile.load_profile(str(path))
    for index in range(len(info)):
        command = info[index]
        ls = ["-usr", "-pwd", "-bio", "-addpost", "-delpost"]
        if ui.check_if_command(command, ls, False) is True:
            if command in ["-usr", "-pwd", "-bio"]:
                try: 
                    if info[index+1].startswith("-") and admin is False:
                        change = ui.get_edit_info(command)
                    else:
                        change = info[index+1]
                except IndexError:
                    if admin is True:
                        command = "invalid"  
                    else:
                        change = ui.get_edit_info(command)
                if command == "-usr":
                    if ui.confirm_change("Username", profile.username, change, admin) is True:
                        profile.username = change
                elif command == "-pwd":
                    if ui.confirm_change("Password", profile.password, change, admin) is True:
                        profile.password = change
                elif command == "-bio":
                    if ui.confirm_change("Bio", profile.bio, change, admin) is True:
                        profile.bio = change
            elif command == "-addpost":
                try:
                    newPost = Post(info[index+1])
                except IndexError:
                    if admin is True:
                        pass
                    else:
                        newPost = Post( ui.get_edit_info(command) )
                profile.add_post(newPost)
                ui.print_admin_lines("New post added!", admin)
            elif command == "-delpost":
                ui.delete_post(profile, admin)
            else:
                print("Invalid command...")
            profile.save_profile(str(path))
        else:
            pass

def create_new_profile(path, info, admin=False):
    fileName = None
    if len(info) == 0 or info[0] != "-n":
        if admin is True:
            print("Invalid command.")
            return 
        else:
            info.insert(0, "-n")
    try:
        fileName = info[1]
    except:
        if admin is True:
            print("Invalid command.")
            return 
        else:
            fileName = ui.prompt_info("Please give a name for the file", True, admin)
    if fileName.endswith(".dsu") is False:
        fileName += ".dsu"
        info.insert(1, fileName)
    filePath = path / fileName
    if filePath.exists():
        print("File already exists.")
        if admin is False:
            ui.print_admin_lines("Loading file...", admin) 
            open_DSU_file(filePath, admin)
    else:
        if admin is False:
            ps.create_new_file(path, info)
            server = ui.prompt_info("What is the server address?",True)
            user, pswd, biop = ui.get_profile_info(admin)
            profile = Profile(dsuserver = server, filepath = str(filePath), username = user, password = pswd, bio =biop)
            profile.save_profile(str(filePath))
            ui.print_admin_lines("Profile created", admin)
        else:
            return 
    return filePath

def delete_DSU_file(path, admin):
    if ps.check_if_dsu(path, admin) is True:
        if ui.confirm_change("file", "remove", path.name, admin) is True:
            path.unlink()
            print(path, "DELETED")

def open_DSU_file(path, admin):
    if path.suffix == ".dsu":
        if path.exists():
            profile = Profile()
            profile.load_profile(str(path))
            ui.print_admin_lines(f"opened Profile: {profile.username}", admin)
            return True
    ui.print_admin_lines("File does not exist. Try 'C' to create a new DSU file.", admin, True)
    return False     

def recursive_contents(path, admin, options=[]):
    content = []
    directories = ps.directory_list(path)
    numDirectory = len(directories)
    for i in range(numDirectory + 1):
        if len(options) == 0:
            ui.print_admin_lines("Here are all your files and directories:", admin)
            content.append( path )
            content.append( ps.file_list(path) )
        else:
            if "-f" in options:
                ui.print_admin_lines("Here are all your files:", admin)
                content.append( ps.file_list(path) )
            elif "-s" in options:
                try:
                    select = options[1]
                except Exception:
                    if admin is True:
                        return "None"
                    else:
                        select = ui.prompt_info("Please enter a filename", True, admin)
                if admin is False:
                    while "." not in select:
                        ui.print_admin_lines("Missing extension. Try again:", False, admin)
                        select = ui.prompt_info("Please enter a filename", True, admin)
                    options.append(select)
                elif admin is True and "." not in select:
                    return "None"
                selectFiles = ps.select_filename(path, select)
                if len(selectFiles) == 0:
                    ui.print_admin_lines(f"There are no files with {select} name.", admin)
                else:
                    ui.print_admin_lines(f"Here are all your {select} files:", admin)
                    content.append(selectFiles)
            elif "-e" in options:
                try:
                    ext = options[1]
                except Exception:
                    if admin is True:
                        print("Invalid command.")
                        return "None"
                    else:
                        ext = ui.prompt_info("Please enter an extension", False, admin)
                        options.append(ext)
                extFiles = ps.select_extension(path, ext)
                if len(extFiles) == 0:
                    ui.print_admin_lines(f"There are no files with {ext} extension.", admin)
                else:
                    ui.print_admin_lines(f"Here are all your {ext} files:", admin)
                    content.append( ps.select_extension(path, ext) )
        if i == numDirectory:
            break
        else:
            path = ps.convert_to_Path(directories[i])
    return content

def default_contents(path):
    content = ps.file_list(path)
    content.append( ps.directory_list(path) )
    return content

def list_contents(path, options, admin, stop = None):
    contents = []
    if len(options) == 0:
        ui.print_admin_lines("Here are your file contents:", admin)
        contents.append(default_contents(path))
    else:
        nOptions = ui.remove_list_info(options)
        if options[0] == "-r":
            contents.append(recursive_contents(path, admin, nOptions))
        elif options[0] == "-f":
            ui.print_admin_lines("Here are all your files:", admin)
            contents.append(ps.file_list(path))
        elif options[0] == "-s":
            try:
                select = options[1]
            except Exception:
                if admin is True:
                    contents.append("None")
                else:
                    select = ui.prompt_info("Please enter a filename", True, admin)
            if admin is False:
                while "." not in select:
                    ui.print_admin_lines("Missing extension. Try again:", admin)
                    select = ui.prompt_info("Please enter a filename", True, admin)
                options.append(select)
            elif admin is True and "." not in select:
                contents.append("None")
            selectFiles = ps.select_filename(path, select)
            if len(selectFiles) == 0:
                ui.print_admin_lines(f"There are no files with {select} name.", admin)
            else:
                ui.print_admin_lines(f"Here are all your {select} files:", admin)
                contents.append(selectFiles)
        elif options[0] == "-e":
            try:
                ext = options[1]
            except Exception:
                if admin is True:
                    print("Invalid command.")
                    contents.append("None")
                else:
                    ext = ui.prompt_info("Please enter an extension", False, admin)
                    options.append(ext)
            extFiles = ps.select_extension(path, ext)
            if len(extFiles) == 0:
                ui.print_admin_lines(f"There are no files with {ext} extension.", admin)
            else:
                ui.print_admin_lines(f"Here are all your {ext} files", admin)
                contents.append( ps.select_extension(path, ext) )
        elif options[0] != "stop":
            print("Invalid L command.")
    
    if "None" in contents:
        print("Invalid command")
    else:
        contents = ps.remove_input_directory(path, contents)
        ui.print_info(contents)

    if admin is False and stop is None:
        cont = ui.continue_listing()
        if cont[0].lower() != "no":
            stop = False
        elif cont[0].lower() == "no":
            stop = True
        elif cont[0].lower() == "stop":
            print("Going back to main menu...")
            stop = True
        while stop is False:
            list_contents(path, cont, admin, stop)
            cont = ui.prompt_info("Please enter your next command", False)
            if cont[0].lower() == "stop":
                print("Going back to main menu...")
                stop = True
                
def publish_post_command(filePath):
    profile = Profile()
    profile.load_profile(str(filePath))
    publish = True

    if len(profile._posts) > 0:
        print()
        print(ui.index_all_posts(profile._posts))
        exPost = ui.yes_or_no("Would you like to publish an existing post")

        if exPost.lower() == "no":
            newPost = ui.yes_or_no("Would you like to make a new post")
            if newPost.lower() == "yes":
                ui.print_admin_lines("Alright then, let's make a new post!")

                ui.create_post(filePath)
            else:
                publish = False
    else:
        ui.print_admin_lines("You have no posts.")
        createNew = ui.yes_or_no("Would you like to create a post")
        if createNew.lower() == "yes":
            ui.create_post(filePath)
        else:
            publish = False 

    if publish is True:
        print(ui.index_all_posts(profile._posts))
        index = int(ui.prompt_info("Which post would you like to publish?", True))
        while index not in range(len(profile._posts)+1):
            index = int(ui.prompt_info("Invalid index, try again", True))
        postTP = profile.get_post_by_ID(index-1)
        post_entry = postTP.get_entry()

        if ui.confirm_publish(post_entry) is True:
            return postTP
    return None

