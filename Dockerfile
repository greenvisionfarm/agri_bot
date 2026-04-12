# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости для matplotlib и других либ
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6-dev \
    libpng-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем только файл зависимостей для кэширования слоев
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . .

# Создаем директории для логов и данных, если их нет
RUN mkdir -p logs data

# По умолчанию запускаем бота (это переопределяется в docker-compose для планировщика)
CMD ["python", "main.py"]
