"""
This program enables a user to input short one line notes and have them stored in a file called pynote.txt

"""

from pathlib import Path
from lab6_module import *

def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

def save_note(p, note: str):
    # create path obj to notes storage file
    # p = Path(NOTES_PATH) / NOTES_FILE

    # check if storage file exists, if not create it.
    if path_exist(p) is False:
        p.touch(exist_ok=True)
    
    # open and write user note to file
    with open(p, "a") as f:
        f.write(note + '\n')

def read_notes(p):
    # check if storage file exists, if not return.
    if path_exist(p) is False:
        return
    print_notes(p)

def remove_note(p) -> str:

    # check if storage file exists, if not return.
    if path_exist(p) is False:
        raise FileNotFoundError("Notes file has been deleted unexpectedly")
    
    lines = create_lines(p)

    remove_id = input("Enter the number of the note you would like to remove: ")
    if not is_int(remove_id):
        print ("Not a valid number, cancelling operation.")
        return

    removed_note = remove(p, lines, remove_id)
    return removed_note

def run(path):
    note = input("Please enter a note (enter :d to delete a note or :q to exit):  ")
    if note == ":d":
        try:
            note = remove_note(path)
            print(note)
            if note is None:
                assert False, "FileNotFoundError should have been raised"
            
            print(f"The following note has been removed: \n\n {note}")
        except FileNotFoundError:
            print("The PyNote.txt file no longer exists")
    elif note == ":q":
        return
    else:    
        save_note(path, note)
    run(path)


if __name__ == "__main__":
    assert is_int(5) == True
    assert is_int("five") == False

    path = Path(".pynote.txt")
    print("Welcome to PyNote! \n")
    read_notes(path)

    run(path)
    