"""
Интеграционные тесты для European Commission Agri-Food API

Проверяют реальное соединение с API и получение данных.
"""
import pytest
import requests
from datetime import datetime, timedelta

from data_core.data import ApiData
from data_core import main_constants


class TestAPIIntegration:
    """Тесты интеграции с API"""

    @pytest.fixture
    def api_data(self):
        """Фикстура с экземпляром ApiData"""
        return ApiData()

    @pytest.mark.parametrize('product_code,product_type', [
        ('BLTPAN', 'cereal'),   # Пшеница
        ('MAI', 'cereal'),      # Кукуруза
        ('Rapeseed', 'oilseeds') # Рапс
    ])
    def test_api_connection_status(self, product_code, product_type):
        """Проверка доступности API для каждого продукта"""
        if product_type == 'cereal':
            request_url = f'{main_constants.main_url}/{product_type}/prices?beginDate=01/01/2024&memberStateCodes=SK&productCodes={product_code}'
        else:
            request_url = f'{main_constants.main_url}/{product_type}/prices?beginDate=01/01/2024&memberStateCodes=SK&products={product_code}'

        response = requests.get(request_url, timeout=10)

        assert response.status_code == 200, f"API вернул {response.status_code} для {product_code}"
        assert response.headers.get('Content-Type', '').startswith('application/json'), "Ответ не JSON"

    @pytest.mark.parametrize('product_code,product_type', [
        ('BLTPAN', 'cereal'),
        ('MAI', 'cereal'),
        ('Rapeseed', 'oilseeds')
    ])
    def test_api_response_structure(self, product_code, product_type):
        """Проверка структуры ответа API"""
        if product_type == 'cereal':
            request_url = f'{main_constants.main_url}/{product_type}/prices?beginDate=01/01/2024&memberStateCodes=SK&productCodes={product_code}'
        else:
            request_url = f'{main_constants.main_url}/{product_type}/prices?beginDate=01/01/2024&memberStateCodes=SK&products={product_code}'

        response = requests.get(request_url, timeout=10)
        data = response.json()

        assert isinstance(data, list), f"Ожидался список, получено {type(data)}"
        assert len(data) > 0, "API вернул пустой список"

        # Проверка структуры первого элемента
        first_item = data[0]
        assert isinstance(first_item, dict), "Первый элемент не dict"
        assert 'price' in first_item, "Отсутствует поле 'price'"
        assert 'beginDate' in first_item, "Missing 'beginDate' field"
    
    @pytest.mark.parametrize('product_name', ['Pšenica', 'Kukurica', 'Raps'])
    def test_api_data_get_data_method(self, product_name, api_data):
        """Проверка метода get_data класса ApiData"""
        product_code = main_constants.products_dict[product_name]
        product_type = main_constants.products_groups[product_code]

        request_url = f'{main_constants.main_url}/{product_type}/prices?beginDate=01/01/2024&memberStateCodes=SK'
        if product_type == 'cereal':
            request_url += f'&productCodes={product_code}'
        else:
            request_url += f'&products={product_code}'

        result = api_data.get_data(request_url)

        assert result != [False, False], f"API вернул ошибку для {product_name}"
        assert isinstance(result, list), f"Ожидался список, получено {type(result)}"
        assert len(result) > 0, "API вернул пустой список"

    def test_api_timeout_handling(self, api_data):
        """Проверка обработки таймаутов"""
        # Используем несуществующий URL для имитации таймаута
        result = api_data.get_data('http://10.255.255.1/api/test')

        # Должен вернуть [False, False] при ошибке
        assert result == [False, False], "Таймаут должен вернуть [False, False]"

    @pytest.mark.parametrize('product_name', ['Pšenica', 'Kukurica', 'Raps'])
    def test_api_data_processing(self, api_data, product_name):
        """Проверка обработки данных для каждого продукта"""
        result = api_data.data_processing(product_name)

        # Результат должен быть списком или [False, False] если нет данных
        assert isinstance(result, list), f"Ожидался список, получено {type(result)}"

        if result != [False, False]:
            # Если данные есть, проверяем структуру
            assert len(result) == 2, f"Ожидалось 2 элемента, получено {len(result)}"
            price, date = result

            # Проверка цены (должна быть строкой)
            assert isinstance(price, str), f"Цена должна быть строкой, получено {type(price)}"
            # Удаляем € и проверяем что это число
            clean_price = price.replace('€', '').replace(',', '.')
            try:
                float(clean_price)
            except ValueError:
                pytest.fail(f"Цена '{price}' не является корректным числом")

            # Проверка даты (должна быть в формате DD/MM/YYYY)
            assert isinstance(date, str), f"Дата должна быть строкой, получено {type(date)}"
            assert len(date) == 10, f"Неверная длина даты: {date}"


