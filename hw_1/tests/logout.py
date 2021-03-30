from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CLICK_RETRY = 3


class Logout:

    def __init__(self, driver):
        self.driver = driver

    def logout(self):
        self.click_element("//div[contains(@class, 'right-module-rightWrap')]")
        self.click_element("//a[text()='Выйти']")

    def click_element(self, path, timeout=10):
        for i in range(CLICK_RETRY):
            try:
                element = WebDriverWait(self.driver, timeout=timeout).until(EC.presence_of_element_located((By.XPATH, path)))
                element = WebDriverWait(self.driver, timeout=timeout).until(EC.element_to_be_clickable((By.XPATH, path)))
                element.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if i == CLICK_RETRY - 1:
                    raise

