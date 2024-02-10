
def reverseString(line):
    if len(line) == 0:
        return line
    firstCh = line[:1]
    line = line[1:]
    newLine = reverseString(line)
    line = newLine + firstCh
    return line

def encryptFile(ogFile, newfile):
    encryptString = ""
    with open(ogFile, "r") as f:
        for line in f.readlines():
            # line = line[:-2]
            encryptString = reverseString(line) + encryptString
    with open (newfile, "w")  as f:
        f.write(encryptString)
    printFileContents(ogFile)
    printFileContents(newfile)

def printFileContents(file):
    with open(file, "r") as f:
        print(f.read())

def main():
    files = input().split()
    encryptFile(files[0], files[1])
    

if __name__ == "__main__":
    main()
