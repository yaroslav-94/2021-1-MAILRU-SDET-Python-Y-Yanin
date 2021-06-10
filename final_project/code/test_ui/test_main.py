import allure
import pytest
from datetime import datetime

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from data.prepare_user import prepare_user_name, prepare_password, prepare_email
from mysql.base_sql import MySQLBase
from mysql.models import DataBaseUsers
from test_ui.base_ui import BaseUICase


class TestAuthorization(BaseUICase, MySQLBase):
    """
    This class contains tests for authorization page
    There are 16 test-cases
    """

    @pytest.mark.UI
    def test_logout(self):
        """
        This test create new user in data base, successfully registers and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name).all()
            assert mysql_data[0].active == 0, 'User not active in app but active in DataBase'
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_what_api(self):
        """
        This test create new user in data base, successfully registers, click on text 'What is an API?' in main menu,
        switch to new window and after go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('CLICK ON IMAGE WITH TEXT ABOVE What is an API?'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            window_before = main_page.driver.current_window_handle
            main_page.click(main_page.locators.MAIN_WHAT_API_URL_LOC)

        with allure.step('CLOSE WINDOW WITH INFO ABOUT API'):
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://en.wikipedia.org/wiki/API"
            main_page.driver.close()

        with allure.step('GO BACK TO APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_future_internet(self):
        """
        This test create new user in data base, successfully registers, click on text 'Future of internet' in main menu,
        switch to new window and after go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('CLICK ON IMAGE WITH TEXT ABOVE Future of internet'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_FUTURE_LOC)
            window_before = main_page.driver.current_window_handle
            main_page.click(main_page.locators.MAIN_FUTURE_URL_LOC)

        with allure.step('CLOSE WINDOW WITH TEXT ABOUT FUTURE OF INTERNET'):
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"
            main_page.driver.close()

        with allure.step('GO BACK TO APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_smtp(self):
        """
        This test create new user in data base, successfully registers, click on text 'Lets talk about SMTP?' in main
        menu, switch to new window and after go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('CLICK ON IMAGE WITH TEXT ABOVE Lets talk about SMTP?'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_SMTP_LOC)
            window_before = main_page.driver.current_window_handle
            main_page.click(main_page.locators.MAIN_SMTP_URL_LOC)

        with allure.step('CLOSE WINDIW WITH INFO ABOUT SMTP'):
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://ru.wikipedia.org/wiki/SMTP"
            main_page.driver.close()

        with allure.step('GO BACK TO APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_network_news(self):
        """
        This test create new user in data base, successfully registers, click on label 'Network' in main menu,
        choose 'NEWS' and switch to new window and after go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('OPEN MENU Network'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_NETWORK_MENU_LOC)
            window_before = main_page.driver.current_window_handle
            main_page.click(main_page.locators.MAIN_NETWORK_MENU_LOC)

        with allure.step('GO TO NEWS'):
            main_page.click(main_page.locators.MAIN_NETWORK_NEWS_LOC)
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://www.wireshark.org/news/"
            main_page.driver.close()

        with allure.step('GO BACK TO APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_network_download(self):
        """
        This test create new user in data base, successfully registers, click on label 'Network' in main menu,
        choose 'DOWNLOAD' and switch to new window and after go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('OPEN MENU Network'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_NETWORK_MENU_LOC)
            window_before = main_page.driver.current_window_handle
            main_page.click(main_page.locators.MAIN_NETWORK_MENU_LOC)

        with allure.step('GO TO DOWNLOADS'):
            main_page.click(main_page.locators.MAIN_NETWORK_DOWNLOAD_LOC)
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://www.wireshark.org/#download"
            main_page.driver.close()

        with allure.step('LOGOUT IA APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_network_examples(self):
        """
        This test create new user in data base, successfully registers, click on label 'Network' in main menu,
        choose 'EXAMPLES' and switch to new window and after go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('OPEN MENU Network'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_NETWORK_MENU_LOC)
            window_before = main_page.driver.current_window_handle
            main_page.click(main_page.locators.MAIN_NETWORK_MENU_LOC)

        with allure.step('GO TO EXAMPLES'):
            main_page.click(main_page.locators.MAIN_NETWORK_TCPDUMP_LOC)
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://hackertarget.com/tcpdump-examples/"
            main_page.driver.close()

        with allure.step('LOGOUT IA APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_linux_download_error(self):
        """
        This test create new user in data base, successfully registers, click on label 'Linux' in main menu,
        choose 'Download Centos7' and switch to new window and open page with Fedora - it is bug
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('OPEN MENU Linux'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_LINUX_MENU_LOC)
            window_before = main_page.driver.current_window_handle
            main_page.click(main_page.locators.MAIN_LINUX_MENU_LOC)

        with allure.step('GO TO DOWNLOAD CENTOS 7'):
            main_page.click(main_page.locators.MAIN_LINUX_CENTOS_LOC)
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://www.centos.org/download/", \
                f'Url in is not correct. Expected https://www.centos.org/download/, given {main_page.driver.current_url}'
            main_page.driver.close()

        with allure.step('LOGOUT IA APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_home_button(self):
        """
        This test create new user in data base, successfully registers, click on label 'HOME' in main menu,
        go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('CLICK ON HOME BUTTON'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_HOME_LOC)
            main_page.click(main_page.locators.MAIN_HOME_LOC)
            assert main_page.find(main_page.locators.MAIN_HOME_LOC)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_python_menu_tab_error(self):
        """
        This test create new user in data base, successfully registers, click on label 'Python' in main menu,
        after opened new window and this is bug
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('OPEN MENU Python'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_PYTHON_MENU_LOC)
            window_before = main_page.driver.current_window_handle
            main_page.click(main_page.locators.MAIN_PYTHON_MENU_LOC)
            assert self.login_page.driver.current_url == "http://0.0.0.0:8095/welcome/", "Menu tab 'Python' open window"

        with allure.step('GO TO Python history'):
            main_page.click(main_page.locators.MAIN_PYTHON_HISTORY_LOC)
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://en.wikipedia.org/wiki/History_of_Python"
            main_page.driver.close()

        with allure.step('LOGOUT IA APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_python_history(self):
        """
        This test create new user in data base, successfully registers, hovers the mouse over the label 'Python' in main
        menu, choose 'Python history' and switch to new window and after go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('OPEN MENU Python'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_PYTHON_MENU_LOC)
            search_python = main_page.find(main_page.locators.MAIN_PYTHON_MENU_LOC)
            ActionChains(main_page.driver).move_to_element(search_python).perform()

        with allure.step('GO TO Python history'):
            main_page.click(main_page.locators.MAIN_PYTHON_HISTORY_LOC)
            assert main_page.driver.current_url == "https://en.wikipedia.org/wiki/History_of_Python"

        with allure.step('LOGOUT IA APP'):
            main_page.driver.back()

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_python_flask(self):
        """
        This test create new user in data base, successfully registers, hovers the mouse over the label 'Python' in main
        menu, choose 'Python flask' and switch to new window and after go back to app, success exits in end
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)

        with allure.step('OPEN MENU Python'):
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find(main_page.locators.MAIN_PYTHON_MENU_LOC)
            window_before = main_page.driver.current_window_handle
            search_python = main_page.find(main_page.locators.MAIN_PYTHON_MENU_LOC)
            ActionChains(main_page.driver).move_to_element(search_python).perform()

        with allure.step('GO TO About flask'):
            main_page.click(main_page.locators.MAIN_PYTHON_FLASK_LOC)
            main_page.driver.switch_to_window(main_page.driver.window_handles[1])
            assert main_page.driver.current_url == "https://flask.palletsprojects.com/en/1.1.x/#"
            main_page.driver.close()

        with allure.step('LOGOUT IA APP'):
            main_page.driver.switch_to_window(window_before)

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_username_in_page(self):
        """
        This test create new user in data base, successfully registers, compare username and after exit
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)

        with allure.step('COMPARE USERNAME'):
            assert main_page.find((By.XPATH, f"//li[text()='Logged as {user_name}']")), 'Names not equal'

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_access_loged_user(self):
        """
        This test create new user in data base, successfully registers, access param =0, refresh window and find msg
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=10)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)

        with allure.step('ACCESS PARAM == 0'):
            self.mysql_builder.change_access_param_user(user_name=user_name)
            main_page.driver.refresh()
            assert main_page.find((By.XPATH, "//div[text()='This page is available only to authorized users']"))

    @pytest.mark.UI
    def test_find_vk_id(self):
        """
        This test create new user in data base, successfully registers, find correct vk_id and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=7)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.find((By.XPATH, "//li[text()='VK ID: 12345']"))

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name).all()
            assert mysql_data[0].active == 0, 'User not active in app but active in DataBase'
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)

    @pytest.mark.UI
    def test_not_find_vk_id(self):
        """
        This test create new user in data base, successfully registers, not find correct vk_id and exits
        """
        with allure.step('CREATE USER IN DATABASE'):
            user_name = prepare_user_name(length=9)
            user_pass = prepare_password(length=10)
            self.mysql_builder.add_user_in_base(user_name=user_name, user_pass=user_pass, access=1,
                                                email=prepare_email(length=10), active=0,
                                                start_active_time=datetime.now())

        with allure.step('LOGIN IN APP'):
            self.login_page.login(user_login=user_name, user_password=user_pass)
            main_page = self.login_page.go_to_main()
            assert main_page.find(main_page.locators.MAIN_WHAT_API_LOC)
            assert main_page.is_element_empty((By.XPATH, "//li[text()='VK ID: 12345']"))

        with allure.step('LOGOUT IA APP'):
            main_page.click(main_page.locators.MAIN_LOGOUT_LOC)
            mysql_data = self.mysql_client.session.query(DataBaseUsers).order_by(DataBaseUsers.id.desc()).filter_by(
                username=user_name).all()
            assert mysql_data[0].active == 0, 'User not active in app but active in DataBase'
            assert main_page.find(self.login_page.locators.LOG_ENTRY_LOC)
