
def notes_dialoge():
    print("Here are your notes: \n")

def print_notes(p):
    notes_dialoge()
    with open(p, "r") as f:
        for line in f:
            print(line)

def create_lines(p):
    notes_dialoge()
    id = 1
    lines = []
    with open(p, "r") as f:
        for line in f:
            lines.append(line)
            print(f'{id}: {line}')
            id += 1
    return lines

def remove(p, lines, remove_id):
    removed_note = ""
    with open(p, "w") as f:
        id = 1

        for line in lines:
            if id == int(remove_id):
                removed_note = line
            else:
                f.write(line)
            id += 1
    return removed_note

def path_exist(p):
    if p.exists():
        return True
    return False
