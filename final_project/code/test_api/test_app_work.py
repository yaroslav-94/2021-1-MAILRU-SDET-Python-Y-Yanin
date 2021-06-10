import allure
import pytest
from datetime import datetime

from data.prepare_user import prepare_user_name, prepare_password, prepare_email
from mysql.base_sql import MySQLBase
from test_api.base_api import ApiBase


class TestApiAppState(ApiBase, MySQLBase):

    @pytest.mark.API
    def test_unlock_exist_user(self):
        """
        Test for getting status app
        """
        with allure.step('CREATE USR IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10), start_active_time=datetime.now())
        with allure.step('SEND REQUEST TO APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)
            resp = self.api_client.state_app()
            assert resp.status_code == 200, f"Response return status code {resp.status_code }, expected 200"
            assert resp.json()['status'] == "ok", f"Response return text {resp.text}, expected 'ok'"
