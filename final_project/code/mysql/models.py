from pymysql import NULL
from sqlalchemy import Column, Integer, String, VARCHAR, SMALLINT, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DataBaseUsers(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TestUsers(id='{self.id}', username='{self.username}', password='{self.password}', " \
               f"email='{self.email}', access='{self.access}', active='{self.active}', " \
               f"start_active_time='{self.start_active_time}')>"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(VARCHAR(16), default=NULL, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False, unique=True)
    access = Column(SMALLINT, default=NULL)
    active = Column(SMALLINT, default=NULL)
    start_active_time = Column(DateTime, default=NULL)
