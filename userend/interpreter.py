from random import randint

KEYWORDS = ["help","new","edit","view","quit","settings","add","remove","set"]
ERROR_KEY = "vAkEoAYB0pd3nOW8XSOHzxRU87YmEB4KUGoJI1eLnJ7Tk58RPV"

def interpret(args):
    alen = len(args)
    if alen == 0:
        return ERROR_KEY
    
    elif args[0] not in KEYWORDS:
        return f"{args[0]} is not a recognized command. type \"help\" for a list of commands."
    else:
        match args[0]:
            case "help":
                if alen == 1:
                    return f"the following commands are available: {KEYWORDS}"
                else:
                    if args[1] not in KEYWORDS:
                        return f"{args[1]} is not a recognized command. type help for a list of commands."
                    return help_with(args[1])
            case "add":
                return "added"
            case "edit":
                return "edited"
            case "view":
                return "viewed"
            case "quit":
                return "quit"
            case "settings":
                return "settings-ed"

def help_with(cmd):
    with open("manual.utf8","r") as help_conf:
        outputs = {}
        line = help_conf.readline().strip()
        while line[0] == '#':
            line = help_conf.readline().strip()
        while line:
            key = line
            value = help_conf.readline().strip()
            value = value.replace('//','\n')
            outputs[key] = value
            line = help_conf.readline().strip()
            while line != '' and line[0] == '#':
                line = help_conf.readline().strip()
    try:
        message = outputs[cmd]
    except KeyError:
        message = "There was an error reading the help menu."
    return message