"""
Конфигурация pytest для всего проекта.
Устанавливает переменные окружения перед запуском тестов.
"""
import os
import pytest

# Устанавливаем тестовый TOKEN до загрузки любых модулей
# Это должно быть сделано до импорта bot.configuration
os.environ.setdefault('TOKEN', '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz')


@pytest.fixture(scope='session')
def test_token():
    """Фикстура с тестовым токеном"""
    return os.environ.get('TOKEN')


@pytest.fixture
def sample_products():
    """Фикстура со списком продуктов"""
    from data_core import main_constants
    return main_constants.products


@pytest.fixture
def api_data():
    """Фикстура с экземпляром ApiData"""
    from data_core.data import ApiData
    return ApiData()
