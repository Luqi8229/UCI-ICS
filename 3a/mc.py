
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
    command = ui.prompt_info("What are you interested in seeing?", command=True, option="list")
    fPath = ui.prompt_info("Please enter a directory", admin)
    filePath = ps.path(fPath)
    while command != "q":
        option = ''
        searchInfo = ''

        while command == "menu":
            ui.run_L_menu()
            command = ui.prompt_info("What would you like to list next?", command=True, option="list")

        if ui.command_exist( command, "list", admin ) is True:
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

def dsu_command(admin = False):
    profile = Profile

def publish_command():
    pass

