from sqlalchemy.orm import sessionmaker
from data_core.models import Wheat, Corn, Rapeseed

from configuration import engine


def db_session():
    session = sessionmaker(bind=engine)()
    return session


def post_ebm() -> list:
    """ Wheat """
    session = db_session()
    all_res = session.query(Wheat).all()[-1]
    session.close()
    price = all_res.price
    time = all_res.date.strftime('%d-%m-%Y')
    return [price, time]


def post_ema() -> list:
    """ Corn """
    session = db_session()
    all_res = session.query(Corn).all()[-1]
    session.close()
    price = all_res.price
    time = all_res.date.strftime('%d-%m-%Y')
    return [price, time]


def post_eco() -> list:
    """ Rapeseed """
    session = db_session()
    all_res = session.query(Rapeseed).all()[-1]
    session.close()
    price = all_res.price
    time = all_res.date.strftime('%d-%m-%Y')
    return [price, time]
