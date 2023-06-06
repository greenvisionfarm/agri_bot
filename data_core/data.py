import requests
from datetime import datetime, timedelta

class ApiData:
    main_url = 'https://ec.europa.eu/agrifood/api'
    begin_date = (datetime.now() - timedelta(days=60)).strftime("%d/%m/%Y")

    def get_product_prices(self, product: str) -> list:
        """ Product Type """
        if product == 'BLTPAN' or product == 'MAI':
            product_type = 'cereal'
        else:
            product_type = 'oilseeds'

        """ Make a Request """
        url = f'{self.main_url}/{product_type}/prices?beginDate={self.begin_date}&'

        if product_type == 'cereal':
            request_url = f'{url}productCodes={product}'
            response = requests.get(request_url).json()
            return response
        if product_type == 'oilseeds':
            request_url = f'{url}products={product}'
            response = requests.get(request_url).json()
            return response

    def data_processing(self, product_name: str) -> str:
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

        product_group = self.get_product_prices(product_name)
        price = sum([float(i['price'][1:].replace(',', '.')) for i in product_group])
        price = format(price /  len(product_group), ".2f")
        # <--- Change to mean

        return price

    @staticmethod
    def validation_of_incoming_data(data: str):
        products = ['Pšenica', 'Kukurica', 'Raps']

        data = data.split(' ')
        first_letter = data[0]

        if first_letter not in products:
            return False
        elif len(data) == 1:
            return data
        elif len(data) == 2 and data[1] == 'graf':
            return data
        return False