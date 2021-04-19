import logging
import os

from ui.locators.company_locators import CompanyLocators
from ui.pages.base_page import BasePage

logger = logging.getLogger('test')


class CompanyPage(BasePage):
    locators = CompanyLocators()
    url = 'https://target.my.com/dashboard'

    def __init__(self, driver):
        super().__init__(driver)

    def upload_file(self):
        elem = self.find(self.locators.COMPANY_UPLOAD_FILE_LOCATOR)
        path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
        path2 = os.path.join(path, 'download_files', 'photo.jpg')
        elem.send_keys(path2)
