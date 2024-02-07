"""
This program prints the value of my_var at different levels of scope
"""

def print_scope_lab7(d:dict):
    """
    Iterates through a dictionary of variables from a given scope and
    prints any item that contains the variable name "my_var"
    """
    for item in d.items():
        if "my_var" in item[0]:
            print(item)

my_var = 'global'

def my_func_1():
    my_var = 'enclosed'

    def my_func_3():
        nonlocal my_var
        my_var = "local"
        print_scope_lab7(locals().copy())

    my_func_3()
    print_scope_lab7(locals().copy())

def my_func_2():
    global my_var
    my_var = 'enclosed'

    def my_func_3():
        my_var = 'local'
        print_scope_lab7(locals().copy())

    my_func_3()
    print_scope_lab7(locals().copy())


if __name__ == "__main__":
    my_func_1()
    my_func_2()
    print_scope_lab7(globals().copy())
