import os
import re
import sys
import platform


# version number
VERSION = "0.0.2"

BANNER = """{color_scheme_1}
{tabbed_indent}                                                    _____ 
{tabbed_indent}   _ _ _ _       _   _____                 _       |___  |
{tabbed_indent}  | | | | |_ ___| |_| __  |___ ___ ___ ___| |_       |  _|
{tabbed_indent}  | | | |   | .'|  _| __ -|  _| -_| .'|  _|   |      |_|  
{tabbed_indent}  |_____|_|_|__,|_| |_____|_| |___|__,|___|_|_|[][][]|_|{color_scheme_end}
{tabbed_indent}{color_scheme_2}Find emails and their associated leaked databases.. v{version_number}{color_scheme_end}

""".format(
    color_scheme_end="\033[0m",
    color_scheme_1="\033[34m",
    color_scheme_2="\033[4;33m",
    version_number=VERSION,
    tabbed_indent="\t"

)

# home path
HOME = "{}/.whatbreach_home".format(os.path.expanduser("~"))

# where we gonna download this shit too?
DOWNLOADS_PATH = "{}/downloads".format(HOME)

# have you been pwned?!
HIBP_URL = "https://haveibeenpwned.com/api/v2/breachedaccount/{}"

# paste URL
HIBP_PASTE_URL = "https://haveibeenpwned.com/api/v2/pasteaccount/{}"

# dehashed search query
DEHASHED_URL = "https://www.dehashed.com/search?query={}"

# databases.tody URL
DATABASES_URL = "https://databases.today/search-nojs.php?for={}"

# our user agent because who doesn't love a good user agent?
USER_AGENT = "Breach-Reporter/{} (Language={}; Platform={})".format(
    VERSION, sys.version.split(" ")[0], platform.platform().split("-")[0]
)

# default request headers
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Connection": "close",
    "Made-With-Love": "By Eku"
}

# a giant ass list of ten minute email extensions
TEN_MINUTE_EMAIL_EXTENSION_LIST = "{}/etc/ten_minute_emails.lst".format(os.getcwd())

# check if the results actually exist or not
VERIFICATION_REGEX = re.compile("sensitive.data.available.but.hidden", re.I)


def display_found_databases(data, overflow=23, is_downloaded=False):
    """
    display the found data in a pretty table
    """
    if not is_downloaded:
        tmp = []
        for item in data.keys():
            if type(data[item]) == tuple:
                tmp.append(data[item][-1])
            else:
                if len(data[item]) == 8:
                    data[item] = "https://pastebin.com/{}".format(data[item])
                tmp.append(data[item])
        sep = "-" * len(max(tmp, key=len)) + "-" * overflow
        print(sep)
        output_template = "{0:20} | {1:30}"
        print("\033[99;4mBreach/Paste:\033[0m\t{}|{}\033[99;4mDatabase/Paste Link:\033[0m".format(" " * 5, " "))
        for i, key in enumerate(data.keys(), start=1):
            key = str(key)
            if type(data[key]) == tuple:
                result, search_url = data[key][0], data[key][-1]
                if result:
                    print(output_template.format(key, data[key][-1]))
            else:
                print(output_template.format(key, str(data[key])))
        print(sep)
    else:
        sep = "-" * 50
        print(sep)
        for i, path in enumerate(data, start=1):
            print("#{} ~~> {}".format(i, path))
        print(sep)


def check_ten_minute_email(email, path):
    """
    check if the provided email is a ten minute email or not
    """
    with open(path) as data:
        exts = [e.strip() for e in data.readlines()]
        current_ext = email.split("@")[-1]
        if current_ext in exts:
            return True
    return False
