import logging

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.decorators import wait

CLICK_RETRY = 2
BASE_TIMEOUT = 10

logger = logging.getLogger('test')


class PageNotLoadedException(Exception):
    pass


class BasePage:

    url = 'http://0.0.0.0:8095/'

    def __init__(self, driver):
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')
        self.is_opened()

    def is_opened(self):
        def _check_url():
            if self.driver.current_url != self.url:
                raise PageNotLoadedException(
                    f'{self.url} did not opened in {BASE_TIMEOUT} for {self.__class__.__name__}.\n'
                    f'Current url: {self.driver.current_url}.')
            return True

        return wait(_check_url, error=PageNotLoadedException, check=True, timeout=BASE_TIMEOUT, interval=1)

    def is_element_clickable(self, locator):
        try:
            elem = self.wait(1).until(EC.element_to_be_clickable(locator))
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def find(self, locator, timeout=10):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def is_element_exist(self, locator):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i+1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=1)
                element = self.wait(1).until(EC.element_to_be_clickable(locator))
                return element.is_displayed()
            except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
                if i == CLICK_RETRY - 1:
                    return False

    def is_element_empty(self, locator):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i+1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=1)
                element = self.wait(1).until(EC.element_to_be_clickable(locator))
                return element.is_displayed()
            except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
                if i == CLICK_RETRY - 1:
                    return True

    def wait(self, timeout=5):
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=10):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i+1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
                if i == CLICK_RETRY - 1:
                    raise

    def write(self, locator, text):
        element = self.find(locator, timeout=5)
        element.clear()
        element.send_keys(text)
