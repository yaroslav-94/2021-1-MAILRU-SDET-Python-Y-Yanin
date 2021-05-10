import os
import pytest

from hw_6.builder.builder import MySQLBuilder


class MySQLBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)

        self.prepare()

    @staticmethod
    def read_file():
        path = os.path.dirname(os.path.abspath(os.path.join(__file__, "../..")))
        path_to_log_file = path + "/access.log"

        for line in open(path_to_log_file, "r"):
            yield line
