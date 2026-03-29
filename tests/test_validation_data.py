from bot.functions import validation_of_incoming_data
from data_core.main_constants import products
import pytest


class TestValidationData:
    @pytest.mark.parametrize('data', products)
    def test_validation_data_positive_prod(self, data):
        result = validation_of_incoming_data(data)
        assert result is not False
        assert result[0] in products

    @pytest.mark.parametrize('data', ['Pšenica graf', 'Kukurica graf', 'Raps graf'])
    def test_validation_data_positive_graf(self, data):
        result = validation_of_incoming_data(data)
        result = f'{result[0]} {result[1]}'
        assert result in ['Pšenica graf', 'Kukurica graf', 'Raps graf']

    @pytest.mark.parametrize('data', [' ', 'qwerty', 'qwerty qwerty'])
    def test_validation_data_negative(self, data):
        result = validation_of_incoming_data(data)
        assert result is False
