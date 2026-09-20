from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 8. Запись голоса в Audacity 4 и анализ спектра
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Читаем файл
fs, y = wavfile.read('voice.wav')
if y.ndim > 1: y = y.mean(axis=1) # Если стерео, усредняем
y = y.astype(np.float64)
y /= np.max(np.abs(y)) # Нормировка

# Считаем спектр
N = len(y)
Y = np.fft.rfft(y)
freqs = np.fft.rfftfreq(N, d=1/fs)
Y_mag = np.abs(Y) / N

# Ищем максимальную частоту
# Порог: где амплитуда падает ниже 1% от максимума
threshold = 0.01 * np.max(Y_mag)
indices = np.where(Y_mag > threshold)[0]
f_max = freqs[indices[-1]]
print(f"~~~ Часть 8 ~~~")
print(f"Максимальная частота в спектре: {f_max:.0f} Гц")

plt.figure(figsize=(12, 4))
plt.plot(freqs, Y_mag, linewidth=0.8)
plt.title('Амплитудный спектр голоса')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.xlim(0, fs/2) # Показываем до половины частоты дискретизации
plt.grid(True)
plt.tight_layout()
plt.savefig('fig8_voice_fft.png', dpi=150)
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 9. Анализ аудиофайла в Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fs_voice, y_voice = wavfile.read('voice.wav')
print(f"~~~ Часть 9 ~~~")
print(f"Частота дискретизации из файла: {fs_voice} Гц")
print(f"Число отсчетов: {len(y_voice)}")
print(f"Длительность: {len(y_voice)/fs_voice:.3f} с")
print(f"Тип данных: {y_voice.dtype}")

# Если стерео — усредним
if y_voice.ndim > 1:
    y_voice = y_voice.mean(axis=1)

# Нормировка
y_voice = y_voice.astype(np.float64)
y_voice /= np.max(np.abs(y_voice))

t_voice = np.arange(len(y_voice)) / fs_voice
plt.figure(figsize=(12, 4))
plt.plot(t_voice, y_voice, linewidth=0.5)
plt.title('Голосовой сигнал во временной области')
plt.xlabel('t, с')
plt.ylabel('Амплитуда (норм.)')
plt.grid(True)
plt.tight_layout()
plt.savefig('fig8_voice_time.png', dpi=150)
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 10. Определение частоты дискретизации
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

duration = len(y_voice) / fs_voice
fs_calc = len(y_voice) / duration
print(f"~~~ Часть 10 ~~~")
print(f"Вычисленная частота дискретизации: {fs_calc:.0f} Гц")
print(f"Значение из wavfile: {fs_voice} Гц")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 11. Прореживание и воспроизведение
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Прореживание: каждый 10-й отсчет (аналог downsample(y, 10) в Matlab)
y_down = y_voice[::10]
fs_down = fs_voice // 10  # 4410 Гц

print(f"~~~ Часть 11 ~~~")
print(f"Новая частота дискретизации: {fs_down} Гц")
print(f"Число отсчетов после прореживания: {len(y_down)}")

# Сохраним прореженный файл для прослушивания
import soundfile as sf
sf.write('voice_down10.wav', y_down, fs_down)

# Попытка воспроизведения через sounddevice
try:
    import sounddevice as sd
    print("Воспроизведение прореженного сигнала (4410 Гц)...")
    sd.play(y_down, fs_down)
    sd.wait()
    print("Воспроизведение оригинала (44100 Гц)...")
    sd.play(y_voice, fs_voice)
    sd.wait()
except Exception as e:
    print(f"Воспроизведение через Python не удалось: {e}")
    print("Используйте команду в терминале: afplay voice_down10.wav")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 12. ДПФ для оригинала и прореженного сигнала
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def plot_spectrum(signal, fs, title, filename):
    N = len(signal)
    Y = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    Y_mag = np.abs(Y) / N
    plt.figure(figsize=(12, 4))
    plt.plot(freqs, Y_mag, linewidth=0.8)
    plt.title(title)
    plt.xlabel('f, Гц')
    plt.ylabel('|Y(f)|')
    plt.xlim(0, 10000) # Ограничим 10 кГц для наглядности
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()

plot_spectrum(y_voice, fs_voice, 'Спектр оригинала (44100 Гц)', 'fig10_voice_fft_orig.png')
plot_spectrum(y_down, fs_down, 'Спектр прореженного (4410 Гц)', 'fig11_voice_fft_down.png')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 13. Влияние разрядности АЦП
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def quantize(signal, bits):
    levels = 2**bits - 1
    s_min, s_max = signal.min(), signal.max()
    if s_max == s_min:
        return np.zeros_like(signal), 0.0
    s_norm = (signal - s_min) / (s_max - s_min) * levels
    s_quant = np.round(s_norm)
    s_out = s_quant / levels * (s_max - s_min) + s_min
    error = np.mean(np.abs(signal - s_out))
    return s_out, error

# Возьмем небольшой фрагмент сигнала (например, 0.1 секунды), чтобы графики были читаемы
fragment_len = int(0.1 * fs_voice)
signal_ref = y_voice[:fragment_len]

plt.figure(figsize=(12, 8))
print(f"~~~ Часть 13 ~~~")
for i, bits in enumerate([3, 4, 5, 6]):
    s_q, err = quantize(signal_ref, bits)
    print(f"Разрядность {bits} бит: средняя ошибка квантования = {err:.6f}")
    
    Y_q = np.fft.rfft(s_q)
    freqs_q = np.fft.rfftfreq(len(s_q), d=1/fs_voice)
    Y_q_mag = np.abs(Y_q) / len(s_q)
    
    plt.subplot(2, 2, i+1)
    plt.plot(freqs_q, Y_q_mag, linewidth=0.8, color='red')
    plt.title(f'Спектр при {bits} бит (ошибка={err:.5f})')
    plt.xlabel('f, Гц')
    plt.ylabel('|Y(f)|')
    plt.xlim(0, 10000)
    plt.grid(True)

plt.tight_layout()
plt.savefig('fig12_quantization.png', dpi=150)
plt.show()