# Agri-bot 🌾

Telegram-бот, предоставляющий актуальные данные о ценах на пшеницу, кукурузу и рапс из API [European Commission Agri-Food Data Portal](https://agridata.ec.europa.eu/extensions/DataPortal/home.html).

🤖 **Telegram:** [@Lagro_bot](https://t.me/Lagro_bot)

---

## 📋 Оглавление

- [Возможности](#возможности)
- [Архитектура проекта](#архитектура-проекта)
- [Установка](#установка)
- [Запуск](#запуск)
- [Использование](#использование)
- [Тестирование](#тестирование)
- [Структура проекта](#структура-проекта)
- [Переменные окружения](#переменные-окружения)
- [Развёртывание](#развёртывание)

---

## ✨ Возможности

- 📊 Получение текущих цен на сельскохозяйственные культуры
- 📈 Генерация графиков изменения цен за последние 120 дней
- 🌍 Данные по Словакии (SK) из официального API ЕС
- ⌨️ Удобное кнопочное меню

**Поддерживаемые культуры:**
- Пшеница (Pšenica)
- Кукуруза (Kukurica)
- Рапс (Raps)

---

## 🏗 Архитектура проекта

```
┌─────────────────────────────────────────────────────────┐
│                     main.py (Entry Point)               │
└─────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│   bot/ (Telegram UI)  │       │  data_core/ (Data)    │
│                       │       │                       │
│  - configuration.py   │       │  - data.py            │
│  - main.py (handlers) │       │  - main_constants.py  │
│  - functions.py       │       │                       │
│  - buttons.py         │       │  ApiData:             │
│  - constants.py       │       │  - get_data()         │
│                       │       │  - data_processing()  │
│  validation_of_       │       │  - create_graf()      │
│  incoming_data()      │       │                       │
└───────────────────────┘       └───────────────────────┘
            │                               │
            └───────────────┬───────────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │  European Commission│
                  │  API (agridata.ec.  │
                  │  europa.eu)         │
                  └─────────────────────┘
```

### Модули

| Модуль | Описание |
|--------|----------|
| **bot/** | Telegram-бот интерфейс |
| └─ `configuration.py` | Инициализация TeleBot с токеном |
| └─ `main.py` | Обработчики сообщений (start, callback) |
| └─ `functions.py` | Вспомогательные функции (валидация, форматирование) |
| └─ `buttons.py` | Создание кнопок клавиатуры |
| └─ `constants.py` | Тексты сообщений бота |
| **data_core/** | Слой работы с данными |
| └─ `data.py` | Класс `ApiData`: работа с API, обработка, графики |
| └─ `main_constants.py` | Константы: URL API, продукты, коды |
| **tests/** | pytest-тесты для API и валидации |

---

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd agri_bot
```

### 2. Создание виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# или
.venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` или экспортируйте переменную:

```bash
export TOKEN="your_telegram_bot_token"
```

> 📝 **Как получить токен:** Создайте бота через [@BotFather](https://t.me/BotFather) в Telegram

---

## ▶️ Запуск

### Запуск бота

```bash
python main.py
```

### Запуск в фоновом режиме

```bash
nohup python main.py &
```

---

## 📖 Использование

1. Запустите бота командой `/start`
2. Выберите культуру из меню:
   - `Pšenica` — пшеница
   - `Kukurica` — кукуруза
   - `Raps` — рапс
3. Для получения графика добавьте `graf`:
   - `Pšenica graf`
   - `Kukurica graf`
   - `Raps graf`

### Примеры запросов

| Запрос | Результат |
|--------|-----------|
| `Pšenica` | Текущая цена пшеницы |
| `Pšenica graf` | График цен за 120 дней |
| `Kukurica` | Текущая цена кукурузы |
| `Raps graf` | График цен на рапс |

---

## 🧪 Тестирование

### Запуск всех тестов

```bash
python -m pytest tests/ -v
```

### Запуск конкретного теста

```bash
python -m pytest tests/test_validation_data.py -v
```

### Покрытие тестами

- `test_get_data_test.py` — тесты подключения к API
- `test_post_data_test.py` — тесты обработки данных
- `test_validation_data.py` — тесты валидации входных данных

---

## 📁 Структура проекта

```
agri_bot/
├── main.py                 # Точка входа
├── requirements.txt        # Зависимости
├── runtime.txt            # Версия Python
├── Procfile               # Конфигурация Heroku
├── README.md              # Документация
├── .gitignore             # Игнорируемые файлы
│
├── bot/                   # Модуль бота
│   ├── configuration.py   # Инициализация TeleBot
│   ├── main.py            # Обработчики сообщений
│   ├── functions.py       # Вспомогательные функции
│   ├── buttons.py         # Кнопки клавиатуры
│   └── constants.py       # Тексты сообщений
│
├── data_core/             # Модуль данных
│   ├── data.py            # Класс ApiData
│   ├── main_constants.py  # Константы
│   └── __init__.py
│
└── tests/                 # Тесты
    ├── test_get_data_test.py
    ├── test_post_data_test.py
    └── test_validation_data.py
```

---

## 🔐 Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `TOKEN` | Токен Telegram-бота от @BotFather | ✅ Да |

---

## ☁️ Развёртывание

### Heroku

Проект готов к развёртыванию на Heroku:

```bash
heroku create your-app-name
heroku config:set TOKEN=your_bot_token
git push heroku main
```

Файлы конфигурации:
- `Procfile` — команда запуска
- `runtime.txt` — версия Python (3.12.3)

### Локальный сервер

```bash
# Установка зависимостей
pip install -r requirements.txt

# Установка токена
export TOKEN="your_token"

# Запуск
python main.py
```

---

## 🛠 Технологии

- **[pyTelegramBotAPI (Telebot)](https://pypi.org/project/pyTelegramBotAPI/)** — фреймворк для Telegram-ботов
- **[Requests](https://requests.readthedocs.io/)** — HTTP-запросы к API
- **[Matplotlib](https://matplotlib.org/)** — построение графиков
- **[pytest](https://docs.pytest.org/)** — тестирование

---

## 📄 API Documentation

- [European Commission Agri-Food Data Portal](https://agridata.ec.europa.eu/extensions/DataPortal/API_Documentation.html)
- Base URL: `https://ec.europa.eu/agrifood/api`

---

## 📝 License

Этот проект используется в образовательных целях.

---

## 👤 Author

Разработано для получения данных о ценах на сельскохозяйственные культуры из официальных источников ЕС.
