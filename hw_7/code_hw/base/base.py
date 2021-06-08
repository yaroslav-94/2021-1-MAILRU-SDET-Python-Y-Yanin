import pytest


class ApiBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, socket_client):
        self.socket_client = socket_client
