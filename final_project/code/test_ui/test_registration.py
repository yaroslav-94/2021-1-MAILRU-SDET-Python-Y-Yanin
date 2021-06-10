from datetime import datetime, timedelta

import allure
import pytest
from selenium.webdriver.common.by import By
from data.prepare_user import prepare_user_name, prepare_password, prepare_email
from mysql.base_sql import MySQLBase
from mysql.models import DataBaseUsers
from test_ui.base_ui import BaseUICase


class TestRegistration(BaseUICase, MySQLBase):
    """
    There are 22 test-cases
    """
    is_regis_page = True
    user_pass_good = prepare_password(length=10)


class TestUsername(TestRegistration):

    @pytest.mark.UI
    def test_empty_user_name(self):
        """
        Test for registration with empty user name
        """
        with allure.step('REGISTRATION WITH EMPTY USERNAME'):
            self.registration_page.registration(user_name=None, user_pass=self.user_pass_good,
                                                email=prepare_email(length=10), rep_pass=self.user_pass_good)
            assert self.registration_page.is_element_empty(self.registration_page.locators.REG_TITLE_LOC)

    @pytest.mark.UI
    def test_registration_short_user_name_error(self):
        """
        Test for registration with short user name
        """
        with allure.step('REGISTRATION WITH SHORT USERNAME. CATCH ERROR'):
            self.registration_page.registration(user_name=prepare_user_name(length=3), user_pass=self.user_pass_good,
                                                email=prepare_email(length=10), rep_pass=self.user_pass_good)
            assert self.login_page.driver.current_url == "http://0.0.0.0:8095/welcome/", \
                'Can not register with good parameters'

    @pytest.mark.UI
    def test_registration_long_user_name(self):
        """
        Test for registration with long user name
        """
        with allure.step('REGISTRATION WITH LONG USERNAME'):
            self.registration_page.registration(user_name=prepare_user_name(length=16), user_pass=self.user_pass_good,
                                                email=prepare_email(length=10), rep_pass=self.user_pass_good)

            assert self.registration_page.find((By.XPATH, "//div[text()='What is an API?']"))

    @pytest.mark.UI
    def test_registration_longer_user_name(self):
        """
        Test for registration with user name more than appruve 16 symbols
        """
        with allure.step('REGISTRATION WITH USERNAME LENGTH >16'):
            self.registration_page.registration(user_name=prepare_user_name(length=17), user_pass=self.user_pass_good,
                                                email=prepare_email(length=10), rep_pass=self.user_pass_good)

            assert self.registration_page.find((By.XPATH, "//div[text()='Incorrect username length']"))

    @pytest.mark.UI
    def test_registration_double_user_name_error(self):
        """
        Test for double registration
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name_double = prepare_user_name(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name_double,
                                                user_pass=self.user_pass_good,
                                                email=prepare_email(length=11),
                                                access=1, active=0, start_active_time=datetime.now())
        with allure.step('REGISTRATION OF AN EXISTING USER. CATCH ERROR'):
            self.registration_page.registration(user_name=user_name_double,
                                                email=prepare_email(length=10),
                                                user_pass=self.user_pass_good, rep_pass=self.user_pass_good)

            assert not self.registration_page.is_element_empty((By.XPATH, "//div[text()='User already exists']")), \
                "Missed 's' in 'exists'"

    @pytest.mark.UI
    def test_registration_bad_user_name_error(self):
        """
        Test for registration with banned symbol in user name
        """
        with allure.step('REGISTRATION WITH BAD SYMBOL IN USERNAME'):
            self.registration_page.registration(user_name=prepare_user_name(length=10, is_bad_sym=True),
                                                user_pass=self.user_pass_good, email=prepare_email(10),
                                                rep_pass=self.user_pass_good)

            assert self.login_page.driver.current_url == "http://0.0.0.0:8095/welcome/", \
                'User with forbidden characters in the name must not be registered'


class TestEmail(TestRegistration):

    @pytest.mark.UI
    def test_registration_no_email(self):
        """
        Test for registration with empty email
        """
        with allure.step('REGISTRATION WITH EMPTY EMAIL'):
            self.registration_page.registration(user_name=prepare_user_name(length=10), user_pass=self.user_pass_good,
                                                rep_pass=self.user_pass_good, email=None)

            assert self.registration_page.find((By.XPATH, "//div[text()='Incorrect email length']"))

    @pytest.mark.UI
    def test_registration_short_email(self):
        """
        Test for registration with short email
        """
        with allure.step('REGISTRATION WITH SHORT EMAIL'):
            self.registration_page.registration(user_name=prepare_user_name(length=10), user_pass=self.user_pass_good,
                                                rep_pass=self.user_pass_good, email=prepare_email(length=8))

            assert self.registration_page.find((By.XPATH, "//div[text()='What is an API?']"))

    @pytest.mark.UI
    def test_registration_long_email(self):
        """
        Test for registration with long email
        """
        with allure.step('REGISTRATION WITH MAX NUMBER SYMBOLS IN EMAIL'):
            self.registration_page.registration(user_name=prepare_user_name(length=10), user_pass=self.user_pass_good,
                                                rep_pass=self.user_pass_good, email=prepare_email(length=64))

            assert self.registration_page.find((By.XPATH, "//div[text()='What is an API?']"))

    @pytest.mark.UI
    def test_registration_longer_email(self):
        """
        Test for registration with email length > 64
        """
        with allure.step('REGISTRATION WITH LEN EMAIL MORE THAN APPRUVED'):
            self.registration_page.registration(user_name=prepare_user_name(10), user_pass=self.user_pass_good,
                                                rep_pass=self.user_pass_good, email=prepare_email(length=65))
            assert self.registration_page.find((By.XPATH, "//div[text()='Incorrect email length']"))

    @pytest.mark.UI
    def test_registration_double_email_error(self):
        """
        Test for double registration
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_email_double = prepare_email(15)
            self.mysql_builder.add_user_in_base(user_name=prepare_user_name(11),
                                                user_pass=self.user_pass_good,
                                                email=user_email_double,
                                                access=1, active=0, start_active_time=datetime.now())
        with allure.step('DOUBLE REGISTRATION'):
            self.registration_page.registration(user_name=prepare_user_name(10),
                                                email=user_email_double,
                                                user_pass=self.user_pass_good, rep_pass=self.user_pass_good)

            assert not self.registration_page.is_element_empty((By.XPATH, "//div[text()='User already exist']")), \
                'The app is unable to process user re-registration!'

    @pytest.mark.UI
    def test_registration_no_dog_email(self):
        """
        Test for registration with email without @
        """
        with allure.step('REGISTRATION WITH NO DOG IN EMAIL'):
            self.registration_page.registration(user_name=prepare_user_name(length=10), user_pass=self.user_pass_good,
                                                rep_pass=self.user_pass_good,
                                                email=prepare_email(no_dog=True, length=12))

            assert self.registration_page.find((By.XPATH, "//div[text()='Invalid email address']"))

    @pytest.mark.UI
    def test_registration_no_com_email(self):
        """
        Test for registration with empty without '.'
        """
        with allure.step('REGISTRATION WITHOUT .COM'):
            self.registration_page.registration(user_name=prepare_user_name(length=10), user_pass=self.user_pass_good,
                                                rep_pass=self.user_pass_good,
                                                email=prepare_email(no_com=True, length=12))

            assert self.registration_page.find((By.XPATH, "//div[text()='Invalid email address']"))


