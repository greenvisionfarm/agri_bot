"""
Тесты для проверки основной функциональности бота

Проверяют работу обработчиков сообщений, валидацию и интеграцию компонентов.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from telebot import types

# TOKEN установлен в conftest.py до запуска тестов

from bot.functions import validation_of_incoming_data, create_message
from bot import constants
from data_core.data import ApiData
from data_core import main_constants


class TestBotHandlers:
    """Тесты обработчиков сообщений бота"""

    def test_start_command_handler(self):
        """Проверка обработки команды /start"""
        from bot.configuration import bot
        from bot import buttons

        mock_message = Mock()
        mock_message.from_user.id = 12345
        mock_message.from_user.username = 'test_user'
        mock_message.chat.id = 12345
        mock_message.bot = bot

        # Импортируем функцию после установки TOKEN
        from bot.main import add_buttons
        markup = add_buttons()

        assert isinstance(markup, types.ReplyKeyboardMarkup)
        assert len(buttons.bot_buttons) == 6  # 3 продукта + 3 графика

    def test_add_buttons(self):
        """Проверка создания кнопок"""
        from bot import buttons

        from bot.main import add_buttons
        markup = add_buttons()

        assert isinstance(markup, types.ReplyKeyboardMarkup)
        assert len(buttons.bot_buttons) == 6  # 3 продукта + 3 графика


class TestValidation:
    """Тесты валидации входных данных"""

    @pytest.mark.parametrize('input_text,expected', [
        ('Pšenica', ['Pšenica']),
        ('Kukurica', ['Kukurica']),
        ('Raps', ['Raps']),
        ('Pšenica graf', ['Pšenica', 'graf']),
        ('Kukurica graf', ['Kukurica', 'graf']),
        ('Raps graf', ['Raps', 'graf']),
    ])
    def test_validation_positive(self, input_text, expected):
        """Позитивные тесты валидации"""
        result = validation_of_incoming_data(input_text)
        assert result == expected, f"Ожидалось {expected}, получено {result}"

    @pytest.mark.parametrize('input_text', [
        ' ',
        '',
        'qwerty',
        'qwerty qwerty',
        'Pšenica extra',
        '123',
        'Pšenica Graf',  # Большая буква
    ])
    def test_validation_negative(self, input_text):
        """Негативные тесты валидации"""
        result = validation_of_incoming_data(input_text)
        assert result is False, f"Ожидалось False для '{input_text}', получено {result}"


class TestCreateMessage:
    """Тесты форматирования сообщений"""

    def test_create_message_format(self):
        """Проверка формата сообщения"""
        result = create_message('250.5', '01/03/2024')
        expected = constants.answer_message.format('250.5', '01/03/2024')
        assert result == expected

    def test_create_message_with_special_chars(self):
        """Проверка со специальными символами"""
        result = create_message('100,5', '15/12/2023')
        assert '100,5' in result
        assert '15/12/2023' in result


class TestApiDataClass:
    """Тесты класса ApiData"""

    @pytest.fixture
    def api_data(self):
        return ApiData()

    def test_api_data_initialization(self, api_data):
        """Проверка инициализации ApiData"""
        assert api_data.url == main_constants.main_url
        assert api_data.country == 'SK'
        assert api_data.begin_date is not None

    def test_get_begin_date(self, api_data):
        """Проверка расчёта начальной даты"""
        date_30 = api_data.get_begin_date(days=30)
        date_120 = api_data.get_begin_date(days=120)

        # Проверка формата даты
        assert len(date_30.split('/')) == 3
        assert len(date_120.split('/')) == 3

        # 120 дней должно быть раньше чем 30 дней
        from datetime import datetime
        d30 = datetime.strptime(date_30, '%d/%m/%Y')
        d120 = datetime.strptime(date_120, '%d/%m/%Y')
        assert d120 < d30

    def test_change_date_format(self, api_data):
        """Проверка изменения формата даты"""
        result = api_data.change_date_format('01/02/2024')
        assert result == '01/02/2024'

    def test_change_price(self, api_data):
        """Проверка конвертации цены"""
        # Тест с запятой (европейский формат)
        result = api_data.change_price('123,45€')
        assert result == 123.45

        # Тест с точкой
        result = api_data.change_price('100.50€')
        assert result == 100.50

    def test_change_price_invalid(self, api_data):
        """Проверка с неверной ценой"""
        result = api_data.change_price('invalid')
        assert result == 0.0


class TestCallbackHandler:
    """Тесты обработки сообщений callback"""

    def test_callback_private_chat_only(self):
        """Проверка что бот отвечает только в приватных чатах"""
        from bot.main import callback
        from bot.configuration import bot

        mock_message = Mock()
        mock_message.chat.type = 'group'
        mock_message.from_user.id = 12345
        mock_message.from_user.username = 'test'
        mock_message.text = 'Pšenica'
        mock_message.bot = bot

        with patch.object(bot, 'send_message') as mock_send:
            callback(mock_message)
            # Бот не должен отправлять сообщение в групповом чате
            assert not mock_send.called

    def test_callback_invalid_input(self):
        """Проверка обработки неверных данных"""
        from bot.main import callback
        from bot.configuration import bot

        mock_message = Mock()
        mock_message.chat.type = 'private'
        mock_message.from_user.id = 12345
        mock_message.from_user.username = 'test'
        mock_message.text = 'invalid_input'
        mock_message.bot = bot

        with patch.object(bot, 'send_message') as mock_send:
            callback(mock_message)
            # Бот должен отправить сообщение об ошибке
            assert mock_send.called
            call_args = mock_send.call_args
            assert constants.error_message in call_args[0][1]

    @patch('bot.main.ApiData')
    def test_callback_price_request(self, mock_api_class):
        """Проверка запроса цены"""
        from bot.main import callback
        from bot.configuration import bot

        # Настраиваем мок для ApiData
        mock_api_instance = Mock()
        mock_api_instance.data_processing.return_value = ['250.5', '01/03/2024']
        mock_api_class.return_value = mock_api_instance

        mock_message = Mock()
        mock_message.chat.type = 'private'
        mock_message.from_user.id = 12345
        mock_message.from_user.username = 'test'
        mock_message.text = 'Pšenica'
        mock_message.bot = bot

        with patch.object(bot, 'send_message') as mock_send:
            callback(mock_message)

            # Проверяем что data_processing был вызван
            assert mock_api_instance.data_processing.called
            # Бот должен отправить ответ
            assert mock_send.called

    @patch('bot.main.ApiData')
    def test_callback_graph_request(self, mock_api_class):
        """Проверка запроса графика"""
        from bot.main import callback
        from bot.configuration import bot

        # Настраиваем мок для ApiData
        mock_api_instance = Mock()
        mock_api_instance.create_graf.return_value = b'fake_png_data'
        mock_api_class.return_value = mock_api_instance

        mock_message = Mock()
        mock_message.chat.type = 'private'
        mock_message.from_user.id = 12345
        mock_message.from_user.username = 'test'
        mock_message.text = 'Pšenica graf'
        mock_message.bot = bot

        with patch.object(bot, 'send_photo') as mock_send:
            callback(mock_message)

            # Проверяем что create_graf был вызван
            assert mock_api_instance.create_graf.called
            # Бот должен отправить фото
            assert mock_send.called


class TestErrorHandling:
    """Тесты обработки ошибок"""

    @patch('bot.main.ApiData')
    def test_callback_api_error(self, mock_api_class):
        """Проверка обработки ошибки API"""
        from bot.main import callback
        from bot.configuration import bot

        # Настраиваем мок для возврата ошибки
        mock_api_instance = Mock()
        mock_api_instance.data_processing.return_value = [False, False]
        mock_api_class.return_value = mock_api_instance

        mock_message = Mock()
        mock_message.chat.type = 'private'
        mock_message.from_user.id = 12345
        mock_message.from_user.username = 'test'
        mock_message.text = 'Pšenica'
        mock_message.bot = bot

        with patch.object(bot, 'send_message') as mock_send:
            callback(mock_message)

            # Бот должен отправить сообщение об ошибке
            assert mock_send.called
            call_args = mock_send.call_args
            assert 'Не удалось получить данные' in call_args[0][1]

    @patch('bot.main.ApiData')
    def test_callback_graph_no_data(self, mock_api_class):
        """Проверка когда нет данных для графика"""
        from bot.main import callback
        from bot.configuration import bot

        mock_api_instance = Mock()
        mock_api_instance.create_graf.return_value = False
        mock_api_class.return_value = mock_api_instance

        mock_message = Mock()
        mock_message.chat.type = 'private'
        mock_message.from_user.id = 12345
        mock_message.from_user.username = 'test'
        mock_message.text = 'Pšenica graf'
        mock_message.bot = bot

        with patch.object(bot, 'send_message') as mock_send:
            callback(mock_message)

            # Бот должен отправить сообщение о недостатке данных
            assert mock_send.called
            call_args = mock_send.call_args
            assert 'Na vykreslenie grafu nie je dostatok hodnôt' in call_args[0][1]