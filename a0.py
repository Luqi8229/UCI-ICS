
def print_diagonal_blocks(n):
    print("+-+")
    for i in range(n):
        print(i * "  " + "| |")
        if n > i + 1:
            print(i * "  " + "+-+-+")
        else:
            print(i * "  " + "+-+")

def main():
    sizeN = input()
    print_diagonal_blocks(int(sizeN))

main()
