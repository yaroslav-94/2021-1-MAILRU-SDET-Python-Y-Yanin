import pytest
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data import *
from ui.locators.base_locators import *

CLICK_RETRY = 5
BASE_TIMEOUT = 5


class BaseCase:
    driver = None
    config = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config

    def authorize(self):
        self.click(BASE_ENTER_LOCATOR, 5)
        self.write(BASE_LOGIN_LOCATOR, LOGIN_EMAIL)
        self.write(BASE_PASSWORD_LOCATOR, LOGIN_PASSWORD)
        self.click(BASE_AUTH_LOCATOR, 5)

    def logout(self):
        self.click(BASE_USER_INFO_LOCATOR, 5)
        self.click(BASE_LOGOUT_LOCATOR, 5)

    def wait(self, timeout):
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=5):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def get_value(self, locator):
        element = self.find(locator).get_attribute('value')
        return element

    def write(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator, timeout):
        for i in range(CLICK_RETRY):
            try:
                element = self.find(locator, timeout=timeout)
                element = self.wait(timeout).until(EC.presence_of_element_located(locator))
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException) as err:
                if i == CLICK_RETRY - 1:
                    raise
