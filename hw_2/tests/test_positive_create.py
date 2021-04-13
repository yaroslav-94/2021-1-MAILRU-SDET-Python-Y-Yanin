import allure
import pytest
from selenium.webdriver.common.by import By
from tests.base import BaseCase


class TestHomeWork(BaseCase):

    URL_COMPANY = "https://ya.ru"

    @pytest.mark.UI
    def test_create_company(self):
        self.dashboard_page.is_opened()
        company_page = self.dashboard_page.go_to_company()

        with allure.step("Create new company"):
            company_page.click(company_page.locators.COMPANY_MAIN_LOCATOR)
            company_page.click(company_page.locators.COMPANY_CREATE_IN_LIST_LOCATOR)
            company_page.click(company_page.locators.COMPANY_AIM_CREATING_LOCATOR)
            company_page.write(locator=company_page.locators.COMPANY_AIM_URL_LOCATOR, text=self.URL_COMPANY)
            company_page.write(locator=company_page.locators.COMPANY_NAME_NEW_LOCATOR, text="My company create")
            company_page.click(locator=company_page.locators.COMPANY_FORMAT_AD_LOCATOR)
            company_page.upload_file()
            company_page.click(locator=company_page.locators.COMPANY_CREATE_IN_LIST_LOCATOR)

        with allure.step("Switch between pages"):
            segment_page = self.dashboard_page.go_to_auditory()
            segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)
            company_page.click(locator=company_page.locators.COMPANY_MAIN_LOCATOR)
            company_page.click(locator=company_page.locators.COMPANY_STATUS_LIST_LOCATOR)

        with allure.step("Delete company"):
            company_page.click(
            locator=(By.XPATH, company_page.locators.COMPANY_CHOOSE_IN_LIST_PATH.format("My company create")))
            company_page.click(locator=company_page.locators.COMPANY_ACTIONS_LOCATOR)
            company_page.click(locator=company_page.locators.COMPANY_DELETE_LOCATOR)

    @pytest.mark.UI
    def test_auditory_segment(self):
        self.dashboard_page.is_opened()
        segment_page = self.dashboard_page.go_to_auditory()
        segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)

        with allure.step("Create new auditory"):
            if segment_page.is_element_clickable(locator=segment_page.locators.SEGMENT_CREATE_EMPTY_LOCATOR):
                segment_page.click(locator=segment_page.locators.SEGMENT_CREATE_EMPTY_LOCATOR)
            elif segment_page.is_element_clickable(locator=segment_page.locators.SEGMENT_CREATE_LOCATOR):
                segment_page.click(locator=segment_page.locators.SEGMENT_CREATE_LOCATOR)

            segment_page.click(locator=segment_page.locators.SEGMENT_SETTING_LOCATOR)
            segment_page.click(locator=segment_page.locators.SEGMENT_ADD_NEW_LOCATOR)
            segment_page.write(locator=segment_page.locators.SEGMENT_NAME_LOCATOR, text="Segment name")
            segment_page.click(locator=segment_page.locators.SEGMENT_CREATE_LOCATOR)

        with allure.step("Switch between pages"):
            company_page = self.dashboard_page.go_to_company()
            company_page.click(locator=company_page.locators.COMPANY_MAIN_LOCATOR)
            segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)

        with allure.step("Delete auditory"):
            assert segment_page.find(locator=(By.XPATH, segment_page.locators.SEGMENT_CHOOSE_IN_LIST_PATH.format("Segment name")))
            company_page.click(locator=(By.XPATH, segment_page.locators.SEGMENT_CHOOSE_IN_LIST_PATH.format("Segment name")))
            segment_page.click(locator=segment_page.locators.SEGMENT_ACTIONS_LOCATOR)
            segment_page.click(locator=segment_page.locators.SEGMENT_DELETE_LOCATOR)
        self.dashboard_page.logout()

    @pytest.mark.UI
    def test_auditory_deleting(self):
        self.dashboard_page.is_opened()
        segment_page = self.dashboard_page.go_to_auditory()
        segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)

        with allure.step("Create new auditory"):
            if segment_page.is_element_clickable(locator=segment_page.locators.SEGMENT_CREATE_EMPTY_LOCATOR):
                segment_page.click(locator=segment_page.locators.SEGMENT_CREATE_EMPTY_LOCATOR)
            elif segment_page.is_element_clickable(locator=segment_page.locators.SEGMENT_CREATE_LOCATOR):
                segment_page.click(locator=segment_page.locators.SEGMENT_CREATE_LOCATOR)

            segment_page.click(locator=segment_page.locators.SEGMENT_SETTING_LOCATOR)
            segment_page.click(locator=segment_page.locators.SEGMENT_ADD_NEW_LOCATOR)
            segment_page.write(locator=segment_page.locators.SEGMENT_NAME_LOCATOR, text="Segment delete name")
            segment_page.click(locator=segment_page.locators.SEGMENT_CREATE_LOCATOR)

        with allure.step("Delete auditory"):
            segment_page.click(
                locator=(By.XPATH, segment_page.locators.SEGMENT_CHOOSE_IN_LIST_PATH.format("Segment delete name")))
            segment_page.click(locator=segment_page.locators.SEGMENT_ACTIONS_LOCATOR)
            segment_page.click(locator=segment_page.locators.SEGMENT_DELETE_LOCATOR)

        with allure.step("Switch between pages"):
            company_page = self.dashboard_page.go_to_company()
            company_page.click(locator=company_page.locators.COMPANY_MAIN_LOCATOR)

        with allure.step("Сhecking for lack of audience "):
            segment_page.click(locator=segment_page.locators.SEGMENT_MAIN_LOCATOR)
            assert segment_page.is_element_clickable(
                locator=(By.XPATH, segment_page.locators.SEGMENT_CHOOSE_IN_LIST_PATH.format("Segment delete name"))) == False
        self.dashboard_page.logout()
