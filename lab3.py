#lab3.py

# Starter code for lab 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Luqi Chen
# luqic2@uci.edu
# 69278864

def read_file():
    print()
    with open('pynote.txt', "r") as fil:
        for line in fil.readlines():
            print(line)

def run_notes():
    
    with open("pynote.txt", "a") as myfile:
        read_file()
        new_note = input("Please enter a new note (enter q to exit):")
        while new_note != "q":
            myfile.write(new_note + "\n")
            new_note = input("Please enter a new note (enter q to exit):")

def main():
    print("Welcome to PyNote!")
    print("Here are your notes:")
    run_notes()

if __name__ == "__main__":
    main()
