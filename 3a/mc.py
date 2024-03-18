
import ps, ui
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
        print(contents)
        
        ans = ui.yes_or_no("Would you like to list something else")
        if ans == "no":
            command = 'q'
        else:
            command = ui.prompt_info("What would you like to list next?", command=True, option="list")
    ui.aline("Going back to main...")

################################ DSU #########################################

def open_profile(filePath, admin = False):
    prof = Profile
    try:
        prof.load(str(filePath))
        ui.aline(f'Opened Profile: {prof.username}')
    except:
        ui.aline("There is not a profile associated with this DSU file", admin)
        newAns = ui.yes_or_no("Would you like to enter another directory?", admin)
        if newAns == "yes":
            filePath = ui.prompt_directory(admin, True)
            prof = open_profile(filePath, admin)
        else:
            createAns = ui.yes_or_no("Would you like to create a new Profile?", admin)
            if createAns == "yes":
                prof = create_profile(admin)
            else:
                prof = None

    return prof

def create_profile(admin=False):
    dir = ui.prompt_folder(admin, True)
    fileName = ui.propmt_info("Give a name for the file", admin)
    filePath = ps.create_file(dir, fileName, dsu=True)

    user, pwd, bio = ui.profile_info(admin)
    profile = Profile(filePath = str(filePath), username = user, password = pwd, bio = bio)
    profile.save_profile(str(filePath))
    
    ui.aline("Profile created", admin)
    return profile

def edit_profile(prof, admin=False):
    pass

def print_profile(prof, admin=False):
    pass

def dsu_command(admin = False):
    profile = Profile
    existing = ui.yes_or_no("Do you have an existing DSU file", admin)

    if existing == "yes":
        ui.aline("That's great!", admin)
        dsufile = ui.prompt_directory(admin, True)

        ui.aline("Opening DSU file...")
        profile = open_profile(dsufile, admin)
    else:
        ui.aline("Alright then. Let's create a DSU file!", admin)
        profile = create_profile(admin)

    if profile != None:
        manage = ui.prompt_info("Would you like to edit or print your DSU file?", command = True, option='edpr').lower()
        if manage == "edit":
            edit_profile(profile, admin)
        elif manage == "print":
            print_profile(profile, admin)
    else:
        ui.aline("Going back to main...")
    

def publish_command():
    pass

