import requests

from lib.settings import (
    DEFAULT_REQUEST_HEADERS,
    EMAILREP_IO_LINK
)


class EmailRepHook(object):

    def __init__(self, email, proxies=None, headers=None):
        if proxies is None:
            proxies = {}
        if headers is None:
            headers = DEFAULT_REQUEST_HEADERS
        self.headers = headers
        self.proxies = proxies
        self.email = email

    def _parse_results(self, content):
        results = []
        for item in content["details"]["profiles"]:
            results.append(str(item))
        return results

    def hooker(self):
        try:
            req = requests.get(EMAILREP_IO_LINK.format(self.email), proxies=self.proxies, headers=self.headers)
            return self._parse_results(req.json())
        except Exception:
            return None
