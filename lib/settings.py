import os
import re
import sys
import platform


VERSION = "0.0.1"
HOME = "{}/.whatbreach_home".format(os.path.expanduser("~"))
DOWNLOADS_PATH = "{}/downloads".format(HOME)
HIBP_URL = "https://haveibeenpwned.com/api/v2/breachedaccount/{}"
HIBP_PASTE_URL = "https://haveibeenpwned.com/api/v2/pasteaccount/{}"
DEHASHED_URL = "https://www.dehashed.com/search?query={}"
DATABASES_URL = "https://databases.today/search-nojs.php?for={}"
USER_AGENT = "Breach-Reporter/{} (Language={}; Platform={})".format(
    VERSION, sys.version.split(" ")[0], platform.platform().split("-")[0]
)
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Connection": "close",
    "Made-With-Love": "By Eku"
}
TEN_MINUTE_EMAIL_EXTENSION_LIST = "{}/etc/ten_minute_emails.lst".format(os.getcwd())
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
        print("\033[99;4mBreached Site:\033[0m\t{}|{}\033[99;4mDatabase Link:\033[0m".format(" " * 5, " "))
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
