from database import Base
from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, func
from sqlalchemy.schema import Sequence

class Test(Base):
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True)
    thing = Column(String(5), unique=True, nullable=True)

class User(Base):
    __tablename__ = 'users'
    field_seq = Sequence('groups_field_seq')
    id = Column(Integer, field_seq, server_default=field_seq.next_value())
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), unique=False, nullable=False)
    birthday = Column(Date(), unique=False, nullable=False)
    create_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
