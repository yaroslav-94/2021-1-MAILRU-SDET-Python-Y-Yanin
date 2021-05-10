from hw_6.mysql.base import MySQLBase
from hw_6.mysql.models import SumRequests, SumRequestsOnTypes, TopTenMostSendedRequests, TopFiveHavySendedRequests, \
    TopFiveUsersWithServerErrors


class TestMysqlLoggingSumRequests(MySQLBase):
    dict_protocols = {}
    sum_requests = 0

    def prepare(self):
        file = self.read_file()
        for line in file:
            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")

            request_type = arr[5]
            request_url = arr[6]

            if request_type and request_url not in self.dict_protocols.keys():
                self.dict_protocols[request_url] = {1}
        file.close()
        self.sum_requests = len(self.dict_protocols)
        self.mysql_builder.add_sum_requests(sum_requests=len(self.dict_protocols))

    def test_sum_requests(self):
        mysql_sum = self.mysql.session.query(SumRequests).order_by(SumRequests.id.desc()).first()
        assert self.sum_requests == mysql_sum.sum_requests, f"Data not equal: {self.sum_requests} and {mysql_sum}"


class TestMysqlLoggingSumRequestsOnTypes(MySQLBase):
    request_types = {}

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

        assert mysql_data == class_data


class TestMysqlLoggingTenMostSendedReqests(MySQLBase):
    top_all_pop_req = {}
    class_data_top_ten = {}

    def prepare(self):
        file = self.read_file()
        for line in file:

            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")
            request_url = arr[6]

            if request_url not in self.top_all_pop_req.keys():
                self.top_all_pop_req[request_url] = 1
            elif request_url in self.top_all_pop_req.keys():
                self.top_all_pop_req[request_url] += 1
        file.close()

        fl = 0
        for w in sorted(self.top_all_pop_req, key=self.top_all_pop_req.get, reverse=True):
            if fl < 11:
                self.class_data_top_ten[w] = self.top_all_pop_req.get(w)
                fl += 1
            else:
                break

        for key, value in self.class_data_top_ten.items():
            self.mysql_builder.add_top_most_sended_requests(url=key, sum_requests=value)

    def test_most_sended_requests(self):
        mysql_sum = self.mysql.session.query(TopTenMostSendedRequests).order_by(TopTenMostSendedRequests.id.desc()).all()
        mysql_data = {
            sql_param.url: sql_param.sum_requests for sql_param in mysql_sum
        }

        assert mysql_data == self.class_data_top_ten


class TestMysqlLoggingTopFiveHavyRequests(MySQLBase):
    top_all_havy_req = {}
    class_data_top_five = {}

    def prepare(self):

        file = self.read_file()
        for line in file:

            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")

            user_url = arr[0]
            request_url = arr[6]
            request_code = int(arr[8])
            request_size = int(arr[9]) if arr[9].isalnum() else None

            if request_size and request_code:
                if (len(self.top_all_havy_req) < 5) and (500 > request_code >= 400):
                    self.top_all_havy_req[request_size] = [request_url, request_code, user_url]
                elif (500 > request_code >= 400) and request_size and request_size >= min(self.top_all_havy_req.keys()) and \
                        len(self.top_all_havy_req) == 5:
                    self.top_all_havy_req.pop(min(self.top_all_havy_req.keys()))
                    self.top_all_havy_req[request_size] = [request_url, request_code, user_url]
        file.close()

        fl = 0
        for w in sorted(self.top_all_havy_req, key=self.top_all_havy_req.get, reverse=True):
            if fl < 11:
                self.class_data_top_five[w] = self.top_all_havy_req.get(w)
                fl += 1
            else:
                break

        for key, value in self.class_data_top_five.items():
            self.mysql_builder.add_top_havy_requests(url=value[0], stat_code=value[1], req_size=key, user_addr=value[2])

    def test_most_sended_requests(self):
        mysql_sum = self.mysql.session.query(TopFiveHavySendedRequests).order_by(TopFiveHavySendedRequests.id.desc()).all()
        mysql_data = {
            sql_param.req_size: [sql_param.url, sql_param.stat_code, sql_param.user_addr]
            for sql_param in mysql_sum
        }

        assert mysql_data == mysql_data


class TestMysqlLoggingTopFiveUsersWithServerErrors(MySQLBase):
    top_five_users = {}

    def prepare(self):

        file = self.read_file()
        for line in file:

            arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")

            user_url = arr[0]
            request_code = int(arr[8])

            if request_code:
                if (user_url not in self.top_five_users) and (600 > request_code >= 500):
                    self.top_five_users[user_url] = 1
                elif user_url in self.top_five_users and (600 > request_code >= 500):
                    self.top_five_users[user_url] += 1

        file.close()

        for key, value in self.top_five_users.items():
            self.mysql_builder.add_top_user_with_server_errors(user_addr=key, sum_requests=value)

    def test_most_sended_requests(self):
        mysql_sum = self.mysql.session.query(TopFiveUsersWithServerErrors).order_by(TopFiveUsersWithServerErrors.id.desc()).all()
        mysql_data = {
            sql_param.user_addr: sql_param.sum_requests for sql_param in mysql_sum
        }

        assert mysql_data == self.top_five_users


