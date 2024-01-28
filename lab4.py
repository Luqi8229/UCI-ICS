#lab4.py

# Starter code for lab 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Luqi Chen
# luqic@uci.edu
# 69278864

import random

"""
The default numbers here are generally good enough to create a rich tree. 
You are free to play with the numbers if you want. Lower numbers will simplify the results, 
larger numbers will take more time to render and create hundreds of acorns.
"""

TREE_DEPTH = 5
NODE_DEPTH = 5

def tree_builder(nodes:list, level:int, acorn:str) -> list:
    """
    Builds a tree using the random integers selected from the tree_depth and node_depth defaults
    """
    r = random.randrange(1, NODE_DEPTH)
    for i in range(r):
        if level < TREE_DEPTH:
            level_id  = f"L{level}-{i}"
            if level_id == acorn:
                level_id += "(acorn)"
            n = [level_id]
            nodes.append(tree_builder(n, level+1, acorn_placer()))

    return nodes

def acorn_placer() -> str:
    """
    Returns a random acorn location based on tree_depth and node_depth defaults
    """
    return f"L{random.randrange(1,TREE_DEPTH)}-{random.randrange(1,NODE_DEPTH)}"

def list_to_string1(branch):
    content = ""
    for level in branch:
        if type(level) is list:
            content += list_to_string(level)
        else:
            content += level + " -> "
    return content

def run1():
    # create a tree and start placing acorns
    tree = tree_builder([], 1, acorn_placer())

    # insert your solution code here
    acorn = 0
    acorn_branches = ""
    for branch in tree:
        content = list_to_string(branch)
        aCount = content.count("(acorn)")
        if aCount > 0:
            for a in range(aCount):
                index = content.rfind("(acorn)")
                content = content[:index]
                acorn_branches += content.replace("(acorn)", "", aCount) + "\n"
            acorn += aCount
    
    if acorn > 0:
        print(f"You have {acorn} acorns on your tree!")
        print("They are located on the following branches:")
        print(acorn_branches)
    else:
        print("You have no acorns")
    # end solution

# def list_to_string(branch, acornFound = 0):
#     content = ""
#     if branch == "":
#         return content
    
#     #find way around by Lx - y

#     if "acorn" in content:
#         return content
#     else:
#         for edge in branch:
#             if type(edge) is list:
#                 content += list_to_string(edge, acornFound)
#             else:
#                 content += edge + " "
#                 if "acorn" in edge:
#                     return content
#     return content
        
def acorn_finder(tree:list, node):
    content = ""
    finalContent = ""

    #find way around by Lx - y
    for t in tree:
        
        if t is None:
            return
        
        if isinstance(t, list): #if t is a list
            print("t=", t)
            branch = t[0]
            
            print("     BRANCH", branch)
            
            if branch[:2] > node[:2]:
                node = branch
                print("new node ", node)
            
            #delete contents inbetween nodes with no acorn
            print(node, branch)
            if (branch[:2] > node[:2]) and (branch[:-1] > node[:-1]):
                # if "acorn" not in content:
                #     fcon = content.find(node)
                #     content = content[:(fcon+4)] + " "
                fcon = content.find(node)
                content = content[:(fcon+4)] + " "
                
                print("NEW CONTENT ", content)

            #new recursive call
            content += branch + " " + acorn_finder(t, node)
            print("content ", content)

            if "acorn" in t:
                content = "New " + content + "elseacorn \n" 
                print("     CONTENTS AFTER ACORN", content)
            
        
        
        
        # if type(edge) is list:
        #     content += acorn_finder(edge)
        # else:
        #     content += edge + " "
        #     if "acorn" in edge:
        #         return content
    return content

def run():
    # create a tree and start placing acorns
    tree = tree_builder([], 1, acorn_placer())

    print()
    print(tree)
    print()


    # insert your solution code here
    acorn = 0
    acorn_branches = ""

    for bNum in range( len(tree) ):
        print("     NEW BRANCH")
        wholeBranch = tree[bNum]
        nNum = 0
        aFound = 0

        content = acorn_finder(wholeBranch, f'L{bNum}-{nNum}')
        print("run content ", content)
        
        while "acorn" in content:
            acorn += 1
            
    print("     ACORN_BRANCHES", acorn_branches)

    while "(acorn)" in acorn_branches:
        acorn_branches.replace("(acorn)", "")


    # aCount = content.count("(acorn)")
    # if aCount > 0:
    #     for a in range(aCount):
    #         index = content.rfind("(acorn)")
    #         content = content[:index]
    #         acorn_branches += content.replace("(acorn)", "", aCount) + "\n"
    #     acorn += aCount
    
    
    if acorn > 0:
        print(f"You have {acorn} acorns on your tree!")
        print("They are located on the following branches:")
        print(acorn_branches)
    else:
        print("You have no acorns")
    # end solution

if __name__ == "__main__":
    print("Welcome to PyAcornFinder! \n")

    run()
