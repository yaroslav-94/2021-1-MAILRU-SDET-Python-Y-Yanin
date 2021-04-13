import logging

from ui.locators.segment_locators import SegmentLocators
from ui.pages.base_page import BasePage

logger = logging.getLogger('test')


class AuditoryPage(BasePage):
    locators = SegmentLocators()
    url = "https://target.my.com/segments/segments_list"

    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f'{self.__class__.__name__} page is opening...')
        self.is_opened()
