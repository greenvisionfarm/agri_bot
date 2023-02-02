# from datetime import datetime

from configuration import main_url, begin_date, end_date
from data_core.get_data import get_product_prices


def data_processing(product_name: str) -> list:
    """
        Working with data

        price = float(product['price'][1:].replace(',', '.'))
        date = product['beginDate']
        # date = datetime.strptime(product['beginDate'], '%d/%m/%Y')
    """
    if product_name == 'Pšenica':
        product_name = 'BLTPAN'
    elif product_name == 'Kukurica':
        product_name = 'MAI'
    else:
        product_name = 'Rapeseed'

    product_group = get_product_prices(product_name, main_url, begin_date, end_date)
    result = [[float(product['price'][1:].replace(',', '.')), product['beginDate']] for product in product_group]
    return result



