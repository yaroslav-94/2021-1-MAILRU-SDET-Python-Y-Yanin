import logging
import time

from selenium.webdriver.common.by import By

from ui.locators.dashboard_locators import DashboardPageLocators
from ui.pages.auditory_page import AuditoryPage
from ui.pages.base_page import BasePage
from ui.pages.company_page import CompanyPage

CLICK_RETRY = 3
BASE_TIMEOUT = 5


logger = logging.getLogger('test')


class PageNotLoadedException(Exception):
    pass


class DashboardPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = DashboardPageLocators()

    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f'{self.__class__.__name__} page is opening...')
        assert self.is_opened()

    def logout(self):
        self.click((By.XPATH, "//div[contains(@class, 'right-module-rightWrap')]"))
        self.click((By.XPATH, "//a[text()='Выйти']"))
        time.sleep(2)

    def go_to_company(self):
        self.click(locator=self.locators.DASHBOARD_COMPANY_LOCATOR)
        return CompanyPage(driver=self.driver)

    def go_to_auditory(self):
        self.click(locator=self.locators.DASHBOARD_AUDITORY_LOCATOR)
        # self.find((By.XPATH, "//span[text()='Список сегментов']"))
        return AuditoryPage(driver=self.driver)
