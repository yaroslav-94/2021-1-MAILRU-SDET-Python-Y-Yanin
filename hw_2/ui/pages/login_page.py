import logging

from ui.locators.login_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage

CLICK_RETRY = 3
BASE_TIMEOUT = 5

logger = logging.getLogger('test')


class LoginPage(BasePage):

    url = 'https://target.my.com/'
    locators = LoginPageLocators()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')

    def login(self, user_login=None, user_password=None):
        self.click(self.locators.BASE_ENTER_LOCATOR, 5)
        self.write(self.locators.BASE_LOGIN_LOCATOR, user_login)
        self.write(self.locators.BASE_PASSWORD_LOCATOR, user_password)
        self.click(self.locators.BASE_AUTH_LOCATOR, 5)

        if self.driver.current_url == DashboardPage.url:
            return DashboardPage(self.driver)
