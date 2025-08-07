FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей для Piper
RUN apt update && apt install -y \
    git cmake build-essential libespeak-ng1 espeak-ng-data \
    && rm -rf /var/lib/apt/lists/*

# Клонируем и собираем Piper
RUN git clone https://github.com/rhasspy/piper.git /build && \
    cd /build && mkdir build && cd build && \
    cmake .. && make && cp piper /app/

# Копируем модели и данные
COPY ./models /app/models
COPY ./espeak-ng-data /app/espeak-ng-data

# Копируем requirements и устанавливаем зависимости
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем остальные файлы (например, server.py)
COPY . /app/

EXPOSE 5000

CMD ["python", "server.py"]
