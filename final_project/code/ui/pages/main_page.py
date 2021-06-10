import logging

from ui.locators.main_locators import MainPageLocators
from ui.pages.base_page import BasePage


CLICK_RETRY = 3
BASE_TIMEOUT = 5

logger = logging.getLogger('test')


class MainPage(BasePage):

    url = 'http://0.0.0.0:8095/welcome/'
    locators = MainPageLocators()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')
