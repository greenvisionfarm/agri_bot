import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuration import URL
from data_core.models import Wheat, Corn, Rapeseed

engine = create_engine('sqlite:///../agri_bot.db')


def change_to_int(x) -> int:
    x = int(x.split(',')[0])
    return x


def get_json(link: str) -> dict:
    all_res = requests.get(link).json()
    return all_res


def save_to_db(obj):
    session = sessionmaker(bind=engine)
    s = session()
    s.add(obj)
    s.commit()


def request_ebm():
    """ Wheat """
    all_res = get_json(URL)
    ebm = all_res['data'][0]
    price = change_to_int(ebm['value'])
    new_value = Wheat(price=price)
    save_to_db(new_value)


def request_ema():
    """ Corn """
    all_res = get_json(URL)
    ebm = all_res['data'][6]
    price = change_to_int(ebm['value'])
    new_value = Corn(price=price)
    save_to_db(new_value)


def request_eco():
    """ Rapeseed """
    all_res = get_json(URL)
    ebm = all_res['data'][10]
    price = change_to_int(ebm['value'])
    new_value = Rapeseed(price=price)
    save_to_db(new_value)
