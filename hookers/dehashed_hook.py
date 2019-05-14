import requests
from bs4 import BeautifulSoup

from lib.formatter import warn

from lib.settings import (
    grab_random_user_agent,
    DEHASHED_URL,
    VERIFICATION_REGEX,
    DEFAULT_REQUEST_HEADERS,
    RANDOM_USER_AGENT_PATH
)


class DehashedHook(object):

    def __init__(self, found_breaches, headers=False, proxies=False):
        if not proxies:
            proxies = {}
        if not headers:
            headers = DEFAULT_REQUEST_HEADERS
            headers["User-Agent"] = grab_random_user_agent(RANDOM_USER_AGENT_PATH)
            # we're gonna go ahead and try to trick dehashed into thinking
            # we're a real person
            del headers["Made-With-Love"]
        self.found = found_breaches
        self.headers = headers
        self.proxies = proxies
        self.return_value = None

    def _parse_html(self):
        """
        returns a dict of parsed HTML if the term is in the HTML
        """
        retval = {}
        for i, value in enumerate(self.return_value):
            try:
                if value[0] is not None:
                    if VERIFICATION_REGEX.search(value[0]) is not None:
                        retval[self.found[i]] = (True, value[1])
                    else:
                        retval[self.found[i]] = (False, value[1])
            except Exception:
                retval[self.found[i]] = (False, value[1])
        return retval

    def hooker(self):
        """
        hookers still gonna hook
        """
        self.return_value = []
        for breach in self.found:
            search_url = DEHASHED_URL.format(str(breach).strip())
            try:
                req = requests.get(search_url, proxies=self.proxies, headers=self.headers, timeout=7)
                content = (BeautifulSoup(req.content, "html.parser").extract().decode("utf-8"), search_url)
            except Exception as e:
                if "HTTPSConnectionPool" in str(e):
                    warn(
                        "gateway timeout occurred while searching dehashed (this is caused by the fact that "
                        "dehashed doesn't like scraping), possible search URL: {}".format(
                            search_url
                        )
                    )
                content = (None, search_url)
            if content[0] != "" or content[0] is not None:
                self.return_value.append(content)
        if len(self.return_value) != 0:
            return self._parse_html()
        else:
            return None

