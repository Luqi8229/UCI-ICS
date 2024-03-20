
import ps, ui, ds_client
from Profile import *

def recursive_contents(dirPath, admin=False):
    content = []
    path = ps.path(dirPath)
    
    directories = ps.directory_list(path)
    directories.insert(0, path)

    ans = ui.yes_or_no("Would you like to filter for a specfic file, extension, or just files", admin)
    if ans == "yes":
        ui.run_R_menu()
        option = ui.prompt_info("Which of the following do you want try?", command=True, option='LR').lower()

        infoFunc = {'files': ui.prompt_files, 'name':ui.prompt_name, 'ext':ui.prompt_ext}
        repeatFunc = {'files': ps.file_list, 'name':ui.select_name, 'ext':ps.select_extension}
        
        searchInfo = infoFunc[option](admin)
        
        for dir in directories:
            con = repeatFunc[option](ps.path(dir), searchInfo)
            if con != []:
                content.append(con)
    else:
        searchInfo = 'all'
        option = 'all'
        content.append( ps.file_list(path) ) 
        content.append( ps.directory_list(path) )

    strContent = ui.list_to_string(content)
    
    return strContent, option, searchInfo

def list_command(admin = False):
    contents = ''
    ui.run_L_menu()
    command = ui.prompt_info("What are you interested in seeing?", command=True, option="list").lower()
    fPath = ui.prompt_directory(admin)
    filePath = ps.path(fPath)
    while command != "q":
        option = ''
        searchInfo = ''

        while command == "menu":
            ui.run_L_menu()
            command = ui.prompt_info("What would you like to list next?", command=True, option="list")

        if ui.command_exist( command, "list") is True:
            option = command
            if command == "all":
                contents, option, searchInfo = recursive_contents(filePath, admin)
            elif command == "files":
                contents = ui.list_to_string(ps.file_list(filePath))
            elif command == "name":
                searchInfo = ui.prompt_name(admin)
                contents = ui.list_to_string(ui.select_name(filePath, searchInfo))
            elif command == "ext":
                searchInfo = ui.prompt_ext(admin)
                contents = ui.list_to_string(ps.select_extension(filePath, searchInfo))
        else:
            ui.aline(f"{command} is not an option.")

        contents = ui.add_heading(option, contents, searchInfo)
        print(contents) #prints the contents
        
        ans = ui.yes_or_no("Would you like to list something else")
        if ans == "no":
            command = 'q'
        else:
            command = ui.prompt_info("What would you like to list next?", command=True, option="list")
    ui.aline("Going back to main...")

################################ DSU #########################################

def edit_profile(prof, admin=False):
    ui.run_E_menu()
    edit = ui.prompt_info("What would you like to edit?", admin, str = False, command = True, option = "ep")
    while edit[0] != "stop":
        if edit[0] == "all":
            edit = ['username', 'password', 'bio', 'post']
        for elm in edit:
            if elm == "post":
                ui.edit_posts(prof, admin)
            else:
                change = ui.prompt_info(f"Enter your new {elm}", admin)
                if elm == "username":
                    prof.username = change
                elif elm == "password":
                    prof.password = change
                elif elm == "bio":
                    prof.bio = change
        prof.save_profile( prof.get_filepath() )

        again = ui.yes_or_no("Would you like to edit something else", admin)
        if again == "yes":
            edit = list(ui.prompt_info("What would you like to edit?", admin, str = False, command = True, option = "ep"))
        else:
            edit = ["stop"]

def print_profile(prof, admin=False):
    ui.run_P_menu()
    prin = ui.prompt_info("What would you like to print?", admin, str = False, command = True, option = "ep")
    while prin[0] != "stop":
        if prin[0] == "all":
            prin = ['username', 'password', 'bio', 'post']
        profDict = {"username": prof.username, "password":prof.password, "bio":prof.bio, "post":ui.index_posts(prof.get_posts())}
        content = ''
        for elm in prin:
            content += ui.format_print(elm.capitalize(), profDict[elm])
        print(content)

        again = ui.yes_or_no("Would you like to print something else", admin)
        if again == "yes":
            prin = ui.prompt_info("What would you like to print?", admin, str = False, command = True, option = "ep")
        else:
            prin = ["stop"]

def dsu_command(admin = False):
    profile = ui.choose_profile(admin)
    if profile != None:
        manage = ui.prompt_info("Would you like to edit or print your DSU file?", admin, command = True, option='edpr').lower()
        if manage == "edit":
            edit_profile(profile, admin)
        elif manage == "print":
            print_profile(profile, admin)
    ui.aline("Going back to main...")

############################# Publish ##############################3

def publish_command(admin):
    #address 168.235.86.101
    profile = ui.choose_profile(admin)
    if ds_client.send(profile, admin) is True:
        ui.aline("Closing connection...")
    ui.aline("Going back to main...")
    
