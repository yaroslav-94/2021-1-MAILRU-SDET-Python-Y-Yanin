import allure
import pytest
from datetime import datetime

from data.prepare_user import prepare_user_name, prepare_password, prepare_email
from mysql.base_sql import MySQLBase
from mysql.models import DataBaseUsers
from test_api.base_api import ApiBase


class TestApiCreateUser(ApiBase, MySQLBase):
    """
    There are 19 test-cases
    """

    @pytest.mark.API
    @pytest.mark.parametrize(
        "user_name_new",
        [prepare_user_name(length=3), prepare_user_name(length=8), prepare_user_name(length=16)],
        ids=['test_with_sort_name', 'test_success_creating', 'test_long_name']
    )
    def test_username_except_db(self, user_name_new):
        """
        Test for validate good data for parameter username for API
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10), start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('CREATE NEW USER FROM MAIN USER IN DB'):
            user_pass_new = prepare_user_name(length=11)
            resp_add = self.api_client.add_user(user_name=user_name_new, user_pass=user_pass_new,
                                                email=prepare_email(length=11))

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name_new).all()

            assert mysql_data[0].password == user_pass_new, \
                f"User '{user_name_new}' with password '{user_pass_new}' not find in DB"
            assert resp_add.status_code == 201, f"Response return status code {resp_add.status_code}, expected 201"

    @pytest.mark.API
    @pytest.mark.parametrize(
        "user_name_new",
        ['', prepare_user_name(length=17), prepare_user_name(is_bad_sym=True, length=10), None],
        ids=['test_empty_name', 'test_longer_name', 'test_bad_symbol_name', 'test_no_name']
    )
    def test_username_not_except_db(self, user_name_new):
        """
        Test for validate bad data for parameter username for API
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10), start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('CREATE NEW USER FROM MAIN USER IN DB'):
            user_pass_new = prepare_user_name(length=11)
            resp_add = self.api_client.add_user(user_name=user_name_new, user_pass=user_pass_new,
                                                email=prepare_email(length=11))

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name_new).all()

            assert not mysql_data, f"User '{user_name_new}' with password '{user_pass_new}' find in DB but is not"
            assert resp_add.status_code == 400, f"Response return status code {resp_add.status_code}, expected 400"

    @pytest.mark.API
    @pytest.mark.parametrize(
        "user_pass_new",
        [prepare_password(length=1), prepare_password(length=11), prepare_password(length=255)],
        ids=['test_short_password', 'test_normal_password', 'test_long_password']
    )
    def test_password_except_db(self, user_pass_new):
        """
        Test for validate good data for parameter password for API
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10), start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('CREATE NEW USER FROM MAIN USER IN DB'):
            user_name_new = prepare_user_name(length=11)
            resp_add = self.api_client.add_user(user_name=user_name_new, user_pass=user_pass_new,
                                                email=prepare_email(length=11))

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name_new).all()

            assert mysql_data[0].password == user_pass_new, \
                f"User '{user_name_new}' with password '{user_pass_new}' not find in DB"
            assert resp_add.status_code == 201, f"Response return status code {resp_add.status_code}, expected 201"

    @pytest.mark.API
    @pytest.mark.parametrize(
        "user_pass_new",
        [None, prepare_password(length=256)],
        ids=['test_no_password', 'test_longer_password']
    )
    def test_password_not_except_db(self, user_pass_new):
        """
        Test for validate bad data for parameter password for API
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10), start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('CREATE NEW USER FROM MAIN USER IN DB'):
            user_name_new = prepare_user_name(length=11)
            resp_add = self.api_client.add_user(user_name=user_name_new, user_pass=user_pass_new,
                                                email=prepare_email(length=11))

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                    username=user_name_new).all()

            assert not mysql_data, f"User '{user_name_new}' with password '{user_pass_new}' find in DB but is not"
            assert resp_add.status_code == 400, f"Response return status code {resp_add.status_code}, expected 400"

    @pytest.mark.API
    @pytest.mark.parametrize(
        "user_email_new",
        [prepare_email(length=8), prepare_email(length=20), prepare_email(length=64)],
        ids=['test_short_email', 'test_normal_email', 'test_long_email']
    )
    def test_email_except_db(self, user_email_new):
        """
        Test for validate good data for parameter email for API
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10), start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('CREATE NEW USER FROM MAIN USER IN DB'):
            user_name_new = prepare_user_name(length=11)
            user_pass_new = prepare_user_name(length=11)
            resp_add = self.api_client.add_user(user_name=user_name_new, user_pass=user_pass_new, email=user_email_new)

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name_new).all()

            assert mysql_data[0].password == user_pass_new, \
                f"User '{user_name_new}' with password '{user_pass_new}' not find in DB"
            assert resp_add.status_code == 201, f"Response return status code {resp_add.status_code}, expected 201"

    @pytest.mark.API
    @pytest.mark.parametrize(
        "user_email_new",
        [None, prepare_password(length=65), prepare_email(no_dog=True, length=10), prepare_email(no_com=True, length=10)],
        ids=['test_no_email', 'test_longer_email', 'test_no_dog_email', 'test_no_point_email']
    )
    def test_email_not_except_db(self, user_email_new):
        """
        Test for validate bad data for parameter email for API
        """
        with allure.step('CREATE MAIN USER IN DB'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10), start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.api_client.login_in_api(user_pass=user_pass, user_name=user_name)

        with allure.step('CREATE NEW USER FROM MAIN USER IN DB'):
            user_name_new = prepare_user_name(length=11)
            user_pass_new = prepare_user_name(length=11)
            resp_add = self.api_client.add_user(user_name=user_name_new, user_pass=user_pass_new, email=user_email_new)

            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name_new).all()

            assert not mysql_data, f"User '{user_name_new}' with password '{user_pass_new}' find in DB but is not"
            assert resp_add.status_code == 400, f"Response return status code {resp_add.status_code}, expected 400"
