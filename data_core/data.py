from statistics import mean

import requests
from datetime import datetime, timedelta
from constants import main_constants


class ApiData:
    begin_date = (datetime.now() - timedelta(days=60)).strftime("%d/%m/%Y")

    def get_product_prices(self, product: str) -> list:
        """ Product Type """
        if product == 'BLTPAN' or product == 'MAI':
            product_type = main_constants.cereal
        else:
            product_type = main_constants.oilseeds

        """ Make a Request """
        url = f'{main_constants.main_url}/{product_type}/prices?beginDate={self.begin_date}&'

        if product_type == main_constants.cereal:
            request_url = f'{url}productCodes={product}'
        else:
            request_url = f'{url}products={product}'

        response = requests.get(request_url).json()
        return response

    def data_processing(self, product_name: str) -> str:
        """ Working with data """
        product_name = main_constants.products_dict[product_name]
        product_group = self.get_product_prices(product_name)
        price = mean([float(i['price'][1:].replace(',', '.')) for i in product_group])
        price = format(price, ".2f")

        return price

    @staticmethod
    def validation_of_incoming_data(data: str):
        data = data.split(' ')
        first_letter = data[0]

        if first_letter not in main_constants.products:
            return False
        elif len(data) == 1:
            return data
        elif len(data) == 2 and data[1] == 'graf':
            return data
        return False