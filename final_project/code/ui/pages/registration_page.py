import logging

import allure

from ui.locators.registration_locators import RegistrationPageLocators
from ui.pages.base_page import BasePage

logger = logging.getLogger('test')


class RegistrationPage(BasePage):
    url = 'http://0.0.0.0:8095/reg'
    locators = RegistrationPageLocators()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')

    def registration(self, user_name=None, user_pass=None, email=None, accept_rule=1, rep_pass=None):

        with allure.step(f"Taken user_name '{user_name}'"):
            if user_name is not None:
                self.write(self.locators.REG_USERNAME_LOC, user_name)

        with allure.step(f"Taken user_pass '{user_pass}'"):
            if user_pass is not None:
                self.write(self.locators.REG_PASSWORD_LOC, user_pass)

        with allure.step(f"Taken email '{email}'"):
            if email is not None:
                self.write(self.locators.REG_EMAIL_LOC, email)

        with allure.step(f"Taken rep_pass '{rep_pass}'"):
            if rep_pass is not None:
                self.write(self.locators.REG_REP_PASS_LOC, rep_pass)

        with allure.step(f"Click on accept rules '{accept_rule}'"):
            if accept_rule is not None:
                self.click(self.locators.REG_ACCEPT_RULES_LOC)

        with allure.step('Click on button for entry'):
            self.click(self.locators.REG_REGISTER_LOC)
