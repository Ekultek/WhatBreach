from time import sleep

import arrow
import requests

from lib.formatter import (
    warn,
    info,
    error
)
from lib.settings import (
    HIBP_URL,
    HIBP_PASTE_URL,
    DEFAULT_REQUEST_HEADERS,
    grab_random_user_agent,
    RANDOM_USER_AGENT_PATH
)


class BeenPwnedHook(object):

    def __init__(self, email, api_key, headers=False, proxies=False, blocked=1, retry=False):
        if not proxies:
            proxies = {}
        if not headers:
            headers = DEFAULT_REQUEST_HEADERS
        self.email = email
        self.headers = headers
        self.proxies = proxies
        self.content = None
        self.blocked = blocked
        self.max_attempts = 3
        self.retry = retry
        self.status_codes = {
            "blocked": 403,
            "throttled": 429
        }
        self.headers["hibp-api-key"] = api_key

    def _get_breach_names(self, is_paste=False):
        """
        get the names of the breaches from have i been pwned
        """
        report_names = set()
        if is_paste:
            identifier = ["Id", u"Id"]
        else:
            identifier = ["Name", u"Name"]
        if self.content is not None:
            for report in self.content:
                try:
                    for item in identifier:
                        report_names.add(report[item])
                except Exception:
                    pass
        else:
            return None
        return list(report_names)

    def account_hooker(self):
        """
        hookers accounting gonna hook
        """
        try:
            req = requests.get(
                HIBP_URL.format(self.email),
                headers=self.headers,
                proxies=self.proxies
            )
            if req.status_code == self.status_codes["throttled"]:
                wait_time = int(req.headers["Retry-After"])
                human = arrow.now().shift(seconds=wait_time).humanize()
                warn("HIBP Rate Limit Exceeded, trying again in {}".format(human))
                sleep(wait_time)
                info("here we go!")
                self.account_hooker()
            elif req.status_code == self.status_codes["blocked"]:
                if self.blocked != self.max_attempts:
                    if self.retry:
                        warn(
                            "you have been blocked from HIBP, WhatBreach will try {} more time(s)".format(
                                self.max_attempts - self.blocked
                            )
                        )
                        sleep(10)
                        BeenPwnedHook(
                            self.email, headers=self.headers,
                            proxies=self.proxies, blocked=self.blocked + 1
                        ).account_hooker()
                    else:
                        error(
                            "you have been blocked from HIBP, skipping and continuing, pass the `--do-retry` flag to "
                            "retry the requests on failure (max of 3 retries will be attempted)"
                        )
                else:
                    error(
                        "you have been blocked, {} attempts have failed, change your IP address and try again".format(
                            self.max_attempts
                        )
                    )
            else:
                self.content = req.json()
            if self.content is not None or self.content != "":
                return self._get_breach_names()
            else:
                return None
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
