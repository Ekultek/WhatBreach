from __future__ import print_function
import requests
from time import sleep

from lib.settings import HIBP_URL, HIBP_PASTE_URL, DEFAULT_REQUEST_HEADERS


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
            identifier = u"Id"
        else:
            identifier = u"Name"
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
                print(
                    "HIBP Rate Limit Exceeded, try again in "
                    + str(wait_time)
                    + " seconds"
                )
                sleep(wait_time)
                account_hooker(self)
            self.content = req.json()
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
