import string
import random
import pytest
from tests.base import BaseCase


URL_COMPANY = "https://ya.ru"
FIO = ''.join(random.choices(string.ascii_letters, k=10))
MAIL = ''.join(random.choices(string.ascii_letters, k=10) + ['@'] + random.choices(string.ascii_letters, k=5) + [".ru"])
RANDOM_PASSWORD = ''.join(random.choices(string.ascii_letters, k=10)) + str(random.randint(0, 10_000_000_000))


class TestInvalidRegistraition(BaseCase):

    authorize = False

    @pytest.mark.UI
    def test_authorize_negative_one(self):
        self.login_page.login(user_login=MAIL, user_password=RANDOM_PASSWORD)
        assert self.login_page.find(self.login_page.locators.BASE_ERROR)
        assert self.login_page.find(self.login_page.locators.BASE_ERROR_MSG)

    @pytest.mark.UI
    def test_authorize_negative_two(self):
        self.login_page.login(user_login=FIO, user_password=RANDOM_PASSWORD)
        assert self.login_page.find(self.login_page.locators.BASE_ERROR_BADLOGIN_LOCATOR)