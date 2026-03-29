import requests
import pytest

from data_core.main_constants import main_url, begin_date, end_date


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
        from data_core.data import ApiData
        api_data = ApiData()
        
        if product_name == 'BLTPAN' or product_name == 'MAI':
            product_type = 'cereal'
        else:
            product_type = 'oilseeds'
        
        url = f'{main_url}/{product_type}/prices?beginDate={begin_date}&endDate={end_date}&'
        
        if product_type == 'cereal':
            request_url = f'{url}productCodes={product_name}'
        else:
            request_url = f'{url}products={product_name}'
        
        response = api_data.get_data(request_url)
        assert isinstance(response, list)
