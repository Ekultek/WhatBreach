import os
import re
import sys
import json
import string
import random
import platform

import lib.formatter


# version number
VERSION = "0.1.0"

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

# where we're going to place the JSON data
JSON_DATA_DUMPS = "{}/json_dumps".format(HOME)

# API token paths
TOKENS_PATH = "{}/tokens".format(HOME)

# have you been pwned?!
HIBP_URL = "https://haveibeenpwned.com/api/v2/breachedaccount/{}"

# paste URL
HIBP_PASTE_URL = "https://haveibeenpwned.com/api/v2/pasteaccount/{}"

# dehashed search query
DEHASHED_URL = "https://www.dehashed.com/search?query={}"

# databases.tody URL
DATABASES_URL = "https://databases.today/search-nojs.php?for={}"

# hunter.io API url
HUNTER_IO_URL = "https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"

# api link to verify email status
HUNTER_IO_VERIFY_URL = "https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"

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

RANDOM_USER_AGENT_PATH = "{}/etc/user_agents.txt".format(os.getcwd())


def random_string(length=10):
    """
    random strings so files dont get fucked up
    """
    acceptable = string.ascii_letters
    _string = []
    for _ in range(length):
        _string.append(random.choice(acceptable))
    return "".join(_string)


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


def smoosh_multi(single, filename):
    """
    add a string and file into a single list
    """
    retval = [single]
    try:
        open(filename).close()
    except IOError:
        lib.formatter.error(
            "the file failed to open, does it exist?"
        )
        exit(1)
    with open(filename) as data:
        for item in data.readlines():
            retval.append(item.strip())
    return retval


def grab_random_user_agent(path):
    """
    grab a random user agent
    """
    with open(path) as agents:
        return random.choice(agents.readlines()).strip()


def grab_api_tokens():
    """
    grab API tokens from the stored data, this will be useful for when we add more APIs
    """
    filenames = (
        "{}/hunter.io",
    )
    if not os.path.exists(TOKENS_PATH):
        os.makedirs(TOKENS_PATH)
        for f in filenames:
            with open(f.format(TOKENS_PATH), 'a+') as token:
                item = raw_input("You have no provided a token for {}, enter token: ".format(f.split("/")[-1]))
                token.write(item.strip())
    else:
        tokens = {}
        for f in filenames:
            with open(f.format(TOKENS_PATH)) as data:
                token_identifier = f.split("/")[-1]
                lib.formatter.info("grabbing {} API token".format(token_identifier))
                tokens[token_identifier] = data.read().strip()
        return tokens


def write_processed_to_file(data, domain, file_path):
    """
    write the processed data to a file
    """
    with open(file_path, 'a+') as dump:
        json.dump(data[domain], dump, sort_keys=True, indent=4)
    return file_path


def process_discovered(numbers, urls, emails, pattern, domain, do_write=True):
    """
    make a pretty little output of discovered API data
    """
    lib.formatter.info("information discovered associated with {}".format(domain))
    lib.formatter.info("discovered possible pattern to emails: {}".format(pattern))
    if len(numbers) != 0:
        lib.formatter.info("discovered possible associated phone numbers:")
        for number in numbers:
            if number is not None:
                print("   -> {}".format(str(number).replace(" ", "-")))
    else:
        lib.formatter.warn("did not discover any associated phone numbers")
    if len(emails) != 0:
        lib.formatter.info("discovered related emails:")
        for email in emails:
            print("  -> {}".format(str(email)))
    else:
        lib.formatter.warn("did not discover any more associated email addresses")
    if len(urls) != 0:
        lib.formatter.info("discovered (possibly related) external URL's:")
        for url in urls:
            print("  -> {}".format(str(url)))
    else:
        lib.formatter.warn("did not discover any possibly related links")
    if do_write:
        filename = "{}_{}.json".format(random_string(), str(domain))
        file_path = "{}/{}".format(JSON_DATA_DUMPS, filename)
        if not os.path.exists(JSON_DATA_DUMPS):
            os.makedirs(JSON_DATA_DUMPS)
        lib.formatter.info("dumping all information into json file for further processing")
        write_data = {
            domain: {
                "recognition_pattern": pattern if pattern is not None else None,
                "discovered_emails": list(emails),
                "external_urls": list(urls) if len(urls) != 0 else None,
                "discovered_numbers": list(numbers) if len(numbers) != 0 else None
            }
        }
        file_path = write_processed_to_file(write_data, domain, file_path)
        lib.formatter.info("information written to: {}".format(file_path))
        return file_path
    else:
        return None
