import os
import allure
import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from ui.data_hw2 import LOGIN_EMAIL, LOGIN_PASSWORD
from ui.pages.login_page import LoginPage


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture(scope='function')
def dashboard_page(driver, login_page, user_login=LOGIN_EMAIL, user_password=LOGIN_PASSWORD):
    return login_page.login(user_login=user_login, user_password=user_password)


@pytest.fixture(scope='function')
def driver(config, test_dir):
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
