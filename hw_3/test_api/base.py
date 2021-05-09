import pytest

from hw_3.data_hw3 import LOGIN_EMAIL, LOGIN_PASSWORD


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, segment_api, builder):
        self.api_client = api_client

        if self.authorize:
            self.api_client.authorize(login=LOGIN_EMAIL, password=LOGIN_PASSWORD)
            self.segment_api = segment_api
            self.segment_api.csrf_token = self.api_client.csrf_token
            self.segment_api.session = self.api_client.session
            self.segment_name = builder.create_segment_name("Segment name")
