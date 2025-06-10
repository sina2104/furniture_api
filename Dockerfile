FROM python:3.11-slim

# Установить системные зависимости, нужные для opencv-python
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем файлы
COPY app ./app
COPY requirements.txt .

# Установка Python-зависимостей
RUN pip install --upgrade pip && pip install -r requirements.txt

# Указываем порт
EXPOSE 10000

# Запуск FastAPI-приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
