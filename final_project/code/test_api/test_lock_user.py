import allure
import pytest
from datetime import datetime

from data.prepare_user import prepare_user_name, prepare_password, prepare_email
from mysql.base_sql import MySQLBase
from mysql.models import DataBaseUsers
from test_api.base_api import ApiBase


class TestApiLockUser(ApiBase, MySQLBase):
    """
    There are 4 test-cases
    """

    @pytest.mark.API
    @allure.severity(allure.severity_level.CRITICAL)
    def test_lock_exist_user(self):
        """
        Test to lock secondary user by main
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10))

        with allure.step('CREATE SECONDARY USER IN DB'):
            user_name_new = prepare_user_name(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name_new, user_pass=prepare_password(length=11),
                                                access=1, email=prepare_email(length=11), active=0)

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('LOCK SECONDARY USER'):
            resp = self.api_client.lock_user(user_name=user_name_new)

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name_new).all()

            assert mysql_data[0].access == 0, f"User '{user_name_new}' do not lock"
            assert resp.status_code == 400, f"Response return status code {resp.status_code }, expected 400"

    @pytest.mark.API
    def test_lock_login_user(self):
        """
        Test to lock main user
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)
        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('LOCK MAIN USER'):
            resp = self.api_client.lock_user(user_name=user_name)

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name).all()

            assert mysql_data[0].access == 0, f"User '{user_name}' do not lock"
            assert resp.status_code == 200, f"Response return status code {resp.status_code}, expected 200"

    @pytest.mark.API
    def test_lock_non_existent_user(self):
        """
        Test to lock not created user in DB
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)
        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('LOCK NOT CREATED USER'):
            resp = self.api_client.lock_user(user_name=prepare_user_name(length=11))

            assert resp.status_code == 404, f"Response return status code {resp.status_code}, expected 404"

    @pytest.mark.API
    def test_lock_empty_name(self):
        """
        Test to lock empty user
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)
        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('LOCK EMPTY USER'):
            resp = self.api_client.lock_user(user_name=None)

            assert resp.status_code == 404, f"Response return status code {resp.status_code}, expected 404"
