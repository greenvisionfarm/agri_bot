from data_core.data import ApiData
from data_core.main_constants import products
import pytest

class TestValidationData:
    api_data = ApiData()
    @pytest.mark.parametrize('data' , products)
    def test_validation_data_positive_prod(self, data):
        result = self.api_data.validation_of_incoming_data(data)[0]
        assert result in products


    @pytest.mark.parametrize('data' , ['Pšenica graf', 'Kukurica graf', 'Raps graf'])
    def test_validation_data_positive_graf(self, data):
        result = self.api_data.validation_of_incoming_data(data)
        result = f'{result[0]} {result[1]}'
        assert result in ['Pšenica graf', 'Kukurica graf', 'Raps graf']


    @pytest.mark.parametrize('data' , [' ', 'qwerty', 'qwerty qwerty'])
    def test_validation_data_negative(self, data):
        result = self.api_data.validation_of_incoming_data(data)
        assert result == False
