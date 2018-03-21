import json
import re
from random import randint

import requests
from bs4 import BeautifulSoup

from DataModel.App import App
from DataModel.Device import Device
from DataModel.User import User

LOGIN_SUCCESS = 0
LOGIN_ACCOUNT_NOT_EXISTS = 1
LOGIN_FAILURE = 2
LOGIN_NEED_PIN_VERIFICATION = 3

SSL_VERIFICATION_FLAG = True

API_JSON_RESPONSE_PREFIX = ")]}'\n\n"
API_JSON_RESPONSE_PREFIX_LEN = len(API_JSON_RESPONSE_PREFIX)

GOOGLE_LOGIN_PAGE = "https://accounts.google.com/ServiceLogin"
ACCOUNT_LOOKUP_API = "https://accounts.google.com/_/signin/sl/lookup?hl=en&_reqid=%s&rt=j"
ACCOUNT_LOGIN_API = "https://accounts.google.com/_/signin/sl/challenge?hl=en&_reqid=%s&rt=j"
ACCOUNT_VERIFY_PIN_API = "https://accounts.google.com/_/signin/challenge?hl=en&_reqid=%s&rt=j&TL="
ACCOUNT_API_DATA_KEY = "f.req"
LOGIN_SUCCESS_COOKIE = "SID"

GOOGLE_PLAY_HOST = "https://play.google.com"
GOOGLE_PLAY_APPS_PAGE = "https://play.google.com/apps"
CSRF_TOKEN_REG_EXP = "window._uc='\[\\\\x22(.*?)\\\\x22,"
GOOGLE_PLAY_FETCH_USER_AND_DEVICE_API = "https://play.google.com/store/xhr/ructx?authuser=0"
GOOGLE_PLAY_INSTALL_API = "https://play.google.com/store/install?authuser=0"
GOOGLE_PLAY_DEVICE_APP_PAGE = "https://play.google.com/apps?androidId=%s"
GOOGLE_PLAY_SEARCH_PAGE = "https://play.google.com/store/search?c=apps&q=%s"
NPD_REG_EXP = "nbp='(\[.*\])"


