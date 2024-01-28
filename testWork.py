
def ReverseAndRemove(s):

    if s == "":
        return s
    
    c = s[0]
    newS = s[1:]

    newS = ReverseAndRemove(newS)
    if c == " ":
        return newS
    else:
        
        s = newS + c
    return s

print( ReverseAndRemove("Hello World") )
