import logging
import requests
from urllib.parse import urljoin

logger = logging.getLogger('test')

MAX_RESPONSE_LENGTH = 500


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class InvalidLoginException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

        self.csrf_token = None

    @staticmethod
    def log_pre(method, url, headers, data, expected_status):
        logger.info(f'Performing {method} request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'expected status: {expected_status}\n\n')

    @staticmethod
    def log_post(response):
        log_str = 'Got response:\n' \
                  'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n')
            elif logger.level == logging.DEBUG:
                logger.debug(f'{log_str}\n'
                             f'RESPONSE CONTENT: {response.text}\n\n')
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n\n')

    def _request(self, method, location=None, headers=None, data=None, json=None, expected_status=200,
                 url=None, allow_redirects=True, cookies=None):

        if not url:
            url = urljoin(self.base_url, location)

        self.log_pre(method, url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data, json=json, verify=False,
                                        allow_redirects=allow_redirects, cookies=cookies)
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        return response

    def authorize(self, password, login):
        url_authorize = "https://auth-ac.my.com/auth?lang=ru&nosavelogin=0"

        data_authorize = {
            "email": f"{login}",
            "password": f"{password}"
        }

        headers_authorize = {
            "Origin": f"{self.base_url}",
            "Referer": f"{self.base_url}",
            "Connection": "keep-alive"
        }

        responce_auth = self._request(method="POST", url=url_authorize, data=data_authorize, headers=headers_authorize,
                                      allow_redirects=False, expected_status=302)

        location = "csrf/"
        responce_csrf = self._request("GET", location=location, cookies=responce_auth.cookies)
        self.csrf_token = responce_csrf.cookies.get("csrftoken")
