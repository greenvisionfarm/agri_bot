import requests
from sqlalchemy.orm import sessionmaker
from data_core.models import Wheat, Corn, Rapeseed

from configuration import URL, engine


def get_json(link: str) -> dict:
    all_res = requests.get(link).json()
    return all_res


def save_to_db(obj):
    session = sessionmaker(bind=engine)
    s = session()
    s.add(obj)
    s.commit()


def get_ebm() -> list:
    """ Wheat """
    all_res = get_json(URL)
    ebm = all_res['data'][0]
    price, time = ebm['value'], ebm['time']
    new_value = Wheat(price=price)
    save_to_db(new_value)
    return [price, time]


def get_ema() -> list:
    """ Corn """
    all_res = get_json(URL)
    ema = all_res['data'][6]
    price, time = ema['value'], ema['time']
    new_value = Corn(price=price)
    save_to_db(new_value)
    return [price, time]


def get_eco() -> list:
    """ Rapeseed """
    all_res = get_json(URL)
    eco = all_res['data'][10]
    price, time = eco['value'], eco['time']
    new_value = Rapeseed(price=price)
    save_to_db(new_value)
    return [price, time]
