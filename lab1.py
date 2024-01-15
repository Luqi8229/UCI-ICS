# lab1.py

# Starter code for lab 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# NAME
# EMAIL
# STUDENT ID

def calculate(n1, n2, op):
    result = 0
    if op == "+":
        result = n1 + n2
    elif op == "-":
        result = n1 - n2
    elif op == "x":
        result = n1 * n2
    elif op == "/":
        result = n1 / n2
    else:
        return "operator not supported"
    print(f'The result of your calculation is: {result}')

def runMenu():
    num1 = int(input('Enter your first operand:\n'))
    num2 = int(input('Enter your second operand:\n'))
    operator = input('Enter your desired operator(+, -, x, or /):\n')
    calculate(num1, num2, operator)

def main():
    runMenu()

main()
