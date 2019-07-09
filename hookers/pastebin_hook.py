import os

import requests

import lib.settings
import lib.formatter


class PastebinRawHook(object):

    def __init__(self, link, headers=None, proxies=None):
        self.link = link
        if proxies is None:
            proxies = {}
        if headers is None:
            headers = lib.settings.DEFAULT_REQUEST_HEADERS
        self.headers = headers
        self.proxies = proxies

    def hooker(self, chunk_size=8192):
        """
        hookers gonna hook
        """
        try:
            if not os.path.exists(lib.settings.PASTEBIN_DOWNLOADS):
                os.makedirs(lib.settings.PASTEBIN_DOWNLOADS)
            with requests.get(self.link, stream=True, proxies=self.proxies, headers=self.headers) as downloader:
                local_filename = self.link.split("/")[-1]
                local_file_path = "{}/{}_pastebin.txt".format(lib.settings.PASTEBIN_DOWNLOADS, local_filename)
                if not os.path.exists(local_file_path):
                    downloader.raise_for_status()
                    with open(local_file_path, 'wb') as path:
                        for chunk in downloader.iter_content(chunk_size=chunk_size):
                            if chunk:
                                path.write(chunk)
                return local_file_path
        except Exception:
            return None
