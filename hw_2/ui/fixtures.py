import os
import allure
import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from hw_2.ui.pages.base_page import BasePage
from hw_2.ui.pages.company_page import CompanyPage


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def company_page(driver):
    return CompanyPage(driver=driver)


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    manager = ChromeDriverManager(version='latest')
    browser = webdriver.Chrome(executable_path=manager.install())
    browser.get(url)
    browser.implicitly_wait(15)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)