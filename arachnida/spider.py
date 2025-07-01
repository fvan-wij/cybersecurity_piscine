import sys
import re
import os
import urllib.request
from urllib.parse import urlparse
from html.parser import HTMLParser
import webbrowser

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

# def get_href(tuple):
#     [item for item in a if item[0] == 1]

class MyHtmlParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.url = None

    def handle_starttag(self, tag, attrs): # for <a href="" ></a>
        match tag:
            case "a":
                # print("Encountered a link: ", tag)
                attr_dict = dict(attrs)
                link = attr_dict['href']
                if link != None and link.find(url.netloc) == -1:
                    print(link)
                # if link != None and link.find(url.netloc) == len(url.netloc):
                #     print(link)

                # print(attr_dict['href'])
                # print(attrs)
                # for attr in attrs:
                    # if attr.find(url.netloc):
                    #     print(attr)
                # if attrs.find(url.netloc):
                    # print("Attributes: ", attrs)
            # case "img":
            #     print("Encountered an image: ", tag)
            #     print("Attributes: ", attrs)

    # def handle_startendtag(self, tag, attrs): # for <img src=""/>
    #     match tag:
    #         case "img":
    #             print("Encountered an image: ", tag)
    #             print("Attributes: ", attrs)

try: # PARSING & VALIDATING INPUT
    parse_arguments()
    validate_arguments(arg_path, arg_url)
    url = urlparse(arg_url)
    print(url)
    print_settings()

    # PARSING HTML IMG
    fp = urllib.request.urlopen(arg_url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    parser = MyHtmlParser()
    parser.url = url
    parser.feed(mystr)
    


except Exception as e:
    print("Error: ", e)




