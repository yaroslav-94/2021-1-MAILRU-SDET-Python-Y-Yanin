import os
import allure
import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from ui.pages.login_page import LoginPage
from _pytest.fixtures import FixtureRequest


@pytest.fixture(scope='function')
def driver(config, test_dir, request: FixtureRequest):
    mark_test = request.node.get_closest_marker('UI')

    if mark_test is not None:
        url = config['url']
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")

        manager = ChromeDriverManager(version='latest')
        browser = webdriver.Chrome(executable_path=manager.install(), options=options)
        browser.get(url)
        browser.implicitly_wait(15)
        browser.maximize_window()
        yield browser
        browser.quit()
    else:
        yield 0


@pytest.fixture(scope='function')
def login_page(driver):
    if driver:
        return LoginPage(driver=driver)


@pytest.fixture(scope='function')
def registration_page(login_page):
    return login_page.go_to_registration()


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):

    if driver:
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
    else:
        yield 0
