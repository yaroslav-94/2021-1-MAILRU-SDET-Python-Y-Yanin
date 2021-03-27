import pytest
import string
import random

from hw_1.tests.base import BaseCase
from hw_1.ui.locators.balance_locators import *
from hw_1.ui.locators.base_locators import *
from ui.locators.profile_locators import *
from ui.locators.settings_locators import *


class TestOne(BaseCase):

    FIO = ''.join(random.choices(string.ascii_letters, k=10))
    PHONE = str(random.randint(10_000_000_000, 100_000_000_000))
    MAIL = ''.join(random.choices(string.ascii_letters, k=10) + ['@'] + random.choices(string.ascii_letters, k=5) + [".ru"])

    @pytest.mark.UI
    def test_login(self):
        self.authorize()

        assert self.driver.current_url == "https://target.my.com/dashboard"
        self.click(BALANCE_LOCATOR, 5)

        self.logout()

    @pytest.mark.UI
    def test_logout(self):
        self.authorize()

        self.click(BALANCE_LOCATOR, 5)

        self.logout()
        assert self.find(BASE_ENTER_LOCATOR)
        assert self.driver.current_url == "https://target.my.com/"

    @pytest.mark.UI
    def test_change_profile(self):
        self.authorize()

        self.click(PROFILE_INFO_LOCATOR, 5)
        self.write(PROFILE_FIO_LOCATOR, self.FIO)
        self.write(PROFILE_PHONE_LOCATOR, self.PHONE)
        self.write(PROFILE_EMAIL_LOCATOR, self.MAIL)
        self.click(PROFILE_SAVE_LOCATOR, 5)

        self.click(BALANCE_LOCATOR, 5)
        self.click(PROFILE_INFO_LOCATOR, 5)

        assert self.get_value(PROFILE_FIO_LOCATOR) == self.FIO
        assert self.get_value(PROFILE_PHONE_LOCATOR) == self.PHONE
        assert self.get_value(PROFILE_EMAIL_LOCATOR) == self.MAIL

        self.logout()

    @pytest.mark.UI
    @pytest.mark.parametrize('page, values', [
        (
            SETTING_LOCATOR, [SETTING_APP_LOCATOR, SETTING_CONVERSION_LOCATOR, SETTING_LIST_FEED_LOCATOR, SETTING_TRANSACTIONS_LOCATOR]
        ),
        (
            BALANCE_LOCATOR, [BALANCE_ADD_MONEY_LOCATOR, BALANCE_AUTO_ADD_MONEY_LOCATOR, BALANCE_OPERATION_LOCATOR]
        )
    ])
    def test_parametrize(self, page, values):
        self.authorize()

        self.click(page, 5)
        for i in values:
            self.click(i, 5)

        self.logout()
