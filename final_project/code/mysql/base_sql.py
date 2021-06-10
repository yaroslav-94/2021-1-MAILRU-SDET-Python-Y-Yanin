import os
import pytest

from mysql.builder import MySQLBuilder


class MySQLBase:

    mysql_client = ''
    mysql_builder = ''

    @pytest.fixture(scope='function', autouse=True)
    def setup_sql(self, mysql_client):
        self.mysql_client = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)

    @staticmethod
    def read_file():
        path = os.path.dirname(os.path.abspath(os.path.join(__file__, "../..")))
        path_to_log_file = path + "/access.log"

        for line in open(path_to_log_file, "r"):
            yield line
