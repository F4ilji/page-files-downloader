# Используем официальный образ Python как базовый
FROM python:3.9-slim-buster

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем наш Python-скрипт в рабочую директорию
COPY download_script.py .

# Команда, которая будет выполняться при запуске контейнера
# (мы можем переопределить ее в docker-compose.yml)
CMD ["python", "download_script.py"]