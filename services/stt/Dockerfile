FROM python:3.11-slim

RUN apt update && apt install -y \
    git build-essential portaudio19-dev && \
    pip install --no-cache-dir vosk sounddevice

WORKDIR /app

COPY . .

CMD ["python", "app.py"]
