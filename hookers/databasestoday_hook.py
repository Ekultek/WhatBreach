import re
import os

import requests
from bs4 import BeautifulSoup

from lib.formatter import (
    prompt,
    warn,
    info
)
from lib.settings import (
    # DATABASES_URL,
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
        answer = prompt(
            "discovered publicly available database for query {}, do you want to download [y/N]".format(self.query)
        )
        flatten = lambda l: [str(item) for sublist in l for item in sublist]
        database_links = flatten(self.database_links)
        to_download = []
        for db in database_links:
            try:
                to_download.append(db.split('"')[3])
            except Exception:
                pass
        if answer == "y":
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
        else:
            info("skipping download as requested")
        return self.downloaded_databases

    def hooker(self):
        """
        hookers gonna hook
        """
        warn(
            "databases.today is down, switching to wayback machine (this isn't as reliable but it will still work)"
        )
        return WayBackMachine(
            self.query, self.proxies, self.headers
        ).hooker()
        # try:
        #     req = requests.get(DATABASES_URL.format(self.query.lower()), headers=self.headers, proxies=self.proxies)
        #     soup = BeautifulSoup(req.content, "html.parser")
        #     self.content = soup.extract()
        #     results = self._parse_html()
        #     if results:
        #         self._find_database_links()
        #         if len(self.database_links) != 0:
        #             return self._download_database()
        #     else:
        #         return []
        # except Exception as e:
        #     return []


class WayBackMachine(object):

    # fix until databases.today comes back online, not as reliable but will still work

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
        self.downloads_directory = kwargs.get("downloads_directory", None)

    def _gather_database_urls(self):
        retval = []
        search_urls = (
            "https://web.archive.org/web/20190409132908/https://cdn.databases.today/",
            "https://web.archive.org/web/20190409132908/https://cdn.databases.today/random",
            "https://web.archive.org/web/20190126112059/http://cdn.databases.today/random/dumps/",
            "https://web.archive.org/web/20190115081847/http://cdn.databases.today/random/files/",
            "https://web.archive.org/web/20190128131503/http://cdn.databases.today/random/github/DevGames/",
            "https://web.archive.org/web/20190128131528/http://cdn.databases.today/random/github/Devin148/",
            "https://web.archive.org/web/20190128131538/http://cdn.databases.today/random/github/WiseXP/",
            "https://web.archive.org/web/20190128131619/http://cdn.databases.today/random/github/chre/",
            "https://web.archive.org/web/20190128131637/http://cdn.databases.today/random/github/leonardoipx/",
            "https://web.archive.org/web/20190115210749/http://cdn.databases.today/random/minecraft/",
            "https://web.archive.org/web/20190124232905/http://cdn.databases.today/random/unverified/",
            "https://web.archive.org/web/20190115210130/http://cdn.databases.today/random/vbulletindump/"
        )
        for link in search_urls:
            try:
                req = requests.get(link, headers=self.headers, proxies=self.proxies)
                retval.append((req.content, link))
            except:
                retval.append((None, None))
        return retval

    def _get_links(self, content):
        urls = []

        for item in content:
            if item[0] is not None:
                soup = BeautifulSoup(item[0], "html.parser")
                for href in soup.findAll('a'):
                    try:
                        urls.append("{}".format(href['href']))
                    except:
                        pass
        return urls

    def _check_if_matched(self, urls):
        matched_urls = []
        for url in urls:
            searcher = re.compile(self.query, re.I)
            if searcher.search(url) is not None:
                matched_urls.append(url)
        return matched_urls

    def hooker(self):
        """
        temporary hookers gonna hook harder than normal hookers
        """
        content = self._gather_database_urls()
        links = self._get_links(content)
        matched_databases = self._check_if_matched(links)
        if len(matched_databases) != 0:
            info(
                'found a total of {} databases(s) that matched the query, dumping URL list'.format(
                    len(matched_databases)
                )
            )
            for db in matched_databases:
                print("\t~~> {}".format(db))
        return []
