import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com/')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    return {'url': url}


@pytest.fixture(scope='function')
def driver(config):
    url = config['url']

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    browser = webdriver.Chrome(options=options, executable_path='/home/user/PycharmProjects/chromedriver')
    browser.implicitly_wait(15)
    browser.get(url)
    browser.set_window_size(1400, 1000)

    yield browser

    browser.quit()