class TestPassword(TestRegistration):

    @pytest.mark.UI
    def test_registration_no_password(self):
        """
        Test for registration with empty password
        """
        with allure.step('REGISTRATION WITHOUT PASSWORD'):
            self.registration_page.registration(user_name=prepare_user_name(length=10), email=prepare_email(length=10),
                                                user_pass=None, rep_pass=None)

            assert self.registration_page.find(self.registration_page.locators.REG_TITLE_LOC)

    @pytest.mark.UI
    def test_registration_short_password(self):
        """
        Test for registration with short password
        """
        with allure.step('REGISTRATION WITH SHORT PASSWORD'):
            new_pass = prepare_password(length=1)
            self.registration_page.registration(user_name=prepare_user_name(length=10), user_pass=new_pass,
                                                rep_pass=new_pass, email=prepare_email(length=10))

            assert self.registration_page.find((By.XPATH, "//div[text()='What is an API?']"))

    @pytest.mark.UI
    def test_registration_long_password(self):
        """
        Test for registration with long password
        """
        with allure.step('REGISTRATION WITH LONG PASSWORD'):
            new_pass = prepare_password(length=255)
            self.registration_page.registration(user_name=prepare_user_name(length=10), user_pass=new_pass,
                                                rep_pass=new_pass, email=prepare_email(length=10))

            assert self.registration_page.find((By.XPATH, "//div[text()='What is an API?']"))

    @pytest.mark.UI
    def test_registration_longer_password_error(self):
        """
        Test for registration with password's len more 255 symbols
        """
        with allure.step('REGISTRATION WITH LONGER PASSWORD'):
            new_pass = prepare_password(length=256)
            self.registration_page.registration(user_name=prepare_user_name(length=10), user_pass=new_pass,
                                                rep_pass=new_pass, email=prepare_email(length=10))

            assert self.registration_page.is_element_exist((By.XPATH, "//div[text()='Incorrect password length']")), \
                'No text message with good answer'


