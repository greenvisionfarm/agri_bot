"""
Конфігурація pytest для всього проекту.
Встановлює змінні оточення перед запуском тестів.
"""
import os
import pytest

# Встановлюємо тестовий TOKEN до завантаження будь-яких модулів
# Це має бути зроблено до імпорту bot.configuration
os.environ.setdefault('TOKEN', '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz')


@pytest.fixture(scope='session')
def test_token():
    """Фікстура з тестовим токеном"""
    return os.environ.get('TOKEN')


@pytest.fixture
def sample_products():
    """Фікстура зі списком продуктів"""
    from data_core import main_constants
    return main_constants.products


@pytest.fixture
def api_data():
    """Фікстура з екземпляром ApiData"""
    from data_core.data import ApiData
    return ApiData()
