from mysql.base import MySQLBase
import urllib.parse
from mysql.models import (SumRequests, SumRequestsOnTypes, TopTenMostSendedRequests, TopFiveHavySendedRequests,
                          TopFiveUsersWithServerErrors)


class TestMysqlLoggingSumRequests(MySQLBase):

    def prepare(self):
        dict_protocols = {}
        file = self.read_file()

        for line in file:
            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")

            request_type = arr[5]
            request_url = arr[6]

            if request_type and request_url not in dict_protocols.keys():
                dict_protocols[request_url] = {1}
        file.close()
        self.sum_requests = len(dict_protocols)
        self.mysql_builder.add_sum_requests(sum_requests=len(dict_protocols))

    def test_sum_requests(self):
        mysql_sum = self.mysql.session.query(SumRequests).order_by(SumRequests.id.desc()).first()
        assert self.sum_requests == mysql_sum.sum_requests, f"Data not equal: {self.sum_requests} and {mysql_sum}"


class TestMysqlLoggingSumRequestsOnTypes(MySQLBase):

    def prepare(self):
        file = self.read_file()

        for line in file:
            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")
            request_type = arr[5]
            request_url = arr[6]

            if (10 > len(request_type) > 0) and (request_type not in self.request_types.keys()):
                self.request_types[request_type] = {request_url}
            elif (10 > len(request_type) > 0) and request_type in self.request_types.keys():
                self.request_types[request_type].add(request_url)
        file.close()

        for key, value in self.request_types.items():
            self.mysql_builder.add_sum_requests_on_types(request_type=key, sum_requests=len(value))

    def test_sum_types_requests(self):
        mysql_sum = self.mysql.session.query(SumRequestsOnTypes).order_by(SumRequestsOnTypes.id.desc()).all()
        mysql_data = {
            sql_param.request_type: sql_param.sum_requests for sql_param in mysql_sum
        }

        class_data = {
            key: len(value) for key, value in self.request_types.items()
        }

        assert mysql_data == class_data, f"Data not equal: {class_data} and {mysql_data}"


class TestMysqlLoggingTenMostSendedReqests(MySQLBase):

    def prepare(self):
        top_all_pop_req = {}
        file = self.read_file()
        for line in file:

            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")
            request_url = arr[6]

            if request_url not in top_all_pop_req.keys():
                top_all_pop_req[request_url] = 1
            elif request_url in top_all_pop_req.keys():
                top_all_pop_req[request_url] += 1
        file.close()

        fl = 0
        for w in sorted(top_all_pop_req, key=top_all_pop_req.get, reverse=True):
            if fl < 10:
                self.class_data_top_ten[w] = top_all_pop_req.get(w)
                fl += 1
            else:
                break

        for key, value in self.class_data_top_ten.items():
            self.mysql_builder.add_top_most_sended_requests(url=urllib.parse.unquote(key), sum_requests=value)

    def test_most_sended_requests(self):
        mysql_sum = self.mysql.session.query(TopTenMostSendedRequests).order_by(
            TopTenMostSendedRequests.id.desc()).all()
        mysql_data = {
            sql_param.url: sql_param.sum_requests for sql_param in mysql_sum
        }

        assert mysql_data == self.class_data_top_ten, f"Data not equal: {self.class_data_top_ten} and {mysql_data}"


class TestMysqlLoggingTopFiveHavyRequests(MySQLBase):

    def prepare(self):

        top_all_havy_req = {}
        file = self.read_file()
        for line in file:

            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")

            user_url = arr[0]
            request_url = arr[6]
            request_code = int(arr[8])
            request_size = int(arr[9]) if arr[9].isalnum() else None

            if request_size and request_code:
                if (len(top_all_havy_req) < 5) and (500 > request_code >= 400):
                    top_all_havy_req[request_size] = [request_url, request_code, user_url]
                elif (500 > request_code >= 400) and request_size and request_size >= min(top_all_havy_req.keys()) and \
                        len(top_all_havy_req) == 5:
                    top_all_havy_req.pop(min(top_all_havy_req.keys()))
                    top_all_havy_req[request_size] = [request_url, request_code, user_url]
        file.close()

        fl = 0
        for w in sorted(top_all_havy_req, key=top_all_havy_req.get, reverse=True):
            if fl < 5:
                self.class_data_top_five[w] = top_all_havy_req.get(w)
                fl += 1
            else:
                break

        for key, value in self.class_data_top_five.items():
            self.mysql_builder.add_top_havy_requests(url=urllib.parse.unquote(value[0]), stat_code=value[1],
                                                     req_size=key, user_addr=value[2])

    def test_most_sended_requests(self):
        mysql_sum = self.mysql.session.query(TopFiveHavySendedRequests).order_by(
            TopFiveHavySendedRequests.id.desc()).all()
        mysql_data = {
            sql_param.req_size: [sql_param.url, sql_param.stat_code, sql_param.user_addr]
            for sql_param in mysql_sum
        }

        assert mysql_data == mysql_data, f"Data not equal: {self.class_data_top_five} and {mysql_data}"


class TestMysqlLoggingTopFiveUsersWithServerErrors(MySQLBase):

    def prepare(self):
        top_all_havy_req = {}
        file = self.read_file()
        for line in file:

            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")

            user_url = arr[0]
            request_code = int(arr[8])

            if request_code:
                if (user_url not in top_all_havy_req) and (600 > request_code >= 500):
                    top_all_havy_req[user_url] = 1
                elif user_url in top_all_havy_req and (600 > request_code >= 500):
                    top_all_havy_req[user_url] += 1

        file.close()

        fl = 0
        for w in sorted(top_all_havy_req, key=top_all_havy_req.get, reverse=True):
            if fl < 5:
                self.top_five_users[w] = top_all_havy_req.get(w)
                fl += 1
            else:
                break

        for key, value in self.top_five_users.items():
            self.mysql_builder.add_top_user_with_server_errors(user_addr=key, sum_requests=value)

    def test_most_sended_requests(self):
        mysql_sum = self.mysql.session.query(TopFiveUsersWithServerErrors).order_by(
            TopFiveUsersWithServerErrors.id.desc()).all()
        mysql_data = {
            sql_param.user_addr: sql_param.sum_requests for sql_param in mysql_sum
        }

        assert mysql_data == self.top_five_users, f"Data not equal: {self.top_five_users} and {mysql_data}"
