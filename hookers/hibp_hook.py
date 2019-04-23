import requests

from lib.settings import HIBP_URL, HIBP_PASTE_URL, DEFAULT_REQUEST_HEADERS

import arrow
from time import sleep

class BeenPwnedHook(object):
    def __init__(self, email, headers=False, proxies=False):
        if not proxies:
            proxies = {}
        if not headers:
            headers = DEFAULT_REQUEST_HEADERS
        self.email = email
        self.headers = headers
        self.proxies = proxies
        self.content = None

    def _get_breach_names(self, is_paste=False):
        """
        get the names of the breaches from have i been pwned
        """
        report_names = set()
        if is_paste:
            identifier = "Id"
        else:
            identifier = "Name"
        for report in self.content:
            try:
                report_names.add(report[identifier])
            except Exception:
                pass
        return list(report_names)

    def account_hooker(self):
        """
        hookers accounting gonna hook
        """
        try:
            req = requests.get(
                HIBP_URL.format(self.email), headers=self.headers, proxies=self.proxies
            )
            if req.status_code == 429:
                wait_time = int(req.headers["Retry-After"])
                human = arrow.now().shift(seconds=wait_time).humanize()
                print(f"HIBP Rate Limit Exceeded, try again {human}")
                sleep(wait_time)
            if self.content != "" or self.content is not None:
                return self._get_breach_names()
        except ValueError:
            # this means something went wrong
            return None

    def paste_hooker(self):
        """
        paste hookers gonna hook too
        """
        try:
            req = requests.get(
                HIBP_PASTE_URL.format(self.email),
                headers=self.headers,
                proxies=self.proxies,
            )
            self.content = req.json()
            return self._get_breach_names(is_paste=True)
        except Exception:
            return None
