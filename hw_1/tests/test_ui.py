import pytest
import string
import random

from tests.base import BaseCase
from ui.locators.balance_locators import BALANCE_LOCATOR, BALANCE_ADD_MONEY_LOCATOR, \
    BALANCE_AUTO_ADD_MONEY_LOCATOR, BALANCE_OPERATION_LOCATOR
from ui.locators.base_locators import BASE_ERROR, BASE_ERROR_MSG
from ui.locators.profile_locators import PROFILE_INFO_LOCATOR, PROFILE_FIO_LOCATOR, PROFILE_PHONE_LOCATOR, \
    PROFILE_EMAIL_LOCATOR, PROFILE_SAVE_LOCATOR
from ui.locators.settings_locators import SETTING_LOCATOR, SETTING_APP_LOCATOR, SETTING_CONVERSION_LOCATOR, \
    SETTING_LIST_FEED_LOCATOR, SETTING_TRANSACTIONS_LOCATOR


class TestOne(BaseCase):

    FIO = ''.join(random.choices(string.ascii_letters, k=10))
    PHONE = str(random.randint(10_000_000_000, 100_000_000_000))
    MAIL = ''.join(random.choices(string.ascii_letters, k=10) + ['@'] + random.choices(string.ascii_letters, k=5) + [".ru"])
    RANDOM_PASSWORD = ''.join(random.choices(string.ascii_letters, k=10)) + str(random.randint(0, 10_000_000_000))

    @pytest.mark.UI
    def test_login(self):
        self.authorize(login=self.MAIL, password=self.RANDOM_PASSWORD)

        assert self.find(BASE_ERROR, timeout=5)
        assert self.find(BASE_ERROR_MSG, timeout=5)

    @pytest.mark.UI
    def test_logout(self):
        self.authorize()

        assert self.driver.current_url == "https://target.my.com/dashboard"

        self.logout()

        assert self.driver.find_element_by_xpath("//div[text()='Войти']")
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
