import numpy as np
import sounddevice as sd
from pynput import keyboard
import time
import matplotlib.pyplot as plt

fs = 44100
record_duration = 3.0
note_duration = 0.6

# Словарь нот
notes_map = {
    'z': ('До (C4)', 261.63),
    'x': ('Ре (D4)', 293.66),
    'c': ('Ми (E4)', 329.63),
    'v': ('Фа (F4)', 349.23),
    'b': ('Соль (G4)', 392.00),
    'n': ('Ля (A4)', 440.00),
    'm': ('Си (B4)', 493.88)
}

# Создаем пустой массив-буфер на 3 секунды (тишина)
total_samples = int(fs * record_duration)
master_audio = np.zeros(total_samples)

start_time = time.time()

def play_and_mix(frequency):
    """Генерирует ноту, проигрывает её и добавляет в общий буфер"""
    t = np.linspace(0, note_duration, int(fs * note_duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    envelope = np.exp(-3 * t) # Плавное затухание
    wave = wave * envelope * 0.5
    
    sd.play(wave, fs)
    
    # Смешиваем в общий массив для записи
    current_time = time.time() - start_time
    start_idx = int(current_time * fs)
    
    if start_idx < total_samples:
        end_idx = min(start_idx + len(wave), total_samples)
        actual_len = end_idx - start_idx
        master_audio[start_idx:end_idx] += wave[:actual_len]

def on_press(key):
    """Срабатывает при нажатии клавиши"""
    if time.time() - start_time > record_duration:
        return
        
    try:
        k = key.char.lower()
        if k in notes_map:
            note_name, freq = notes_map[k]
            print(f"Играет: {note_name} ({freq} Гц)")
            play_and_mix(freq)
    except AttributeError:
        pass

# ~~~ Основная программа ~~~
print("~~~ ВИРТУАЛЬНОЕ ПИАНИНО (ЗАПИСЬ 3 СЕКУНДЫ) ~~~")
print("Нажимайте клавиши (Я, Ч, С, М, И, Т, Ь) прямо сейчас!")
print("Идет запись...")

# Запускаем слушатель клавиатуры в фоне
listener = keyboard.Listener(on_press=on_press)
listener.start()

time.sleep(record_duration)

listener.stop()
print("\nЗапись завершена! Строим графики...")

# ~~~ РАСЧЕТ СПЕКТРА (БПФ) ~~~
N = len(master_audio)
Y = np.fft.rfft(master_audio)
freqs = np.fft.rfftfreq(N, d=1/fs)
Y_mag = np.abs(Y) / N

# ~~~ ПОСТРОЕНИЕ ГРАФИКОВ ~~~
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# 1. График во временной области
time_axis = np.linspace(0, record_duration, total_samples)
ax1.plot(time_axis, master_audio, color='blue', linewidth=0.5)
ax1.set_title('Временная область (что мы сыграли за 3 секунды)')
ax1.set_xlabel('Время, с')
ax1.set_ylabel('Амплитуда')
ax1.grid(True)
ax1.set_xlim(0, record_duration)

# 2. График в частотной области (Спектр)
ax2.plot(freqs, Y_mag, color='red', linewidth=1)
ax2.set_title('Амплитудный спектр (какие ноты были нажаты)')
ax2.set_xlabel('Частота, Гц')
ax2.set_ylabel('Амплитуда')
ax2.grid(True)
ax2.set_xlim(0, 1000) 

plt.tight_layout()
plt.show()