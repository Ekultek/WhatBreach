import requests

from lib.settings import (
    DEFAULT_REQUEST_HEADERS,
    WELEAKINFO_URL
)


class WeLeakInfoHook(object):

    def __init__(self, email, token, proxies=None, headers=None):
        self.email = email
        if proxies is None:
            proxies = {}
        if headers is None:
            headers = DEFAULT_REQUEST_HEADERS
        headers['Authorization'] = "Bearer {}".format(token)
        self.headers = headers
        self.proxies = proxies

    def _make_request(self):
        """
        request the shit
        """
        try:
            req = requests.get(WELEAKINFO_URL.format(self.email), proxies=self.proxies, headers=self.headers)
            return req.json()
        except Exception:
            return {}

    def _parse_results(self, content):
        """
        parse the results from the requested shit
        """
        parsed_leaks = set()
        for item in content:
            if "-" in item:
                item = item.split(" ")[0]
            elif "(" in item:
                item = item.split("(")[0]
            parsed_leaks.add(str(item))
        return parsed_leaks

    def hooker(self):
        """
        work the corner hooker
        """
        # pssst, if you're reading this create an issue titled `fat clunky penguins` and you'll be my best friend
        # hi btw :D
        results = self._make_request()
        if results is not None and len(results) != 0:
            try:
                return self._parse_results(results['Data'])
            except Exception:
                return None
        else:
            return None