class TestAPIEndpoints:
    """Тесты для различных API endpoints"""

    def test_cereal_endpoint(self):
        """Тест endpoint для зерновых культур"""
        url = f'{main_constants.main_url}/cereal/prices?beginDate=01/01/2024&memberStateCodes=SK&productCodes=BLTPAN'
        response = requests.get(url, timeout=10)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_oilseeds_endpoint(self):
        """Тест endpoint для масличных культур"""
        url = f'{main_constants.main_url}/oilseeds/prices?beginDate=01/01/2024&memberStateCodes=SK&products=Rapeseed'
        response = requests.get(url, timeout=10)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_invalid_product_code(self):
        """Тест с несуществующим кодом продукта"""
        url = f'{main_constants.main_url}/cereal/prices?beginDate=01/01/2024&memberStateCodes=SK&productCodes=INVALID'
        response = requests.get(url, timeout=10)

        # API должен вернуть ошибку или пустой список
        assert response.status_code in [200, 400, 404], f"Неожиданный код статуса: {response.status_code}"

    def test_invalid_date_format(self):
        """Тест с неверным форматом даты"""
        url = f'{main_constants.main_url}/cereal/prices?beginDate=invalid-date&memberStateCodes=SK&productCodes=BLTPAN'
        response = requests.get(url, timeout=10)

        # API может вернуть 200, 400 или 500 для неверной даты
        assert response.status_code in [200, 400, 500], f"Неожиданный код статуса: {response.status_code}"


class TestAPIDataValidation:
    """Тесты валидации данных из API"""

    @pytest.fixture
    def api_data(self):
        return ApiData()

    def test_price_format(self, api_data):
        """Проверка формата цен из API"""
        result = api_data.data_processing('Pšenica')

        if result != [False, False]:
            price_str = result[0]
            # Цена может быть в формате "€123.45", "123,45€" или "123.45€"
            # Удаляем € и проверяем что это число
            clean_price = price_str.replace('€', '').replace(',', '.')
            try:
                float(clean_price)
            except ValueError:
                pytest.fail(f"Цена '{price_str}' не является корректным числом")

    def test_date_format(self, api_data):
        """Проверка формата даты из API"""
        result = api_data.data_processing('Pšenica')

        if result != [False, False]:
            date_str = result[1]
            # Дата должна быть в формате DD/MM/YYYY
            parts = date_str.split('/')
            assert len(parts) == 3, f"Неверный формат даты: {date_str}"

            day, month, year = parts
            assert len(day) == 2, f"Неверный день: {day}"
            assert len(month) == 2, f"Неверный месяц: {month}"
            assert len(year) == 4, f"Неверный год: {year}"

    def test_graph_creation(self, api_data):
        """Проверка создания графика"""
        graph_data = api_data.create_graf('Pšenica')

        # График должен быть создан (bytes) или False если нет данных
        if graph_data is not False:
            assert isinstance(graph_data, bytes), "График должен быть bytes"
            assert len(graph_data) > 0, "График пустой"
            # Проверка PNG signature
            assert graph_data[:8] == b'\x89PNG\r\n\x1a\n', "Неверный PNG файл"