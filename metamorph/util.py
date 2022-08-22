import difflib
from termcolor import colored

def get_edits_string(old, new):
    """
    Colorize the differences between two strings.
    """
    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    for code in codes:
        if code[0] == "equal":
            result += old[code[1]:code[2]]
        elif code[0] == "insert":
            result += colored(new[code[3]:code[4]],'green')
        elif code[0] == "replace":
            result += colored(new[code[3]:code[4]],'green')
    return result