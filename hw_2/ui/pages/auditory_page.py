import logging

from selenium.webdriver.common.by import By

from ui.locators.segment_locators import SegmentLocators
from ui.pages.base_page import BasePage

logger = logging.getLogger('test')


class AuditoryPage(BasePage):
    locators = SegmentLocators()
    url = "https://target.my.com/segments/segments_list"

    def __init__(self, driver):
        super().__init__(driver)
        
    def create_auditory(self, name=""):
        if self.is_element_clickable(locator=self.locators.SEGMENT_CREATE_EMPTY_LOCATOR):
            self.click(locator=self.locators.SEGMENT_CREATE_EMPTY_LOCATOR)
        elif self.is_element_clickable(locator=self.locators.SEGMENT_CREATE_LOCATOR):
            self.click(locator=self.locators.SEGMENT_CREATE_LOCATOR)

        self.click(locator=self.locators.SEGMENT_SETTING_LOCATOR)
        self.click(locator=self.locators.SEGMENT_ADD_NEW_LOCATOR)
        self.write(locator=self.locators.SEGMENT_NAME_LOCATOR, text=name)
        self.click(locator=self.locators.SEGMENT_CREATE_LOCATOR)
    
    def delete_auditory(self, name=""):
        self.click(locator=(By.XPATH, self.locators.SEGMENT_CHOOSE_IN_LIST_PATH.format(name)))
        self.click(locator=self.locators.SEGMENT_ACTIONS_LOCATOR)
        self.click(locator=self.locators.SEGMENT_DELETE_LOCATOR)
