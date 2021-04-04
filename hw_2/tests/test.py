import string
import random
import time

import pytest

from hw_2.tests.base import BaseCase


class TestHomeWork(BaseCase):

    URL_COMPANY = "https://ya.ru"
    FIO = ''.join(random.choices(string.ascii_letters, k=10))
    MAIL = ''.join(random.choices(string.ascii_letters, k=10) + ['@'] + random.choices(string.ascii_letters, k=5) + [".ru"])
    RANDOM_PASSWORD = ''.join(random.choices(string.ascii_letters, k=10)) + str(random.randint(0, 10_000_000_000))

    @pytest.mark.UI
    @pytest.mark.skip
    def test_authorize_negative_one(self):
        self.base_page.login(user_login=self.MAIL, user_password=self.RANDOM_PASSWORD)
        assert self.base_page.find(self.base_page.locators.BASE_ERROR)
        assert self.base_page.find(self.base_page.locators.BASE_ERROR_MSG)

    @pytest.mark.UI
    @pytest.mark.skip
    def test_authorize_negative_two(self):
        self.base_page.login(user_login=self.FIO, user_password=self.RANDOM_PASSWORD)
        assert self.base_page.find(self.base_page.locators.BASE_ERROR_BADLOGIN_LOCATOR)

    @pytest.mark.UI
    def test_create_company(self):
        self.base_page.login()

        self.company_page.click(self.company_page.locators.COMPANY_MAIN_LOCATOR)

        self.company_page.click(self.company_page.locators.COMPANY_CREATE_IN_LIST_LOCATOR)

        self.company_page.click(self.company_page.locators.COMPANY_AIM_CREATING_LOCATOR)

        self.company_page.write(locator=self.company_page.locators.COMPANY_AIM_URL_LOCATOR, text=self.URL_COMPANY)

        self.company_page.write(locator=self.company_page.locators.COMPANY_NAME_NEW_LOCATOR, text="My company create")

        self.company_page.click(locator=self.company_page.locators.COMPANY_FORMAT_AD_LOCATOR)

        self.company_page.upload_file()
        # time.sleep(2)
        # self.company_page.click(locator=self.company_page.locators.COMPANY_SAVE_IMAGE_LOCATOR)
        # time.sleep(2)
        self.company_page.click(locator=self.company_page.locators.COMPANY_SAVE_PARAMETERS_LOCATOR)
        time.sleep(2)

        self.company_page.click(locator=(self.company_page.locators.COMPANY_CHOOSE_IN_LIST_LOCATOR[0],
                                         self.company_page.locators.COMPANY_CHOOSE_IN_LIST_LOCATOR[1].format("My company create")))
        time.sleep(2)
        self.company_page.click(locator=self.company_page.locators.COMPANY_ACTIONS_LOCATOR)
        time.sleep(2)
        self.company_page.click(locator=self.company_page.locators.COMPANY_DELETE_LOCATOR)
        time.sleep(3)


    @pytest.mark.UI
    @pytest.mark.skip
    def test_auditory_segment(self):
        pass

    @pytest.mark.UI
    @pytest.mark.skip
    def test_auditory_deleting(self):
        pass
