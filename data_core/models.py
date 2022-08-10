from sqlalchemy import Integer, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from configuration import engine

Base = declarative_base()


class Wheat(Base):
    __tablename__ = 'Wheat_price'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    date = Column(DateTime, default=datetime.now)


class Corn(Base):
    __tablename__ = 'Corn_price'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    date = Column(DateTime, default=datetime.now)


class Rapeseed(Base):
    __tablename__ = 'Rapeseed_price'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    date = Column(DateTime, default=datetime.now)

