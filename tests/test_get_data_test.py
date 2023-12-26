import requests
import pytest

from data_core.main_constants import main_url, begin_date, end_date
from data_core.get_data import get_product_prices

class TestGetData:
    @pytest.mark.parametrize('product_name' , ['BLTPAN', 'MAI', 'Rapeseed'])
    def test_api_connection(self, product_name):
        if product_name == 'BLTPAN' or product_name == 'MAI':
            product_type = 'cereal'
        else:
            product_type = 'oilseeds'

        url = f'{main_url}/{product_type}/prices?beginDate={begin_date}&endDate={end_date}&'

        if product_type == 'cereal':
            request_url = f'{url}productCodes={product_name}&marketCodes=BRAT'
            response = requests.get(request_url).status_code
            assert response == 200
        if product_type == 'oilseeds':
            request_url = f'{url}products={product_name}&memberStateCodes=HU'
            response = requests.get(request_url).status_code
            assert response == 200


    @pytest.mark.parametrize('product_name' , ['BLTPAN', 'MAI', 'Rapeseed'])
    def test_get_product_prices(self, product_name):
        response = get_product_prices(product_name, main_url, begin_date, end_date)
        print(type(end_date))
        assert type(response) == list
