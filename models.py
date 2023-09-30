from database import Base
from sqlalchemy import Column, String, Integer

class Test(Base):
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True)
    thing = Column(String(5), unique=True, nullable=True)
