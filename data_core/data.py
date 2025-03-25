import io
import requests
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from data_core import main_constants

# plt.style.use('seaborn-whitegrid')


class ApiData:
    def __init__(self):
        self.url = main_constants.main_url

        self.country = 'SK'
        self.begin_date = self.get_begin_date()

    @staticmethod
    def get_begin_date(days=30):
        return (datetime.now() - timedelta(days=days)).strftime("%d/%m/%Y")

    @staticmethod
    def get_data(request_url):
        response = requests.get(request_url).json()

        if isinstance(response, dict):
            errors = response.get("error", False)
            if errors:
                return [False, False]

        return requests.get(request_url).json()

    def create_requests_url(self, product_type, product, date):
        url = f'{self.url}/{product_type}/prices?beginDate={date}&memberStateCodes={self.country}&'

        if product_type == main_constants.cereal:
            request_url = f'{url}productCodes={product}'
        else:
            request_url = f'{url}products={product}'

        return request_url

    def get_product_prices(self, product: str, **kwargs) -> list:
        """ Product Type """
        product_type = main_constants.products_groups[product]
        date = kwargs.get("date", self.begin_date)
        request_url = self.create_requests_url(product_type, product, date)

        return self.get_data(request_url)

    def data_processing(self, product_name: str) -> list:
        """ Working with data """
        product_name = main_constants.products_dict[product_name]
        product_group = self.get_product_prices(product_name)[0]

        if not product_group:
            date = self.get_begin_date(days=120)
            product_group = self.get_product_prices(product_name, date=date)[0]

            if not product_group:
                return [False, False]

        product_group = [product_group['price'], product_group['beginDate']]
        product_group[0] = product_group[0].replace(',', '.')

        return product_group

    @staticmethod
    def validation_of_incoming_data(data: str):
        data = data.split(' ')
        first_letter = data[0]

        if first_letter not in main_constants.products:
            return False

        elif len(data) == 1 or (len(data) == 2 and data[1] == 'graf'):
            return data

        return False

    @staticmethod
    def change_date_format(date):
        date = date.split("/")
        return "/".join(date[:-1])

    @staticmethod
    def change_price(price):
        return float(price.replace("€", ""))

    def create_graf(self, product_name: str):
        """ Creating Data-set """
        self.begin_date = self.get_begin_date(days=120)
        product_name = main_constants.products_dict[product_name]
        product_group = self.get_product_prices(product_name)

        data_dict = {
            self.change_date_format(value.get('beginDate')): self.change_price(value.get('price'))
            for value in product_group
        }

        if len(data_dict) <= 2:
            return False

        dates, prices = zip(*data_dict.items())
        dates = tuple(reversed(dates))
        prices = tuple(reversed(prices))

        """ Creating Graph """
        png_output = io.BytesIO()
        fig, ax = plt.subplots()
        ax.plot(dates, prices)

        canvas = FigureCanvas(fig)
        canvas.print_png(png_output)

        return png_output.getvalue()