class TestRepeatPassword(TestRegistration):

    @pytest.mark.UI
    def test_registration_empty_repeat_password(self):
        """
        Test for registration with empty repeat password
        """
        with allure.step('REGISTRATION WITH EMPTY REPEATED PASSWORD'):
            self.registration_page.registration(user_name=prepare_user_name(length=10), rep_pass=None,
                                                user_pass=prepare_password(length=10), email=prepare_email(length=10))

            assert self.registration_page.find((By.XPATH, "//div[text()='Passwords must match']"))

    @pytest.mark.UI
    def test_registration_wrong_repeat_password(self):
        """
        Test for registration with wrong repeat password
        """
        with allure.step('REGISTRATION WITH WRONG REPEAT PASSWORD'):
            self.registration_page.registration(user_name=prepare_user_name(length=10),
                                                user_pass=prepare_password(length=10),
                                                email=prepare_email(length=10), rep_pass=prepare_password(length=20))
            assert self.registration_page.find((By.XPATH, "//div[text()='Passwords must match']"))


class TestUnsortedParams(TestRegistration):

    @pytest.mark.UI
    def test_registration_go_to_authorization(self):
        """
        Test for registration for open page login
        """
        with allure.step('GO TO LOGIN'):
            self.registration_page.click(self.registration_page.locators.REG_LOGIN_LOC)
            assert self.registration_page.find((By.XPATH, "//h3[text()='Welcome to the TEST SERVER']"))

    @pytest.mark.UI
    def test_registration_user_with_db_param_active_error(self):
        """
        Test for registration with find error in DB in parameter active
        """
        with allure.step('REGISTRATION AND FIND ERROR IN PARAMETER ACTIVE'):
            user_name = prepare_user_name(8)
            self.registration_page.registration(user_name=user_name, user_pass=self.user_pass_good,
                                                email=prepare_email(length=8), rep_pass=self.user_pass_good)
            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name).all()

            assert mysql_data[0].active == 1, 'User active in app but not in DataBase'
            assert (datetime.strptime(mysql_data[0].start_active_time, '%d/%m/%y %H:%M:%S') >=
                    datetime.now() - timedelta(minutes=1), 'User do not crated in this test-run')

    @pytest.mark.UI
    def test_no_accept_rules(self):
        """
        Test for registration with no accepting rules
        """
        with allure.step('REGISTRATION WITH NO ACCEPT RULSE'):
            self.registration_page.registration(user_name=prepare_user_name(length=10), accept_rule=None,
                                                user_pass=self.user_pass_good, email=prepare_email(length=10),
                                                rep_pass=self.user_pass_good)

            assert self.registration_page.is_element_exist(self.registration_page.locators.REG_TITLE_LOC)
