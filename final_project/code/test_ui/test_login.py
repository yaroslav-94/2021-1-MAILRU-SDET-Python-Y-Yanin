import allure
import pytest
from datetime import datetime
from selenium.webdriver.common.by import By

from data.prepare_user import prepare_user_name, prepare_password, prepare_email
from mysql.base_sql import MySQLBase
from test_ui.base_ui import BaseUICase


class TestAuthorization(BaseUICase, MySQLBase):
    """
    There are 10 test-cases
    """

    @pytest.mark.UI
    def test_login_with_bad_password(self):
        """
        This test create new user in data base, login with wrong password and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=prepare_password(length=10), access=1,
                                                email=prepare_email(length=10), active=0)
        
        with allure.step('LOGIN WITH WRONG PASSWORD'):
            self.login_page.login(user_login=user_name, user_password=prepare_password(length=11))
            assert self.login_page.find((By.XPATH, "//div[text()='Invalid username or password']"))

    @pytest.mark.UI
    def test_success_login(self):
        """
        This test create new user in data base, success login and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)
        with allure.step('SUCCESS LOGIN'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            assert self.login_page.find((By.XPATH, "//div[text()='What is an API?']"))

    @pytest.mark.UI
    def test_short_user_name_error(self):
        """
        This test create new user in data base, login with short username and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=3)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10))
        with allure.step("LOGIN WITH SHORT USER NAME"):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            assert self.login_page.driver.current_url == "http://0.0.0.0:8095/welcome/", \
                'Can not authorize registed user '

    @pytest.mark.UI
    def test_long_user(self):
        """
        This test create new user in data base, login with long username and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=16)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1, active=0,
                                                email=prepare_email(length=10))
        
        with allure.step('LOGIN WITH LONG USER NAME'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            assert self.login_page.find((By.XPATH, "//div[text()='What is an API?']"))

    @pytest.mark.UI
    def test_no_access_user(self):
        """
        This test create new user in data base, login as user with no access and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=16)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=0, active=0,
                                                email=prepare_email(length=10))
        
        with allure.step('LOGIN AS USER WITH NO ACCESS'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            assert self.login_page.find((By.XPATH, "//div[text()='Ваша учетная запись заблокирована']"))

    @pytest.mark.UI
    def test_go_to_registration(self):
        """
        This test go to registration url
        """
        with allure.step('CLICK ON REGISTRATION URL'):
            self.login_page.click(self.login_page.locators.LOG_REGISTRATION_LOC, timeout=3)
            assert self.login_page.find((By.XPATH, "//h3[text()='Registration']"))

    @pytest.mark.UI
    def test_no_login(self):
        """
        This test create new user in data base, login with empty userlogin and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=prepare_user_name(length=10), user_pass=user_pass, access=0,
                                                email=prepare_email(length=10), active=0)
        with allure.step('LOGIN WITH EMPTY USERLOGIN'):
            self.login_page.login(user_login=None, user_password=user_pass)
            assert self.login_page.find(self.login_page.locators.LOG_WELCOME_LABEL_LOC).is_displayed()

    @pytest.mark.UI
    def test_no_pass(self):
        """
        This test create new user in data base, login with empty password and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=prepare_password(length=10), access=0,
                                                email=prepare_email(length=10), active=0)

        with allure.step('LOGIN WITH EMPTY USERLOGIN'):
            self.login_page.login(user_login=user_name, user_password=None)
            assert self.login_page.find(self.login_page.locators.LOG_WELCOME_LABEL_LOC).is_displayed()

    @pytest.mark.UI
    def test_no_pass_no_login(self):
        """
        This test create new user in data base, login with empty password and name and exits
        """
        with allure.step('LOGIN WITH EMPTY PASSWORD AND NAME'):
            self.login_page.login()
            assert self.login_page.find(self.login_page.locators.LOG_WELCOME_LABEL_LOC).is_displayed()

    @pytest.mark.UI
    def test_incorrect_user_name_error(self):
        """
        This test create new user in data base, login with incorrect username and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10, is_bad_sym=True)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0)

        with allure.step('LOGIN WITH INCORRECT NAME'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            assert self.login_page.driver.current_url != "http://0.0.0.0:8095/welcome/", \
                'App authorize user with wrong name'
