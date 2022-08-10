import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker

from configuration import engine
from data_core.models import Wheat, Corn, Rapeseed

session = sessionmaker(bind=engine)
plt.style.use('seaborn-whitegrid')


def get_p_t(obj) -> list:
    """ Get price and time """
    price, time = [], []
    for result in obj:
        result_price = int(result.price)
        result_time = str(result.date.date())
        price.append(result_price)
        time.append(result_time)
    return [price, time]


def Wheat_graf():
    s = session()
    results = s.query(Wheat).all()
    s.close()
    results = get_p_t(results)
    time, price = results[1], results[0]
    fig, ax = plt.subplots()
    ax.plot(time, price)
    fig.savefig('png/wheat_graf.png')


def Corn_graf():
    s = session()
    results = s.query(Corn).all()
    s.close()
    results = get_p_t(results)
    time, price = results[1], results[0]
    fig, ax = plt.subplots()
    ax.plot(time, price)
    fig.savefig('png/corn_graf.png')


def Rapeseed_graf():
    s = session()
    results = s.query(Rapeseed).all()
    s.close()
    results = get_p_t(results)
    time, price = results[1], results[0]
    fig, ax = plt.subplots()
    ax.plot(time, price)
    fig.savefig('png/rape_graf.png')
