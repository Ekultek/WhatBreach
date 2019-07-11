import os
import json
import requests

from lib.formatter import info

from lib.settings import (
    DEFAULT_REQUEST_HEADERS,
    EMAILREP_IO_LINK,
    write_processed_to_file,
    random_string,
    JSON_DATA_DUMPS
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
        if len(results) != 0:
            if not os.path.exists(JSON_DATA_DUMPS):
                os.makedirs(JSON_DATA_DUMPS)
            file_path = "{}/{}_emailrep.json".format(
                JSON_DATA_DUMPS, self.email.split("@")[0]
            )
            if not os.path.exists(file_path):
                with open(file_path, 'a+') as data:
                    json.dump(content, data, sort_keys=True, indent=4)
                info("all data dumped to file for future processing: {}".format(file_path))
        return results

    def hooker(self):
        try:
            req = requests.get(EMAILREP_IO_LINK.format(self.email), proxies=self.proxies, headers=self.headers)
            return self._parse_results(req.json())
        except Exception as e:
            print e
            return None
