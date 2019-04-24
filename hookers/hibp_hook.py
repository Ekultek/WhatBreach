from time import sleep
import arrow
import requests

from lib.formatter import (
    warn,
    info
)
from lib.settings import (
    HIBP_URL,
    HIBP_PASTE_URL,
    DEFAULT_REQUEST_HEADERS
)


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
                warn("HIBP Rate Limit Exceeded, trying again in {}".format(human))
                sleep(wait_time)
                info("here we go!")
                self.account_hooker()
            else:
                self.content = req.json()
            if self.content is not None or self.content != "":
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
