from datetime import datetime
import matplotlib.pyplot as plt
from data_core.post_data import data_processing

plt.style.use('seaborn-whitegrid')

def create_graf(product_name: str) -> None:
    """ Creating Data-set """
    data = data_processing(product_name)
    prices = [day_price[0] for day_price in data]
    dates = [datetime.strptime(day_price[1], '%d/%m/%Y') for day_price in data]

    """ Creating Graph """
    fig, ax = plt.subplots()
    ax.plot(dates, prices)
    fig.savefig(f'./data/{product_name}_graf.png')
