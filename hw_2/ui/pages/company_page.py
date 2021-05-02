import logging
import os

from selenium.webdriver.common.by import By

from ui.locators.company_locators import CompanyLocators
from ui.pages.base_page import BasePage

logger = logging.getLogger('test')


class CompanyPage(BasePage):
    locators = CompanyLocators()
    url = 'https://target.my.com/dashboard'

    def __init__(self, driver):
        super().__init__(driver)

    def create_company(self, name="", url=""):
        self.click(self.locators.COMPANY_MAIN_LOCATOR)
        self.click(self.locators.COMPANY_CREATE_IN_LIST_LOCATOR)
        self.click(self.locators.COMPANY_AIM_CREATING_LOCATOR)
        self.write(locator=self.locators.COMPANY_AIM_URL_LOCATOR, text=url)
        self.write(locator=self.locators.COMPANY_NAME_NEW_LOCATOR, text=name)
        self.click(locator=self.locators.COMPANY_FORMAT_AD_LOCATOR)
        self.upload_file()
        self.click(locator=self.locators.COMPANY_CREATE_IN_LIST_LOCATOR)

    def delete_company(self, name=""):
        self.click(locator=(By.XPATH, self.locators.COMPANY_CHOOSE_IN_LIST_PATH.format(name)))
        self.click(locator=self.locators.COMPANY_ACTIONS_LOCATOR)
        self.click(locator=self.locators.COMPANY_DELETE_LOCATOR)

    def upload_file(self):
        elem = self.find(self.locators.COMPANY_UPLOAD_FILE_LOCATOR)
        path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
        path2 = os.path.join(path, 'download_files', 'photo.jpg')
        elem.send_keys(path2)
