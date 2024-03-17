# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Luqi
# luqic2@uci.edu
# 69278864

import a2
import ui
import ps
from Profile import *

def main():
    print("Welcome!")
    ui.run_menu()
    userInput = ui.runStarter()

    admin = False
    path = None
    profile = None

    while userInput[0] != "q":
        if ps.check_if_directory_file(userInput[0], False) is False:
            userInput[0] = userInput[0].upper()
            if userInput[0] == "Q":
                continue
        path, profile, admin = a2.runCommandLine(userInput, path, profile, admin)
        userInput = ui.runStarter(admin)

if __name__ == "__main__":
    main()
