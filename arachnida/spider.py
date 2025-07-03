import sys
import re
import os
import urllib.request
import urllib.request
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
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


path_set = set();

def is_valid_extension(extension):
    match extension:
        case ".png":
            return True
        case ".jpg":
            return True
        case ".jpeg":
            return True
        case ".gif":
            return True
        case ".bmp":
            return True
        case _:
            return False


class MyHtmlParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.netloc = None
        self.current_path = None
        self.images = set()
        self.links = set()

    def handle_starttag(self, tag, attrs): # for </element>
        match tag:
            case "a":
                attr_dict = dict(attrs)
                link = attr_dict['href']
                if link != None and link.find(self.netloc) == -1:
                    self.links.add(link)
            case "img":
                pair = os.path.splitext(attrs[0][1])
                if is_valid_extension(pair[1]):
                    self.images.add(f"{attrs[0][1]}")

    def get_images(self):
        return self.images

    def get_links(self):
        return self.links

    def handle_startendtag(self, tag, attrs): # for <element/>
        if tag == "img":
            pair = os.path.splitext(attrs[0][1])
            if is_valid_extension(pair[1]):
                self.images.add(f"{attrs[0][1]}")


def read_and_feed_parser(parser, url):
    fp = urllib.request.urlopen(url) # Opens URL and sends request
    bytes_read = fp.read()
    fp.close()
    html = bytes_read.decode("utf8")
    parser.feed(html)

def init_html_parser(netloc):
    parser = MyHtmlParser()
    return parser

def clean_up_url(url):
    while url.find("../") != -1:
        url = url.replace("../", "")
        print("cleaning..", url)
    return url


def get_images_till_depth_lvl(depth, base_url, path):
    global opt_recursion
    url = f"{base_url}/{path}"
    url = clean_up_url(url)
    if depth <= 0: 
        print("arachnida finished!")
        return
    print(f"Level [{depth} | {url}]: ")
    parsed_url = urlparse(url)
    parser = MyHtmlParser()
    parser.netloc = parsed_url.netloc
    parser.current_path = parsed_url.path
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    fp.close()
    mystr = mybytes.decode("utf8")
    parser.feed(mystr)
    images = parser.get_images()
    links = parser.get_links()
    for img in images:
        img_url = f"{base_url}/{img}"
        img_name = os.path.basename(urlparse(img_url).path)
        try:
            img_url = clean_up_url(img_url)
            urllib.request.urlretrieve(img_url, f"./data/{img_name}")
            print(".", end='')
        except HTTPError as e:
            print(f"\nHTTP Error ({e.code}) for {img_url}: {e.reason}")
        except URLError as e:
            print(f"\nURL Error for {img_url}: {e.reason}")
        except Exception as e:
            print(f"\nUnexpected error for {img_url}: {e}")
    print("")
    if opt_recursion:
        for link in links:
            get_images_till_depth_lvl(depth - 1, base_url, link)


try: # PARSING & VALIDATING INPUT
    parse_arguments()
    validate_arguments(arg_path, arg_url)
    print_settings()

    # PARSING HTML/IMG
    parsed_url = urlparse(arg_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    get_images_till_depth_lvl(arg_depth_level, base_url, parsed_url.path)

except Exception as e:
    print("Error: ", e)




