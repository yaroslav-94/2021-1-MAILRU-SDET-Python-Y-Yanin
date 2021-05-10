from hw_6.mysql.models import SumRequests, SumRequestsOnTypes, TopTenMostSendedRequests, TopFiveHavySendedRequests, \
    TopFiveUsersWithServerErrors


class BadDataForAddingInMySQL(Exception):
    pass


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    @staticmethod
    def __error_raiser(model, bad_value, column):
        raise BadDataForAddingInMySQL(f"Bad entry value '{bad_value}' for model '{model}' for column '{column}'")

    def prepare_int_value(self, model, value, column):

        if value and isinstance(value, int):
            return value
        else:
            self.__error_raiser(model=model, bad_value=value, column=column)

    def prepare_str_value(self, model, value, column, max_len):

        if value and isinstance(value, str) and len(value) <= max_len:
            return value
        else:
            self.__error_raiser(model=model, bad_value=value, column=column)

    def add_sum_requests(self, sum_requests):

        add_sum_req = self.prepare_int_value(model='SumRequests', value=sum_requests, column='sum_requests')
        sum_log_requests = SumRequests(sum_requests=add_sum_req)

        self.client.session.add(sum_log_requests)
        self.client.session.commit()
        return sum_log_requests

    def add_sum_requests_on_types(self, request_type, sum_requests):

        add_req_type = self.prepare_str_value(model='SumRequestsOnTypes', value=request_type, column='request_type',
                                              max_len=15)
        add_sum_req = self.prepare_int_value(model='SumRequestsOnTypes', value=sum_requests, column='sum_requests')
        add_request_type = SumRequestsOnTypes(request_type=add_req_type, sum_requests=add_sum_req)

        self.client.session.add(add_request_type)
        self.client.session.commit()
        return add_request_type

    def add_top_most_sended_requests(self, url, sum_requests):

        add_top_send_url = self.prepare_str_value(model='TopTenMostSendedRequests', value=url, column='url',
                                                  max_len=200)
        add_top_send_sum = self.prepare_int_value(model='TopTenMostSendedRequests', value=sum_requests,
                                                  column='sum_requests')
        add_top_sended = TopTenMostSendedRequests(url=add_top_send_url, sum_requests=add_top_send_sum)

        self.client.session.add(add_top_sended)
        self.client.session.commit()
        return add_top_sended

    def add_top_havy_requests(self, url, stat_code, req_size, user_addr):

        add_top_havy_url = self.prepare_str_value(model='TopFiveHavySendedRequests', value=url, column='url',
                                                  max_len=250)
        add_top_havy_code = self.prepare_int_value(model='TopFiveHavySendedRequests', value=stat_code,
                                                   column='stat_code')
        add_top_havy_size = self.prepare_int_value(model='TopFiveHavySendedRequests', value=req_size,
                                                   column='req_size')
        add_top_havy_addr = self.prepare_str_value(model='TopFiveHavySendedRequests', value=user_addr,
                                                   column='user_addr', max_len=30)
        add_top_havy = TopFiveHavySendedRequests(url=add_top_havy_url, stat_code=add_top_havy_code,
                                                 req_size=add_top_havy_size, user_addr=add_top_havy_addr)

        self.client.session.add(add_top_havy)
        self.client.session.commit()
        return add_top_havy

    def add_top_user_with_server_errors(self, user_addr, sum_requests):

        add_top_user_addr = self.prepare_str_value(model='TopFiveUsersWithServerErrors', value=user_addr,
                                                   column='user_addr', max_len=30)
        add_top_user_sum = self.prepare_int_value(model='TopFiveUsersWithServerErrors', value=sum_requests,
                                                  column='sum_requests')
        add_top_user = TopFiveUsersWithServerErrors(user_addr=add_top_user_addr, sum_requests=add_top_user_sum)

        self.client.session.add(add_top_user)
        self.client.session.commit()
        return add_top_user
