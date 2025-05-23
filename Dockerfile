FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Копируем скрипт ожидания (после COPY . .)
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Указываем переменную окружения для Python
ENV PYTHONUNBUFFERED=1

# Открываем порт для приложения
EXPOSE 8000

# Запускаем приложение
CMD ["python", "-m", "app.main"]
