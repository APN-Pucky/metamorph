import difflib
from termcolor import colored

def get_edits_string(old:str, new:str, color:str='green', on_color :str= 'on_red'):
    """
    Colorize the differences between two strings.
    """
    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    reds = []
    if on_color:
        for code in codes:
            if code[0] == "replace":
                reds += list(range(code[1],code[2]))
            elif code[0] == "delete":
                reds += list(range(code[1],code[2]))
    
    li = 0
    for code in codes:
        if code[0] == "equal":
            for i in range(code[3],code[4]):
                result += colored(new[i],color=None,on_color=on_color if i in reds else None)
            li=code[4]
        elif code[0] == "insert":
            for i in range(code[3],code[4]):
                result += colored(new[i],color=color,on_color=on_color if i in reds else None)
            li=code[4]
        elif code[0] == "replace":
            for i in range(code[3],code[4]):
                result += colored(new[i],color=color,on_color=on_color if i in reds else None)
            li=code[4]
    
    #mr = max(reds) if len(reds) > 0 else 0
    ##print(mr, li, reds)
    #if li < mr:
    #    result += colored(" "*(mr-li),color=None,on_color=on_color)

    return result