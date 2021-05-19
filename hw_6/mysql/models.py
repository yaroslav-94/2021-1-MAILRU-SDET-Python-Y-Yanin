from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SumRequests(Base):
    __tablename__ = 'sum_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<SumRequests(number_requests='{self.sum_requests}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sum_requests = Column(Integer, nullable=False)


class SumRequestsOnTypes(Base):
    __tablename__ = 'sum_requests_on_types'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<SumRequestsOnTypes(request_type='{self.request_type}', sum_requests='{self.sum_requests}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_type = Column(String(15), nullable=False)
    sum_requests = Column(Integer, nullable=False)


class TopTenMostSendedRequests(Base):
    __tablename__ = 'top_ten_most_sended_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TopTenMostSendedRequests(url='{self.url}', sum_requests='{self.sum_requests}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200), nullable=False)
    sum_requests = Column(Integer, nullable=False)


class TopFiveHavySendedRequests(Base):
    __tablename__ = 'top_five_havy_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TopFiveHavySendedRequests(" \
               f"url='{self.url}, " \
               f"stat_code='{self.stat_code}'" \
               f"req_size='{self.req_size}'" \
               f"user_addr='{self.user_addr}'" \
               f"')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(250), nullable=False)
    stat_code = Column(Integer, nullable=False)
    req_size = Column(Integer, nullable=False)
    user_addr = Column(String(30), nullable=False)


class TopFiveUsersWithServerErrors(Base):
    __tablename__ = 'top_five_user_with_server_errors'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TopFiveUsersWithServerErrors(url='{self.user_addr}', sum_requests='{self.sum_requests}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_addr = Column(String(30), nullable=False)
    sum_requests = Column(Integer, nullable=False)
