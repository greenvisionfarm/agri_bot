import pytest

from data_core.post_data import data_processing


@pytest.mark.parametrize('data' , ['Pšenica', 'Kukurica', 'Rapseed'])
def test_data_processing(data):
    result = data_processing(data)
    assert type(result) == list