import pytest

from data_core.data import ApiData
from data_core import main_constants


class TestDataProcessing:
    api_data = ApiData()
    @pytest.mark.parametrize('data' , main_constants.products)
    def test_data_processing(self, data):
        result = self.api_data.data_processing(product_name=data)
        assert type(result) == list
