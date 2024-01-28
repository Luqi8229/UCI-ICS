
# Tues Jan 9

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


#Thurs Jan 18

def factorial(n):
    if n == 0:
        return 0
    if n == 1:  #1 Base Case
        return 1
    else:       #2 Recursive Case
        return n * factorial (n-1)

def run_factorials(): # main
    try:
        value = factorial(5)
    except TypeError:
        print()
    else:
        print(value)


def generate_fibonacci(n):
    fib_nums = [0,1] #0, 1, 1, 2, 3, 5, 8

    for i in range(2, n):
        next = fib_nums[i-1] + fib_nums[i-2]
        fib_nums.append[next]
    return fib_nums

def generate_fibonacci_recursive(n):
    #base case
    if n == 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0,1]
    else: #recursive case
        fib_seq = generate_fibonacci_recursive(n-1)
        fib_seq.append[fib_seq[-1] + fib_seq[-2]]
        return fib_seq

def test_fibonacci(): #main
    print(generate_fibonacci(10))
    print(generate_fibonacci_recursive(10))

# Tues Jan 23

# from math_module import sum

# OR
# import math_module


