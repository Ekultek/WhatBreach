import requests

from bs4 import BeautifulSoup

from lib.formatter import warn
from lib.settings import (
    SNUSBASE_URL_DICT,
    DEFAULT_REQUEST_HEADERS
)


class SnusbaseHooker(object):

    def __init__(self, email, username, password, proxy=None, headers=None):
        self.email = email
        self.username = username
        self.password = password
        if proxy is None:
            proxy = {}
        if headers is None:
            headers = DEFAULT_REQUEST_HEADERS
        self.proxy = proxy
        self.headers = headers
        self.login_post_data = {"login": self.username, "password": self.password, "action_login": ""}
        self.search_post_data = {"csrf_token": "", "term": self.email, "searchtype": "email"}

    def __start_session(self):
        session = requests.session()
        session.headers = self.headers
        session.proxies = self.proxy
        return session

    def __get_csrf_token(self, session):
        try:
            csrf_url = SNUSBASE_URL_DICT["search"]
            req = session.get(csrf_url)
            soup = BeautifulSoup(req.content, "html.parser")
            token = soup.find('input', {'name': 'csrf_token'})['value']
            return token
        except TypeError:
            return None

    def __do_login(self, session):
        login_url = SNUSBASE_URL_DICT["login"]
        post_data = self.login_post_data
        req = session.post(login_url, data=post_data)
        cookie = req.headers['Set-Cookie']
        cf_ray = req.headers['CF-RAY']
        self.headers['CF-RAY'] = cf_ray
        self.headers['Set-Cookie'] = cookie
        session.headers = self.headers

    def __do_search(self, session):
        search_url = SNUSBASE_URL_DICT["search"]
        req = session.post(search_url, data=self.search_post_data)
        return req.content

    def __parse_results(self, res):
        tmp = set()
        retval = set()
        soup = BeautifulSoup(res, "html.parser")
        result_data = soup.findAll('div', {'id': 'topBar'})
        for div in result_data:
            tmp.add(str(div))
        for item in list(tmp):
            try:
                name = item.split("topBar")[-1].split("target=")[0].split("<")[0].strip('"').strip(">").replace("_", " ").split(" ")[0].lower()
                retval.add(name)
            except:
                pass
        return list(retval)

    def main(self):
        session = self.__start_session()
        self.__do_login(session)
        csrf_token = self.__get_csrf_token(session)
        if csrf_token is None:
            warn("login failed, is your password correct?")
            return []
        self.search_post_data["csrf_token"] = csrf_token
        results = self.__do_search(session)
        breaches = self.__parse_results(results)
        if len(breaches) == 0:
            return None
        return breaches
