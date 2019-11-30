import os
import re
import sys
import json
import string
import random
import platform

import lib.formatter

from hookers.pastebin_hook import PastebinRawHook


# version number
VERSION = "0.2.7"

# sexy banner
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

# pastebin downloads
PASTEBIN_DOWNLOADS = "{}/pastebin".format(DOWNLOADS_PATH)

# where we're going to place the JSON data
JSON_DATA_DUMPS = "{}/json_dumps".format(DOWNLOADS_PATH)

# API token paths
TOKENS_PATH = "{}/tokens".format(HOME)

# have you been pwned?!
HIBP_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"

# paste URL
HIBP_PASTE_URL = "https://haveibeenpwned.com/api/v3/pasteaccount/{}"

# dehashed search query
DEHASHED_URL = "https://www.dehashed.com/search?query={}"

# databases.tody URL
DATABASES_URL = "https://databases.today/search-nojs.php?for={}"

# hunter.io API url
HUNTER_IO_URL = "https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"

# api link to verify email status
HUNTER_IO_VERIFY_URL = "https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"

# snusbase
SNUSBASE_URL_DICT = {
    "login": "https://snusbase.com/login",
    "search": "https://snusbase.com/search"
}

# link to welinkinfo.com
WELEAKINFO_URL = "https://api.weleakinfo.com/v3/public/email/{}"

# get the reputation of the email address
EMAILREP_IO_LINK = "https://emailrep.io/{}"

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

# where the user agents sit
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


def display_found_databases(data, overflow=23, is_downloaded=False, download_pastes=False):
    """
    display the found data in a pretty table
    """
    pastebins = []
    if not is_downloaded:
        tmp = []
        for item in data.keys():
            if type(data[item]) == tuple:
                tmp.append(data[item][-1])
            else:
                if len(data[item]) == 8:
                    pastebins.append("https://pastebin.com/raw/{}".format(data[item]))
                    data[item] = "https://pastebin.com/{}".format(data[item])
                tmp.append(data[item])
        sep = "-" * len(max(tmp, key=len)) + "-" * overflow
        print(sep)
        output_template = "{0:25} | {1:35}"
        print("\033[99;4mBreach/Paste:\033[0m\t{}|{}\033[99;4mDatabase/Paste Link:\033[0m".format(" " * 10, " "))
        for i, key in enumerate(data.keys(), start=1):
            original_key = str(key)
            do_show_key = False
            key = str(key)
            if type(data[key]) == tuple:
                result, search_url = data[key][0], data[key][-1]
                if len(key) >= 15:
                    display_key = key[0:15] + "..."
                    do_show_key = True
                if result:
                    print(output_template.format(key, data[key][-1]))
                else:
                    if do_show_key:
                        print(output_template.format(display_key, "N/A (breach name: {})".format(original_key)))
                    else:
                        print(output_template.format(key, "N/A"))
            else:
                print(output_template.format(key, str(data[key])))
        print(sep)
    else:
        sep = "-" * 50
        print(sep)
        for i, path in enumerate(data, start=1):
            print("#{} ~~> {}".format(i, path))
        print(sep)
    if download_pastes:
        download_raw_pastes(pastebins)


def download_raw_pastes(pastebins):
    """
    download the pastes
    """
    pastebin_hook = PastebinRawHook
    if len(pastebins) != 0:
        lib.formatter.info("downloading a total of {} paste(s)".format(len(pastebins)))
        for paste in pastebins:
            path = pastebin_hook(paste).hooker()
            if path is not None:
                lib.formatter.info("paste downloaded to {}".format(path))
            else:
                lib.formatter.error("unable to download provided paste from link: {}".format(paste))
    else:
        lib.formatter.warn("no pastes discovered for associated email")


def check_ten_minute_email(email, path):
    """
    check if the provided email is a ten minute email or not
    """
    with open(path) as data:
        search_dump = data.read()
        current_ext = email.split("@")[-1]
        searcher = re.compile(current_ext, re.I)
        for item in search_dump.split("\n"):
            if searcher.match(item) is not None:
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
    tokens = {}
    filenames = (
        "{}/hunter.io", "{}/weleakinfo.com", "{}/haveibeenpwned.com", "{}/snusbase.com"
    )
    if not os.path.exists(TOKENS_PATH):
        os.makedirs(TOKENS_PATH)
    for f in filenames:
        if not os.path.exists(f.format(TOKENS_PATH)):
            with open(f.format(TOKENS_PATH), 'a+') as token:
                if "snusbase" in f:
                    username = lib.formatter.prompt(
                        "enter your username for snusbase", lowercase=False
                    )
                    password = lib.formatter.prompt(
                        "enter your snusbase password", lowercase=False
                    )
                    results = {"username": username, "password": password}
                    json.dump(results, token)
                else:
                    item = lib.formatter.prompt(
                        "you have not provided a token for {}, enter token".format(f.split("/")[-1]), lowercase=False
                    )
                    token.write(item.strip())
        with open(f.format(TOKENS_PATH)) as data:
            token_identifier = f.split("/")[-1]
            if "snusbase" in f:
                tokens[token_identifier] = json.load(data)
            else:
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

    def output_loop(data, identifier, loop_length=10, numbers=False):
        if len(data) != 0:
            lib.formatter.info("discovered associated {}:".format(identifier))
            total = len(data)
            for i, item in enumerate(data, start=1):
                if i != loop_length:
                    if item is not None:
                        print("\t-> {}".format(str(item).replace(" ", "-") if numbers else str(item)))
                else:
                    lib.formatter.warn("hit maximum length, total of {} not displayed".format(total - i))
                    break
        else:
            lib.formatter.warn("did not discover any associated {}".format(identifier))

    lib.formatter.info("information discovered associated with {}".format(domain))
    if "None" not in pattern:
        lib.formatter.info("discovered possible pattern to emails: {}".format(pattern))
    else:
        lib.formatter.warn("no email recognition pattern found")
    output_loop(numbers, "phone number(s)", numbers=True)
    output_loop(emails, "email address(es)")
    output_loop(urls, "external URL(s)")
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


def test_file(filename):
    """
    check if a file exists or not
    """
    try:
        open(filename).close()
        return True
    except IOError:
        return False
