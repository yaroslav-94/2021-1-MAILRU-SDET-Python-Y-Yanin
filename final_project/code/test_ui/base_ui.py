import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.login_page import LoginPage
from ui.pages.registration_page import RegistrationPage


class BaseUICase:

    is_regis_page = False

    @pytest.fixture(scope='function', autouse=True)
    def setup_ui(self, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.login_page: LoginPage = request.getfixturevalue('login_page')

        if self.is_regis_page:
            self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')
