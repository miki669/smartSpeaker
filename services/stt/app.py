import queue
import sounddevice as sd
import vosk
import sys
import json
import os
import threading

# 🧠 Слова-активаторы
WAKE_WORDS = ["колонка", "ассистент", "привет", "помощник"]

# Загрузка модели
model_path = "model/vosk-model-small-ru-0.22"
if not os.path.exists(model_path):
    print(f"❌ Model not found at: {model_path}")
    sys.exit(1)

model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)
q = queue.Queue()

# 💬 Глобальное состояние
listening_command = threading.Event()

def callback(indata, frames, time, status):
    if status:
        print("⚠️", status, file=sys.stderr)
    q.put(bytes(indata))

def process_stream():
    print("🎙 Система запущена. Ожидание ключевого слова...")

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if listening_command.is_set():
                # Режим команды
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print("🗣 Команда:", text)
                        print("🔁 Возврат в режим ожидания ключевого слова...\n")
                        listening_command.clear()
                        print("🎙 Ожидание ключевого слова...")
            else:
                # Ожидание ключевого слова
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").lower()
                    if text:
                        print("🧾 Распознано:", text)
                    if any(word in text for word in WAKE_WORDS):
                        print("✅ Ключевое слово найдено. Слушаю команду...")
                        listening_command.set()

if __name__ == "__main__":
    try:
        process_stream()
    except KeyboardInterrupt:
        print("\n⛔ Выход")
