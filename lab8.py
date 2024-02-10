#lab8.py

# Starter code for lab 8 in ICS 32 Programming with Software Libraries in Python

# Please see the README in this repository for the requirements of this lab exercise

# ---------------------

# Write your Note class here
class Note():
    
    def __init__(self, name):
        self.name = name
    
    def read_notes(self):
        wordList = []
        with open (self.name, "r") as f:
            wordList = f.readlines()
        return wordList
    
    def save_note(self, note):
        with open(self.name, "a") as f:
            f.write(note + "\n")

    def remove_note(self, id):
        removed_note = ""
        print(type(id))
        lines = []
        with open(self.name, "r") as f:
            lines = f.readlines()
        with open(self.name, "w") as f:
            idTemp = 1
            for line in lines:
                print(line)
                if idTemp == int(id):
                    removed_note = line
                else:
                    f.write(line)
                idTemp += 1
        return removed_note

# ---------------------
from pathlib import Path

def print_notes(notes:list[str]):
    id = 0
    for n in notes:
        print(f"{id}: {n}")
        id+=1

def delete_note(note:Note):
    try:
        remove_id = input("Enter the number of the note you would like to remove: ")
        remove_note = note.remove_note(int(remove_id))
        print(f"The following note has been removed: \n\n {remove_note}")
    except FileNotFoundError:
        print("The PyNote.txt file no longer exists")
    except ValueError:
        print("The value you have entered is not a valid integer")

def run():
    p = Path("pyNote.txt")
    if not p.exists():
        p.touch()
    note = Note(p)
    
    print("Here are your notes: \n")
    print_notes(note.read_notes())

    user_input = input("Please enter a note (enter :d to delete a note or :q to exit):  ")

    if user_input == ":d":
        delete_note(note)
    elif user_input == ":q":
        return
    else:    
        note.save_note(user_input)
    run()


if __name__ == "__main__":
    print("Welcome to PyNote! \n")

    run()
