
import mc, ui

def runCommandLine(info, filePath, profile, admin):
    command = info[0].lower()

    if ui.command_exist(command, 'command', admin) is False:
        return filePath, profile, admin
    
    nl = ui.remove_info(info)

    if command == "admin":
        admin = True
        return filePath, profile, admin
    elif command == "menu":
        ui.run_menu()
        return filePath, profile, admin
    elif command == "list":
        mc.list_command(admin)
    elif command == "dsu":
        mc.dsu_command(admin)
    elif command == "publish":
        mc.publish_command(admin)

    return filePath, profile, admin 
    
def main():
    print("Welcome!")
    ui.run_menu()

    admin = False
    path = None
    profile = None
    userInput = ui.prompt_info("What would you like to do?", admin, False)

    while userInput[0].lower() != "q":
        path, profile, admin = runCommandLine(userInput, path, profile, admin)
        userInput = ui.prompt_info("What would you like to do?", admin, False)

if __name__ == "__main__":
    main()
