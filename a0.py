
def print_diagonal_blocks(n):
    print("+-+")
    for i in range(n):
        print(i * "  " + "| |")
        if n > i + 1:
            print(i * "  " + "+-+-+")
    print(i * "  " + "+-+")

def main():
    sizeN = input()
    print_diagonal_blocks(int(sizeN))

def print_triangles(n):
    for i in range(n):
        for j in range(n):
            print("*", end='')
        print()

    for i in range(n+1):
        for j in range(i):
            print("*", end ='')
        print()

    print()
    for i in range(n, 0, -1):
        for j in range(i):
            print("*", end ='')
        print()

    print()
    for i in range(n):
        for j in range(i): # i dedicates num of spaces
            print(" ", end='')
        for k in range(n - i):
            print("*", end='')
        print()

        #OR

    print()
    for i in range(n):
        for j in range(n):
            if i > j:
                print(' ', end='')
            else:
                print('*', end='')
        print()


if __name__ == "__main__":
    print_triangles(4)
