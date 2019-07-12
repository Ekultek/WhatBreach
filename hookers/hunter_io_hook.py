import json

import requests
from lib.formatter import (
    info,
    error
)
from lib.settings import (
    HUNTER_IO_URL,
    DEFAULT_REQUEST_HEADERS,
    process_discovered,
    HUNTER_IO_VERIFY_URL
)


class HunterIoHook(object):

    def __init__(self, email, api_key, proxies=None, headers=None, verify_emails=False):
        if proxies is None:
            proxies = {}
        if headers is None:
            headers = DEFAULT_REQUEST_HEADERS
        self.api_key = api_key
        self.email = email
        self.proxies = proxies
        self.headers = headers
        self.verify = verify_emails

    def __get_domain_from_email(self):
        """
        associate the domain name of the email address
        """
        data_list = self.email.split("@")
        return data_list[-1]

    def __verify_emails_alive(self, email_list):
        """
        verify if the email address is deliverable or not
        """
        for email in email_list:
            info("verifying that {} is alive".format(email))
            try:
                req = requests.get(
                    HUNTER_IO_VERIFY_URL.format(email=email, api_key=self.api_key),
                    proxies=self.proxies, headers=self.headers
                )
                results = json.loads(req.text)["data"]["result"]
                if str(results) == "risky":
                    output_str = "\033[31m{}\033[0m".format(str(results))
                elif str(results) == "deliverable":
                    output_str = "\033[32m{}\033[0m".format(str(results))
                else:
                    output_str = "\033[33m{}\[033[0m".format(str(results))
                info("result of verification: {}".format(output_str))
            except:
                error("error verifying email: {}".format(email))

    def make_request(self):
        """
        make the request to the API
        """
        try:
            req = requests.get(
                HUNTER_IO_URL.format(
                    domain=self.__get_domain_from_email(),
                    api_key=self.api_key
                ),
                headers=self.headers,
                proxies=self.proxies
            )
            retval = req.text
        except Exception:
            retval = None
        return retval

    def hooker(self):
        """
        hookers gonna hook
        """
        set_to_list_phone_numebrs = []
        discovered_phone_numbers = set()
        other_discovered_emails = set()
        discovered_external_links = set()
        processed = json.loads(self.make_request())
        domain_name = self.__get_domain_from_email()
        if processed is not None:
            try:
                email_pattern_identification = "{}@{}".format(processed["data"]["pattern"], domain_name)
            except:
                email_pattern_identification = None
            for i, _ in enumerate(processed["data"]["emails"]):
                discovered_phone_numbers.add(processed["data"]["emails"][i]["phone_number"])
                other_discovered_emails.add(str(processed["data"]["emails"][i]["value"]))
                for y, _ in enumerate(processed["data"]["emails"][i]["sources"]):
                    discovered_external_links.add(str(processed["data"]["emails"][i]["sources"][y]["uri"]))
            for item in discovered_phone_numbers:
                if item is not None:
                    set_to_list_phone_numebrs.append(item)
            other_discovered_emails.add(self.email)
            info("discovered a total of {} email(s)".format(len(other_discovered_emails)))
            if self.verify:
                self.__verify_emails_alive(other_discovered_emails)
            file_path = process_discovered(
                set_to_list_phone_numebrs, discovered_external_links,
                other_discovered_emails, email_pattern_identification,
                domain_name, do_write=True
            )
            return file_path
        else:
            error("error while processing domain: {}".format(domain_name))
            return None
