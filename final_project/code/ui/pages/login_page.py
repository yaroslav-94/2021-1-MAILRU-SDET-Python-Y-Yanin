import logging

import allure
from selenium.webdriver.common.by import By

from ui.locators.login_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage

CLICK_RETRY = 3
BASE_TIMEOUT = 5

logger = logging.getLogger('test')


class LoginPage(BasePage):

    url = 'http://0.0.0.0:8095/'
    locators = LoginPageLocators()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')

    def login(self, user_login=None, user_password=None):
        with allure.step(f"Taken user_login '{user_login}'"):
            if user_login is not None:
                self.write(self.locators.LOG_INPUT_NAME_LOC, user_login)

        with allure.step(f"Taken user_password '{user_password}'"):
            if user_password is not None:
                self.write(self.locators.LOG_INPUT_PASS_LOC, user_password)

        assert self.find(self.locators.LOG_WELCOME_LABEL_LOC)
        assert self.find(self.locators.LOG_REGISTRATION_LOC)

        with allure.step('Click on button for entry'):
            self.click(self.locators.LOG_ENTRY_LOC)

    def go_to_registration(self):
        with allure.step('Go to registration page'):
            self.click(self.locators.LOG_REGISTRATION_LOC)
            assert self.find((By.XPATH, "//h3[text()='Registration']"))
            return RegistrationPage(self.driver)

    def go_to_main(self):
        with allure.step('Go to welcome-main page'):
            return MainPage(self.driver)
