"""
Тести для перевірки основної функціональності бота

Перевіряють роботу обробників повідомлень, валідацію та інтеграцію компонентів.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from telebot import types

# TOKEN встановлено в conftest.py до запуску тестів

from bot.functions import validation_of_incoming_data, create_message
from bot import constants
from data_core.data import ApiData
from data_core import main_constants


class TestBotHandlers:
    """Тести обробників повідомлень бота"""
    
    def test_start_command_handler(self):
        """Перевірка обробки команди /start"""
        from bot.configuration import bot
        from bot import buttons
        
        mock_message = Mock()
        mock_message.from_user.id = 12345
        mock_message.from_user.username = 'test_user'
        mock_message.chat.id = 12345
        mock_message.bot = bot
        
        # Імпортуємо функцію після встановлення TOKEN
        from bot.main import add_buttons
        markup = add_buttons()
        
        assert isinstance(markup, types.ReplyKeyboardMarkup)
        assert len(buttons.bot_buttons) == 6  # 3 продукти + 3 графіки
    
    def test_add_buttons(self):
        """Перевірка створення кнопок"""
        from bot import buttons
        
        from bot.main import add_buttons
        markup = add_buttons()
        
        assert isinstance(markup, types.ReplyKeyboardMarkup)
        assert len(buttons.bot_buttons) == 6  # 3 продукти + 3 графіки


class TestValidation:
    """Тести валідації вхідних даних"""
    
    @pytest.mark.parametrize('input_text,expected', [
        ('Pšenica', ['Pšenica']),
        ('Kukurica', ['Kukurica']),
        ('Raps', ['Raps']),
        ('Pšenica graf', ['Pšenica', 'graf']),
        ('Kukurica graf', ['Kukurica', 'graf']),
        ('Raps graf', ['Raps', 'graf']),
    ])
    def test_validation_positive(self, input_text, expected):
        """Позитивні тести валідації"""
        result = validation_of_incoming_data(input_text)
        assert result == expected, f"Expected {expected}, got {result}"
    
    @pytest.mark.parametrize('input_text', [
        ' ',
        '',
        'qwerty',
        'qwerty qwerty',
        'Pšenica extra',
        '123',
        'Pšenica Graf',  # Велика літера
    ])
    def test_validation_negative(self, input_text):
        """Негативні тести валідації"""
        result = validation_of_incoming_data(input_text)
        assert result is False, f"Expected False for '{input_text}', got {result}"


class TestCreateMessage:
    """Тести форматування повідомлень"""
    
    def test_create_message_format(self):
        """Перевірка формату повідомлення"""
        result = create_message('250.5', '01/03/2024')
        expected = constants.answer_message.format('250.5', '01/03/2024')
        assert result == expected
    
    def test_create_message_with_special_chars(self):
        """Перевірка з спеціальними символами"""
        result = create_message('100,5', '15/12/2023')
        assert '100,5' in result
        assert '15/12/2023' in result


class TestApiDataClass:
    """Тести класу ApiData"""
    
    @pytest.fixture
    def api_data(self):
        return ApiData()
    
    def test_api_data_initialization(self, api_data):
        """Перевірка ініціалізації ApiData"""
        assert api_data.url == main_constants.main_url
        assert api_data.country == 'SK'
        assert api_data.begin_date is not None
    
    def test_get_begin_date(self, api_data):
        """Перевірка розрахунку початкової дати"""
        date_30 = api_data.get_begin_date(days=30)
        date_120 = api_data.get_begin_date(days=120)
        
        # Перевірка формату дати
        assert len(date_30.split('/')) == 3
        assert len(date_120.split('/')) == 3
        
        # 120 днів має бути раніше ніж 30 днів
        from datetime import datetime
        d30 = datetime.strptime(date_30, '%d/%m/%Y')
        d120 = datetime.strptime(date_120, '%d/%m/%Y')
        assert d120 < d30
    
    def test_change_date_format(self, api_data):
        """Перевірка зміни формату дати"""
        result = api_data.change_date_format('01/02/2024')
        assert result == '01/02/2024'
    
    def test_change_price(self, api_data):
        """Перевірка конвертації ціни"""
        # Тест з комою (європейський формат)
        result = api_data.change_price('123,45€')
        assert result == 123.45
        
        # Тест з крапкою
        result = api_data.change_price('100.50€')
        assert result == 100.50
    
    def test_change_price_invalid(self, api_data):
        """Перевірка з невірною ціною"""
        result = api_data.change_price('invalid')
        assert result == 0.0


class TestCallbackHandler:
    """Тести обробки повідомлень callback"""
    
    def test_callback_private_chat_only(self):
        """Перевірка що бот відповідає тільки в приватних чатах"""
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
            # Бот не має надсилати повідомлення в груповому чаті
            assert not mock_send.called
    
    def test_callback_invalid_input(self):
        """Перевірка обробки невірних даних"""
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
            # Бот має надіслати повідомлення про помилку
            assert mock_send.called
            call_args = mock_send.call_args
            assert constants.error_message in call_args[0][1]
    
    @patch('bot.main.ApiData')
    def test_callback_price_request(self, mock_api_class):
        """Перевірка запиту ціни"""
        from bot.main import callback
        from bot.configuration import bot
        
        # Налаштовуємо мок для ApiData
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
            
            # Перевіряємо що data_processing був викликаний
            assert mock_api_instance.data_processing.called
            # Бот має надіслати відповідь
            assert mock_send.called
    
    @patch('bot.main.ApiData')
    def test_callback_graph_request(self, mock_api_class):
        """Перевірка запиту графіку"""
        from bot.main import callback
        from bot.configuration import bot
        
        # Налаштовуємо мок для ApiData
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
            
            # Перевіряємо що create_graf був викликаний
            assert mock_api_instance.create_graf.called
            # Бот має надіслати фото
            assert mock_send.called


class TestErrorHandling:
    """Тести обробки помилок"""
    
    @patch('bot.main.ApiData')
    def test_callback_api_error(self, mock_api_class):
        """Перевірка обробки помилки API"""
        from bot.main import callback
        from bot.configuration import bot
        
        # Налаштовуємо мок для повернення помилки
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
            
            # Бот має надіслати повідомлення про помилку
            assert mock_send.called
            call_args = mock_send.call_args
            assert 'Не удалось получить данные' in call_args[0][1]
    
    @patch('bot.main.ApiData')
    def test_callback_graph_no_data(self, mock_api_class):
        """Перевірка коли немає даних для графіку"""
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
            
            # Бот має надіслати повідомлення про недостатньо даних
            assert mock_send.called
            call_args = mock_send.call_args
            assert 'Na vykreslenie grafu nie je dostatok hodnôt' in call_args[0][1]