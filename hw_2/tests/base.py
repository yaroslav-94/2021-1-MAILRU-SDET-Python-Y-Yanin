import pytest
from _pytest.fixtures import FixtureRequest

from hw_2.ui.pages.base_page import BasePage
from hw_2.ui.pages.company_page import CompanyPage


class BaseCase:

    # authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        #
        # self.login_page: LoginPage = request.getfixturevalue('base_page')
        # if self.authorize:
        #     self.dashboard_page = request.getfixturevalue('dashboard_page')
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.company_page: CompanyPage = request.getfixturevalue('company_page')

        self.logger.debug('Initial setup done!')
