import subprocess
import sounddevice as sd
import soundfile as sf
import os

TEXT = "Привет"
PIPER_EXE = "piper/piper.exe"
MODEL_ONNX = "piper/denis.onnx"
CONFIG_JSON = "piper/denis-onnx.json"   # 👈 Обязательно для моделей от OHF-Voice
OUTPUT_WAV = "output.wav"

# Проверка файлов
for path in [PIPER_EXE, MODEL_ONNX, CONFIG_JSON]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Не найден файл: {path}")

# Запуск
print(f"[INFO] Озвучка текста: {TEXT}")
result = subprocess.run([
    PIPER_EXE,
    "--model", MODEL_ONNX,
    "--config", CONFIG_JSON,         # 👈 Добавлен config
    "--output_file", OUTPUT_WAV,
    "--text", TEXT
], capture_output=True, text=True)

print("[DEBUG] STDOUT:\n", result.stdout)
print("[DEBUG] STDERR:\n", result.stderr)

if result.returncode != 0:
    print(f"[ERROR] Piper завершился с ошибкой")
    exit(1)

# Воспроизведение
data, samplerate = sf.read(OUTPUT_WAV)
sd.play(data, samplerate)
sd.wait()
