import random
import string
import allure
import pytest
from selenium.webdriver.common.by import By
from tests.base import BaseCase


class TestHomeWork(BaseCase):
    COMPANY_URL = "https://ya.ru"
    COMPANY_NAME = "My company create " + "".join(random.choices(string.hexdigits, k=5))
    AUDITORY_SEGMENT_NAME = "Segment name " + "".join(random.choices(string.ascii_letters, k=5))
    AUDITORY_DELETE_SEGMENT_NAME = "Segment delete name " + "".join(random.choices(string.ascii_letters, k=5))

    @pytest.mark.UI
    def test_create_company(self):
        self.dashboard_page.is_opened()
        company_page = self.dashboard_page.go_to_company()

        with allure.step("Create new company"):
            company_page.create_company(name=self.COMPANY_NAME, url=self.COMPANY_URL)

        with allure.step("Switch between pages"):
            segment_page = self.dashboard_page.go_to_auditory()
            segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)
            company_page.click(locator=company_page.locators.COMPANY_MAIN_LOCATOR)
            company_page.click(locator=company_page.locators.COMPANY_STATUS_LIST_LOCATOR)

        with allure.step("Delete company"):
            company_page.delete_company(name=self.COMPANY_NAME)
        self.dashboard_page.logout()

    @pytest.mark.UI
    def test_auditory_segment(self):
        self.dashboard_page.is_opened()
        segment_page = self.dashboard_page.go_to_auditory()
        segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)

        with allure.step("Create new auditory"):
            segment_page.create_auditory(name=self.AUDITORY_SEGMENT_NAME)

        with allure.step("Switch between pages"):
            company_page = self.dashboard_page.go_to_company()
            company_page.click(locator=company_page.locators.COMPANY_MAIN_LOCATOR)

        with allure.step("Delete auditory"):
            segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)
            assert segment_page.find(locator=(By.XPATH, segment_page.locators.SEGMENT_CHOOSE_IN_LIST_PATH.format(self.AUDITORY_SEGMENT_NAME)))
            segment_page.delete_auditory(name=self.AUDITORY_SEGMENT_NAME)
        self.dashboard_page.logout()

    @pytest.mark.UI
    def test_auditory_deleting(self):
        self.dashboard_page.is_opened()
        segment_page = self.dashboard_page.go_to_auditory()
        segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)

        with allure.step("Create new auditory"):
            segment_page.create_auditory(name=self.AUDITORY_DELETE_SEGMENT_NAME)

        with allure.step("Delete auditory"):
            segment_page.delete_auditory(name=self.AUDITORY_DELETE_SEGMENT_NAME)

        with allure.step("Switch between pages"):
            company_page = self.dashboard_page.go_to_company()
            company_page.click(locator=company_page.locators.COMPANY_MAIN_LOCATOR)

        with allure.step("Сhecking for lack of audience "):
            segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)
            assert segment_page.is_element_clickable(
                locator=(By.XPATH, segment_page.locators.SEGMENT_CHOOSE_IN_LIST_PATH.format(
                    self.AUDITORY_DELETE_SEGMENT_NAME))) == False
        self.dashboard_page.logout()
