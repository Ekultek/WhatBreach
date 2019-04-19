import requests
from bs4 import BeautifulSoup

from lib.settings import (
    DEHASHED_URL,
    VERIFICATION_REGEX,
    DEFAULT_REQUEST_HEADERS
)


class DehashedHook(object):

    def __init__(self, found_breaches, headers=False, proxies=False):
        if not proxies:
            proxies = {}
        if not headers:
            headers = DEFAULT_REQUEST_HEADERS
        self.found = found_breaches
        self.headers = headers
        self.proxies = proxies
        self.return_value = None

    def _parse_html(self):
        """
        returns a dict of parsed HTML if the term is in the HTML
\        """
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
                req = requests.get(search_url, proxies=self.proxies, headers=self.headers)
                content = (BeautifulSoup(req.content, "html.parser").extract().decode("utf-8"), search_url)
            except Exception:
                content = (None, search_url)
            if content[0] != "" or content[0] is not None:
                self.return_value.append(content)
        if len(self.return_value) != 0:
            return self._parse_html()
        else:
            return None

