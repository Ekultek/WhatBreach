import re
import os

import requests
from bs4 import BeautifulSoup

from lib.formatter import info
from lib.settings import (
    DATABASES_URL,
    DEFAULT_REQUEST_HEADERS,
    DOWNLOADS_PATH
)


class DatabasesTodayHook(object):

    # thank you NullArray for this idea and being an all around badass
    # if you dunno him, go checkout his Github https://github.com/NullArray
    # he practically invented being awesome!

    def __init__(self, query, proxies=False, headers=False, **kwargs):
        if not proxies:
            proxies = {}
        if not headers:
            headers = DEFAULT_REQUEST_HEADERS
        self.query = query
        self.proxies = proxies
        self.headers = headers
        self.content = None
        self.downloaded_databases = []
        self.database_links = []
        self.downloads_directory = kwargs.get("downloads_directory", DOWNLOADS_PATH)

    def _parse_html(self):
        """
        parse the HTML and return it if it has the data in it
        """
        searcher = re.compile("{}".format(self.query), re.I)
        if searcher.search(str(self.content)) is not None:
            return True
        return False

    def _find_database_links(self):
        """
        find the links to the databases
        """
        for table in self.content.find_all(id="myTable"):
            for td in table.find_all('td'):
                results = td.find_all('a', href=True)
                if len(results) != 0:
                    self.database_links.append(results)

    def _download_database(self, chunk_size=8192):
        """
        download the database if it is available
        """
        info("discovered publicly available database for query {}".format(self.query))
        flatten = lambda l: [str(item) for sublist in l for item in sublist]
        database_links = flatten(self.database_links)
        to_download = []
        for db in database_links:
            try:
                to_download.append(db.split('"')[3])
            except Exception:
                pass
        if not os.path.exists(self.downloads_directory):
            os.makedirs(self.downloads_directory)
        for link in to_download:
            local_filename = link.split("/")[-1]
            local_file_path = "{}/{}".format(self.downloads_directory, local_filename)
            if not os.path.exists(local_file_path):
                with requests.get(link, stream=True, proxies=self.proxies, headers=self.headers) as downloader:
                    downloader.raise_for_status()
                    with open(local_file_path, "wb") as path:
                        for chunk in downloader.iter_content(chunk_size=chunk_size):
                            if chunk:
                                path.write(chunk)
                self.downloaded_databases.append(local_file_path)
        return self.downloaded_databases

    def hooker(self):
        """
        hookers gonna hook
        """
        try:
            req = requests.get(DATABASES_URL.format(self.query.lower()), headers=self.headers, proxies=self.proxies)
            soup = BeautifulSoup(req.content, "html.parser")
            self.content = soup.extract()
            results = self._parse_html()
            if results:
                self._find_database_links()
                if len(self.database_links) != 0:
                    return self._download_database()
            else:
                return []
        except Exception:
            return []
