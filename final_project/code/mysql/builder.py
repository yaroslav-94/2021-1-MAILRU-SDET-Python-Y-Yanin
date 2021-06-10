from datetime import datetime

from sqlalchemy import update

from mysql.models import DataBaseUsers


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

    def add_user_in_base(self, user_name, user_pass, email, access, active, start_active_time=datetime.now()):
        add_user = DataBaseUsers(username=user_name, password=user_pass, email=email, access=access, active=active,
                                 start_active_time=start_active_time)

        self.client.session.add(add_user)
        self.client.session.commit()
        return add_user

    def change_access_param_user(self, user_name):
        if user_name is not None:
            com = update(DataBaseUsers).where(DataBaseUsers.username == f'{user_name}').values(access=0)
            self.client.session.execute(com)
            self.client.session.commit()
