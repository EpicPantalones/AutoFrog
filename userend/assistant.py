KEYWORDS = ["help","new","edit","view","quit","settings","add","remove","set"]

def vocal_interpreter(args):
    alen = len(args)
    if alen == 0:
        return "--err--"
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
    with open("help.utf8","r") as config:
        outputs = {}
        line = config.readline().strip()
        while line[0] == '#':
            line = config.readline().strip()
        while line:
            key = line
            value = config.readline().strip()
            value = value.replace('//','\n')
            outputs[key] = value
            line = config.readline().strip()
            while line != '' and line[0] == '#':
                line = config.readline().strip()
    return outputs[cmd]