import requests
from datetime import datetime, timedelta
from constants import main_constants


class ApiData:
    def __init__(self):
        self.begin_date = (datetime.now() - timedelta(days=60)).strftime("%d/%m/%Y")

    def get_product_prices(self, product: str) -> list:
        """ Product Type """
        product_type = main_constants.products_groups[product]
        url = f'{main_constants.main_url}/{product_type}/prices?beginDate={self.begin_date}&memberStateCodes=SK&'
        if product_type == main_constants.cereal:
            request_url = f'{url}productCodes={product}'
        else:
            request_url = f'{url}products={product}'

        response = requests.get(request_url).json()
        return response

    def data_processing(self, product_name: str) -> list:
        """ Working with data """
        product_name = main_constants.products_dict[product_name]
        product_group = self.get_product_prices(product_name)[0]

        product_group = [product_group['price'], product_group['beginDate']]
        product_group[0] = product_group[0].replace(',', '.')

        return product_group

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