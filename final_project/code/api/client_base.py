import logging

import allure
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
                 url=None, allow_redirects=False, cookies=None):

        if not url:
            url = urljoin(self.base_url, location)

        self.log_pre(method, url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data, json=json, verify=False,
                                        allow_redirects=allow_redirects, cookies=cookies)
        self.log_post(response)
        return response

    def add_user(self, user_name, user_pass, email):
        json_data = {}
        with allure.step(f"Create user with name '{user_name}'"):
            if user_pass is not None:
                json_data['password'] = user_pass

        with allure.step(f"Create user with password '{user_pass}'"):
            if user_name is not None:
                json_data['username'] = user_name

        with allure.step(f"Create user with email '{email}'"):
            if email is not None:
                json_data['email'] = email

        headers = {"Content-Type": "application/json"}
        return self._request(method='POST', location="/api/add_user", json=json_data, headers=headers,
                             expected_status=201)

    def login_in_api(self, user_name, user_pass):

        with allure.step(f"LOGIN IN APP WITH PASSWORD '{user_pass}', NAME '{user_name}'"):
            data = {
                "username": user_name,
                "password": user_pass,
                "submit": "Login"
            }
        return self._request(method="POST", location="/login", data=data)

    def delete_user(self, user_name):
        with allure.step(f"Delete user with name '{user_name}'"):
            if user_name is not None:
                return self._request(method='GET', location=f'/api/del_user/{user_name}')
            else:
                return self._request(method='GET', location='/api/del_user/')

    def lock_user(self, user_name):
        with allure.step(f"Lock user with name '{user_name}'"):
            if user_name is not None:
                return self._request(method="GET", location=f'/api/block_user/{user_name}')
            else:
                return self._request(method="GET", location='/api/block_user/')

    def unlock_user(self, user_name):
        with allure.step(f"Unlock user with name '{user_name}'"):
            if user_name is not None:
                return self._request(method="GET", location=f'/api/accept_user/{user_name}')
            else:
                return self._request(method="GET", location='/api/accept_user/')

    def state_app(self):
        return self._request(method="GET", location='/status')
