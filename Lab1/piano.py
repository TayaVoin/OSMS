import numpy as np
import sounddevice as sd
from pynput import keyboard
import threading

fs = 44100
duration = 0.6 

notes_map = {
    'z': ('До (C4)', 261.63),
    'x': ('Ре (D4)', 293.66),
    'c': ('Ми (E4)', 329.63),
    'v': ('Фа (F4)', 349.23),
    'b': ('Соль (G4)', 392.00),
    'n': ('Ля (A4)', 440.00),
    'm': ('Си (B4)', 493.88)
}

def play_sound(frequency):
    """Функция генерации и воспроизведения синусоидального сигнала"""
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    wave = np.sin(2 * np.pi * frequency * t)

    envelope = np.exp(-3 * t)
    wave = wave * envelope * 0.5
    
    sd.play(wave, fs)

def on_press(key):
    """Функция, которая срабатывает при нажатии клавиши"""
    try:
        k = key.char.lower()
        if k in notes_map:
            note_name, freq = notes_map[k]
            print(f"Играет нота: {note_name} ({freq} Гц)")
            threading.Thread(target=play_sound, args=(freq,)).start()
    except AttributeError:
        pass

def on_release(key):
    """Функция для выхода из программы"""
    if key == keyboard.Key.esc:
        print("\nВыход из программы...")
        return False

print("~~~ ВИРТУАЛЬНОЕ ПИАНИНО ~~~")
print("Нажимайте клавиши (русская раскладка):")
print("Я (До), Ч (Ре), С (Ми), М (Фа), И (Соль), Т (Ля), Ь (Си)")
print("Для выхода нажмите ESC\n")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()