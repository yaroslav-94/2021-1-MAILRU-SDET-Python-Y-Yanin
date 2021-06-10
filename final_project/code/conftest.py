import logging
import shutil
import sys

from api.client_base import ApiClient
from mysql.client import MysqlClient
from ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--url', default='http://0.0.0.0:8095/')


@pytest.fixture(scope='function')
def api_client(config):
    return ApiClient(config['url'])


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    return {'url': url}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_test_dir = 'C:\\tests'
    else:
        base_test_dir = '/tmp/tests'

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir, exist_ok=True)

    if not hasattr(config, 'workerinput'):
        mysql_client = MysqlClient(user='root', password='pass', db_name='FINAL_PROJECT')
        mysql_client.recreate_db()

        mysql_client.connect()
        mysql_client.create_all_data_bases()

        mysql_client.connection.close()

    config.base_test_dir = base_test_dir


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir, exist_ok=True)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='root', password='pass', db_name='FINAL_PROJECT')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()
