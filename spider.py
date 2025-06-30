import sys
import re
import os

FLAGS = "rlp"

# Flags & Options
opt_recursion = False;
opt_depth_level = False;
opt_path = False;

arg_url = "";
arg_path = "./data";
arg_depth_level = 5;

def is_flag(char):
    if char == 'r' or char == 'l' or char == 'p':
        return True;

def is_valid_url(string):
    pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
    return bool(re.match(pattern, string))

def is_valid_path(path):
    return os.path.exists(path)

def set_options(flag, arg):
    global arg_depth_level
    global arg_path
    global opt_recursion
    match flag:
        case 'r':
            opt_recursion = True
        case 'l':
            if arg != None:
                opt_depth_level = True
                arg_depth_level = int(arg)
        case 'p':
            opt_path = True
            arg_path = arg
        case _:
            print("Nothing to handle")

def parse_arguments():
    global arg_url
    i = 0
    for arg in sys.argv:
        if arg == 0:
            continue

        if arg[0] == '-' and is_flag(arg[1]):
                set_options(arg[1], sys.argv[i + 1])
        else:
            if is_valid_url(arg):
                arg_url = arg
        i += 1

def validate_arguments(arg_path, arg_url):
    if arg_path != "./data" and not is_valid_path(arg_path):
        raise ValueError("Invalid path")
    elif not os.path.exists(arg_path):
        os.makedirs(arg_path)

    if not is_valid_url(arg_url):
        raise ValueError("Invalid or missing URL")

def print_settings():
    global opt_recursion
    global opt_path
    global opt_depth_level
    global arg_path
    global arg_url
    global arg_depth_level

    if opt_recursion:
        print("Recursive: ", opt_recursion)
        print("Depth level: ", arg_depth_level)
    print("Path: ", arg_path)
    print("URL: ", arg_url)


# Parse and validate arguments
try:
    parse_arguments()
    validate_arguments(arg_path, arg_url)
    print_settings()
except Exception as e:
    print("Error: ", e)


