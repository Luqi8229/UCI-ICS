
import mc, ui

def runCommandLine(info:list, admin=False):
    command = info.lower()

    while command == "menu":
        ui.run_M_menu()
        return admin
    
    if command.lower() == "admin":
        admin = True
        return admin
    
    if ui.command_exist(command, "main") is True:
        if command == "list":
            mc.list_command(admin)
        elif command == "dsu":
            mc.dsu_command(admin)
        elif command == "publish":
            mc.publish_command(admin)
    
def main():
    print("Welcome!")
    ui.run_M_menu()
    userInput = ui.prompt_info("What would you like to do", command = True, option = "main")
    admin = False

    while userInput[0].lower() != "q":
        admin = runCommandLine(userInput, admin)
        userInput = ui.prompt_info("What would you like to do next?", command = True, option = "main")

if __name__ == "__main__":
    main()
