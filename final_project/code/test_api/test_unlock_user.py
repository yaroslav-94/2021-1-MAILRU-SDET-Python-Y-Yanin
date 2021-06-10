import allure
import pytest
from datetime import datetime

from data.prepare_user import prepare_user_name, prepare_password, prepare_email
from mysql.base_sql import MySQLBase
from mysql.models import DataBaseUsers
from test_api.base_api import ApiBase


class TestApiUnlockUser(ApiBase, MySQLBase):
    """
    There are 4 test-cases
    """

    @pytest.mark.API
    @allure.severity(allure.severity_level.CRITICAL)
    def test_unlock_exist_user(self):
        """
        Test for unlock secondary user by main
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)

        with allure.step('CREATE SECONDARY USER IN DB'):
            user_name_new = prepare_user_name(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name_new, user_pass=prepare_password(length=11),
                                                access=0, email=prepare_email(length=11), active=0)

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('UNLOCK SECONDARY USER IN APP'):
            resp = self.api_client.unlock_user(user_name=user_name_new)

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name_new).all()

            assert mysql_data[0].access == 1, f"User '{user_name_new}' not unlock"
            assert resp.status_code == 400, f"Response return status code {resp.status_code }, expected 400"

    @pytest.mark.API
    def test_unlock_login_user(self):
        """
        Test for unlock main user
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('UNLOCK MAIN USER IN APP'):
            resp = self.api_client.unlock_user(user_name=user_name)

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name).all()

            assert mysql_data[0].access == 1, f"User '{user_name}' not unlock"
            assert resp.status_code == 304, f"Response return status code {resp.status_code}, expected 304"

    @pytest.mark.API
    def test_unlock_non_existent_user(self):
        """
        Test for unlock not created user by main user
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('UNLOCK NOT CREATED USER IN APP'):
            resp = self.api_client.unlock_user(user_name=prepare_user_name(length=11))

            assert resp.status_code == 404, f"Response return status code {resp.status_code}, expected 404"

    @pytest.mark.API
    def test_unlock_empty_name(self):
        """
        Test for unlock empty user by main user
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)
        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('UNLOCK NOT EMPTY USER IN APP'):
            resp = self.api_client.unlock_user(user_name=None)

            assert resp.status_code == 404, f"Response return status code {resp.status_code}, expected 404"