class GoogleApi:
    def __init__(self):
        print "GoogleApi class initiated!"
        self.__cookies = None
        self.__apps_page = None
        self.__csrf = None
        self.__user = None
        self.__devices = None
        self.__tl = None
        self.__account_identifier = None
        self.__reqid = None
        self.__api_count = None

    def login(self, account=None, pswd=None):
        self.__reqid = randint(10000, 99999)
        self.__api_count = 0

        # Get necessary cookies from login page
        self._account_api_get(GOOGLE_LOGIN_PAGE)

        # Lookup account info
        lookup_params = {
            ACCOUNT_API_DATA_KEY: self._get_lookup_request_body(account)
        }
        lookup_response = self._account_api_post(ACCOUNT_LOOKUP_API, lookup_params)

        if not lookup_response.startswith(API_JSON_RESPONSE_PREFIX):
            print "Account lookup failed"
            return LOGIN_ACCOUNT_NOT_EXISTS

        try:
            account_info = json.loads(lookup_response[API_JSON_RESPONSE_PREFIX_LEN:])
            self.__account_identifier = account_info[0][0][2]
        except IndexError:
            print "Cannot get account identifier"
            return LOGIN_ACCOUNT_NOT_EXISTS

        # Login
        login_params = {
            ACCOUNT_API_DATA_KEY: self._get_login_request_body(self.__account_identifier, pswd)
        }
        login_response = self._account_api_post(ACCOUNT_LOGIN_API, login_params)

        # Finalize login
        return self._process_login_response(login_response)

    def verify_pin(self, pin=None):
        verify_pin_params = {
            ACCOUNT_API_DATA_KEY: self._get_verify_pin_request_body(self.__account_identifier, pin)
        }
        api = ACCOUNT_VERIFY_PIN_API + self.__tl
        response = self._account_api_post(api, verify_pin_params)

        # Finalize verify
        return self._process_login_response(response)

    def _account_api_post(self, api, params):
        if 0 == self.__api_count:
            api = api % str(self.__reqid)
        else:
            api = api % (str(self.__api_count)+str(self.__reqid))
        self.__api_count += 1
        session = requests.Session()
        response = session.post(api, data=params, headers=self._get_account_api_headers(),
                                cookies=self.__cookies, verify=SSL_VERIFICATION_FLAG)
        self.__cookies = session.cookies.get_dict()
        return response.content

    def _account_api_get(self, api):
        session = requests.Session()
        session.get(api, verify=SSL_VERIFICATION_FLAG)
        self.__cookies = session.cookies.get_dict()

    def _process_login_response(self, response):
        if LOGIN_SUCCESS_COOKIE in self.__cookies:
            self.__apps_page = self._play_api_get(GOOGLE_PLAY_APPS_PAGE)

            p = re.compile(CSRF_TOKEN_REG_EXP)
            result = p.findall(self.__apps_page)
            if 1 == len(result):
                print "Login succeeded!"
                self.__csrf = result[0]
                self._get_user_and_devices()
                return LOGIN_SUCCESS
            else:
                print "Login failed. No CSRF found"
                return LOGIN_FAILURE
        else:
            if not response.startswith(API_JSON_RESPONSE_PREFIX):
                print "Login failed. No 2-step verification data in response"
                return LOGIN_FAILURE

            try:
                two_step_info = json.loads(response[API_JSON_RESPONSE_PREFIX_LEN:])
                self.__tl = two_step_info[0][1][2]
                if not self.__tl:
                    print "Login failed. 2-step verification data insufficient"
                    return LOGIN_FAILURE
                else:
                    print "Need 2-step verification to login"
                    return LOGIN_NEED_PIN_VERIFICATION
            except IndexError:
                print "Login failed. No 2-step verification data"
            return LOGIN_FAILURE

    @staticmethod
    def _get_lookup_request_body(account):
        data = [account,
                None,
                [],
                None,
                "US",
                None,
                None,
                2,
                False,
                True,
                [None, None, [2, 1, None, 1, None, None, [], 4], 1, [None, None, []], None, None, None, True],
                account]
        return json.JSONEncoder().encode(data)

    @staticmethod
    def _get_login_request_body(account_identifier, pw):
        data = [account_identifier,
                None,
                1,
                None,
                [1, None, None, None, [pw, None, True]],
                [None, None, [2, 1, None, 1, None, None, [], 4], 1, [None, None, []], None, None, None, True]
                ]
        return json.JSONEncoder().encode(data)

    @staticmethod
    def _get_verify_pin_request_body(account, pin):
        data = [account,
                None,
                2,
                None,
                [9, None, None, None, None, None, None, None, [None, pin, True, 2]]
                ]
        return json.JSONEncoder().encode(data)

    @staticmethod
    def _get_account_api_headers():
        return {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
            "Google-Accounts-XSRF": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache"
        }

    def get_device_list(self):
        if not self.__cookies:
            print "Please login in first!"
            return None

        if self.__devices is None:
            self._get_user_and_devices()
        else:
            return self.__devices

    def install_app(self, package, device_id):
        device = self._find_device_by_id(device_id)
        params = {"id": package,
                  "device": device.get_gsf_id(),
                  "token": self.__csrf,
                  "xhr": 1}
        response = self._play_api_post(GOOGLE_PLAY_INSTALL_API, params)

        if not response or not response.startswith(API_JSON_RESPONSE_PREFIX):
            print ":( Install", package, "failed on", device.get_display_name()
            return False

        try:
            result = json.loads(response[API_JSON_RESPONSE_PREFIX_LEN:])
            if 1 == result[0][1]:
                print ":) Install", package, "succeeded on", device.get_display_name()
                return True
            else:
                print ":( Install", package, "failed on", device.get_display_name()
                return False
        except IndexError:
            print ":( Install", package, "failed on", device.get_display_name()
            return False
        except ValueError:
            print ":( Install", package, "failed on", device.get_display_name()
            return False

    def _find_device_by_id(self, device_id):
        for device in self.__devices:
            if device_id == device.get_web_id():
                return device

        return None

    def _get_user_and_devices(self):
        self._fetch_user_and_devices()
        self._update_device_web_id()

    def _fetch_user_and_devices(self):
        params = {"xhr": 1, "token": self.__csrf}
        response = self._play_api_post(GOOGLE_PLAY_FETCH_USER_AND_DEVICE_API, params)

        if not response or not response.startswith(API_JSON_RESPONSE_PREFIX):
            return []

        try:
            json_text = response[API_JSON_RESPONSE_PREFIX_LEN:]
            json_text = ','.join([v or '""' for v in json_text.split(",")])
            obj = json.loads(json_text)
            info = obj[0][2]

            self.__user = User()
            self.__user.set_name(info[8], info[9])
            self.__user.set_email(info[15])

            devices = list()
            for raw in info[10]:
                devices.append(Device(raw[1], raw[0], raw[2], raw[3], raw[10], raw[6]))
            self.__devices = devices
        except IndexError:
            print "Error when parsing user and device info"

    def _update_device_web_id(self):
        soup = BeautifulSoup(self.__apps_page, "lxml")
        founds = soup.find_all("a", class_="leaf-submenu-link", href=re.compile("androidId="))

        if not founds or 0 == len(founds):
            print "No device found!"
            return None

        for tag in founds:
            name = tag["title"]
            link = tag["href"]
            equal_index = link.find("=")
            web_id = link[equal_index + 1:]

            for device in self.__devices:
                if device.get_display_name() == name:
                    device.set_web_id(web_id)

    def get_apps_by_device_web_id(self, device_id=None):
        if not self.__cookies:
            print "Please login in first!"
            return None

        if not device_id:
            print "Please pass a non-empty device id!"
            return None

        response = self._play_api_get(GOOGLE_PLAY_DEVICE_APP_PAGE % device_id)

        if response:
            apps = list()
            self._build_app_list_from_apps_page(response, apps)
            return apps
        else:
            print "Device " + device_id + " not exist!"
            return None

    def _build_app_list_from_apps_page(self, page_content, apps):
        # Parse page first
        self._parse_apps(page_content, apps)

        # Check if more app pages need to be parsed
        new_page = self._fetch_next_apps_page(page_content)
        if new_page is None or "" == new_page:
            return
        else:
            self._build_app_list_from_apps_page(new_page, apps)

    def _fetch_next_apps_page(self, current_page):
        p = re.compile(NPD_REG_EXP)
        result = p.findall(current_page)
        if 1 == len(result):
            npd_json = result[0].decode('unicode_escape').decode('unicode_escape')
            npd = json.loads(npd_json)
            api_url = npd[0] + "&authuser=0"
            if api_url.startswith("/"):
                api_url = GOOGLE_PLAY_HOST + api_url
            page_token = npd[1]
            params = {"start": 0, "num": 0, "numChildren": 0,
                      "pagTok": page_token, "pagtt": 1,
                      "cllayout": "MULTI_CORPUS_SHORT",
                      "ipf": 1, "xhr": 1, "token": self.__csrf
                      }
            return self._play_api_post(api_url, params)
        else:
            return None

    def search_apps(self, keyword):
        if not self.__cookies:
            print "Please login in first!"
            return None

        response = self._play_api_get(GOOGLE_PLAY_SEARCH_PAGE % keyword)

        if response:
            apps = list()
            self._build_app_list_from_search(response, 0, apps)
            return apps
        else:
            print "Search for " + keyword + " failed!"
            return None

    def _build_app_list_from_search(self, page_content, page_number, apps):
        # Parse page first
        self._parse_apps(page_content, apps)

        page_number += 1
        # Check if more app pages need to be parsed
        new_page = self._fetch_next_search_page(page_content, page_number, 48)
        if new_page is None or "" == new_page:
            return
        else:
            self._build_app_list_from_search(new_page, page_number, apps)

    def _fetch_next_search_page(self, current_page, start, number):
        p = re.compile(NPD_REG_EXP)
        result = p.findall(current_page)
        if 1 == len(result):
            npd_json = result[0].decode('unicode_escape').decode('unicode_escape')
            npd = json.loads(npd_json)
            api_url = npd[0] + "&authuser=0"
            if api_url.startswith("/"):
                api_url = GOOGLE_PLAY_HOST + api_url
            page_token = npd[1]
            params = {"start": start * number, "num": number, "numChildren": 0,
                      "pagTok": page_token, "pagtt": 3, "cctcss": "square-cover",
                      "cllayout": "NORMAL",
                      "ipf": 1, "xhr": 1, "token": self.__csrf}
            return self._play_api_post(api_url, params)
        else:
            return None

    @staticmethod
    def _parse_apps(content, apps):
        if content or 0 < len(content):
            soup = BeautifulSoup(content, "lxml")
            tags = soup.find_all("div", class_="cover")

            for app_tag in tags:
                image_tag = app_tag.find("img", class_="cover-image")
                image_url = image_tag["src"]
                image_url = image_url[:image_url.find("=")]
                if not image_url.startswith("http"):
                    image_url = "https:" + image_url
                app_name = image_tag["alt"]
                link_tag = app_tag.find("span", class_="preview-overlay-container")
                app_package = link_tag["data-docid"]
                apps.append(App(app_package, app_name, image_url))

        return apps

    def _play_api_get(self, api):
        session = requests.Session()
        response = session.get(api, cookies=self.__cookies, verify=SSL_VERIFICATION_FLAG)
        if response.ok:
            return response.content
        else:
            return None

    def _play_api_post(self, api, params):
        session = requests.Session()
        response = session.post(api, cookies=self.__cookies, data=params,
                                headers=self._get_play_api_header(), verify=SSL_VERIFICATION_FLAG)
        if response.ok:
            return response.content
        else:
            return None

    @staticmethod
    def _get_play_api_header():
        return {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
