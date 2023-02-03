from data_core.secondary_functions import validation_of_incoming_data
import pytest


@pytest.mark.parametrize('data' , ['Pšenica', 'Kukurica', 'Raps'])
def test_products_validation_of_incoming_data_positive(data):
    result = validation_of_incoming_data(data)[0]
    assert result in ['Pšenica', 'Kukurica', 'Raps']


@pytest.mark.parametrize('data' , ['Pšenica graf', 'Kukurica graf', 'Raps graf'])
def test_products_validation_of_incoming_data_positive(data):
    result = validation_of_incoming_data(data)
    result = f'{result[0]} {result[1]}'
    assert result in ['Pšenica graf', 'Kukurica graf', 'Raps graf']


@pytest.mark.parametrize('data' , [' ', 'qwerty', 'qwerty qwerty'])
def test_validation_of_incoming_data_negative(data):
    result = validation_of_incoming_data(data)
    assert result == False

