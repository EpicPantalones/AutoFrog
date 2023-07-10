from random import randint

KEYWORDS = ["help","new","edit","view","quit","settings","add","remove","set"]
ERROR_KEY = str(randint(100000000,999999999))

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
            case "new":
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

def read_settings():
    with open("settings.conf","r") as settings:
        args = settings.read().split()
        settings = []
        for i in range(0,len(args)):
            if i % 2 == 1:
                settings.append(args[i])
        print(settings)
        return settings
    