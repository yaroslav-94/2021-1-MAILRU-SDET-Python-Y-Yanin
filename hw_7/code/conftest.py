import os
import signal
import subprocess
import time
from copy import copy

import pytest
import requests
from requests.exceptions import ConnectionError

import settings
from mock import flask_mock
from socket_client.client import SocketClient

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='session')
def config():
    return {}


def __start_waiter(host, port):
    started = False

    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f"Service did not started in 5s on url '{host}:{port}'!")
    else:
        return True


def start_app(config):
    app_path = os.path.join(repo_root, 'app', 'app.py')

    app_out = open(os.path.join(repo_root, 'tmp', 'app_out.txt'), 'w')
    app_err = open(os.path.join(repo_root, 'tmp', 'app_err.txt'), 'w')

    env = copy(os.environ)
    env['APP_HOST'] = settings.APP_HOST
    env['APP_PORT'] = settings.APP_PORT

    env['STUB_HOST'] = settings.STUB_HOST
    env['STUB_PORT'] = settings.STUB_PORT

    env['MOCK_HOST'] = settings.MOCK_HOST
    env['MOCK_PORT'] = settings.MOCK_PORT

    proc = subprocess.Popen(['python3', app_path], stdout=app_out, stderr=app_err, env=env)

    config.app_proc = proc
    config.app_out = app_out
    config.app_err = app_err

    if __start_waiter(host=settings.APP_HOST, port=settings.APP_PORT):
        app_out.writelines(f"App on url '{settings.APP_HOST}:{settings.APP_PORT}' start successfull!")


def start_stub(config):
    stub_path = os.path.join(repo_root, 'stub', 'simple_http_server_stub.py')

    stub_out = open(os.path.join(repo_root, 'tmp', 'stub_out.txt'), 'w')
    stub_err = open(os.path.join(repo_root, 'tmp', 'stub_err.txt'), 'w')

    env = copy(os.environ)
    env['STUB_HOST'] = settings.STUB_HOST
    env['STUB_PORT'] = settings.STUB_PORT

    proc = subprocess.Popen(['python3', stub_path], stdout=stub_out, stderr=stub_err, env=env)

    if __start_waiter(host=settings.STUB_HOST, port=settings.STUB_PORT):
        stub_out.writelines(f"Stub on url '{settings.STUB_HOST}:{settings.STUB_PORT}' start successfull!")

    config.stub_proc = proc
    config.stub_out = stub_out
    config.stub_err = stub_err


def start_mock(config):

    mock_out = open(os.path.join(repo_root, 'tmp', 'mock_out.txt'), 'w')
    mock_err = open(os.path.join(repo_root, 'tmp', 'mock_err.txt'), 'w')

    env = copy(os.environ)
    env['STUB_HOST'] = settings.MOCK_HOST
    env['STUB_PORT'] = settings.MOCK_PORT

    flask_mock.ActionWithMock().run_mock()
    if __start_waiter(host=settings.MOCK_HOST, port=settings.MOCK_PORT):
        mock_out.writelines(f"Mock on url '{settings.MOCK_HOST}:{settings.MOCK_PORT}' start successfull!")

    config.mock_out = mock_out
    config.mock_err = mock_err


@pytest.fixture(scope='function')
def socket_client(config):
    return SocketClient()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        start_mock(config)
        start_stub(config)
        start_app(config)


def stop_app(config):
    config.app_proc.send_signal(signal.SIGINT)
    exit_code = config.app_proc.wait()

    config.app_out.close()
    config.app_err.close()

    assert exit_code == 0


def stop_stub(config):
    config.stub_proc.send_signal(signal.SIGINT)
    config.stub_proc.wait()

    config.stub_out.close()
    config.stub_err.close()


def stop_mock(config):
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')
    config.mock_out.close()
    config.mock_err.close()


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_app(config)
        stop_stub(config)
        stop_mock(config)
