import numpy as np
import matplotlib.pyplot as plt

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1. Генерация и визуализация непрерывного сигнала
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Параметры варианта 4
A = 3.0
f = 40.0          # Гц
phi = np.pi / 7   # начальная фаза

# Имитация непрерывного времени
t_continuous = np.linspace(0, 1.0, 50000)  # 10000 точек на 0.2 с
y_continuous = A * np.cos(2 * np.pi * f * t_continuous + phi)

# График
plt.figure(figsize=(10, 4))
plt.plot(t_continuous, y_continuous, 'b-', linewidth=1.5)
plt.title('Непрерывный сигнал y(t) = 3cos(2π·40·t + π/7)')
plt.xlabel('t, с')
plt.ylabel('y(t)')
plt.grid(True)
plt.tight_layout()
plt.savefig('fig1_continuous.png', dpi=150)
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. Определение максимальной частоты в спектре
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Аналитический спектр (для отчёта)
plt.figure(figsize=(8, 3))
plt.stem([-f, f], [A/2, A/2], basefmt=" ")
plt.title('Амплитудный спектр (аналитически)')
plt.xlabel('f, Гц')
plt.ylabel('|Y(f)|')
plt.grid(True)
plt.savefig('fig2_spectrum_analytic.png', dpi=150)
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3. Минимальная частота дискретизации (теорема Котельникова)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# fs = 2*f = 2*40 = 80 Гц

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 4. Оцифровка сигнала с частотой 80 Гц
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fs = 80               # частота дискретизации, Гц
T_duration = 1.0      # длительность, с
N = int(fs * T_duration)  # 80 отсчетов
n = np.arange(N)
t_sampled = n / fs
y_sampled = A * np.cos(2 * np.pi * f * t_sampled + phi)

print(f"~~~ Часть 4 ~~~")
print(f"Частота дискретизации: {fs} Гц")
print(f"Число отсчетов: {N}")
print(f"Первые 10 отсчетов: {y_sampled[:10]}")

plt.figure(figsize=(10, 4))
plt.plot(t_continuous, y_continuous, 'b-', alpha=0.4, label='Непрерывный')
plt.stem(t_sampled, y_sampled, linefmt='r-', markerfmt='ro', basefmt=' ',
         label='Отсчеты (fs=80 Гц)')
plt.title('Дискретизация с fs = 80 Гц')
plt.xlabel('t, с')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('fig3_sampling_80.png', dpi=150)
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 5. Прямое ДПФ, ширина спектра, объём памяти
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Прямое ДПФ
# Используем rfft для вещественных сигналов (включает частоту Найквиста)
Y = np.fft.rfft(y_sampled)
freqs = np.fft.rfftfreq(N, d=1/fs)  # частоты от 0 до fs/2 включительно

# Амплитудный спектр (нормировка)
Y_mag = np.abs(Y) / N

print(f"~~~ Часть 5 ~~~")

# Ширина спектра
peak_idx = np.argmax(Y_mag)
print(f"Пик на частоте: {freqs[peak_idx]:.2f} Гц")
print(f"Амплитуда пика: {Y_mag[peak_idx]:.4f}")

# Объём памяти
bytes_per_value = 8  # float64
memory_bytes = N * bytes_per_value
print(f"Объём памяти для массива: {memory_bytes} байт = {memory_bytes/1024:.2f} КБ")

plt.figure(figsize=(10, 4))
plt.stem(freqs, Y_mag, basefmt=' ')
plt.title('Амплитудный спектр (fs = 80 Гц, N = 80)')
plt.xlabel('f, Гц')
plt.ylabel('|Y(f)|')
plt.grid(True)
plt.tight_layout()
plt.savefig('fig4_fft_80.png', dpi=150)
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 6. Восстановление аналогового сигнала
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

plt.figure(figsize=(10, 4))
plt.plot(t_continuous, y_continuous, 'b-', linewidth=2, label='Оригинал')
plt.plot(t_sampled, y_sampled, 'r.-', linewidth=1, markersize=8,
         label='Восстановленный (линейная интерполяция)')
plt.title('Сравнение оригинала и восстановленного сигнала (fs = 80 Гц)')
plt.xlabel('t, с')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('fig5_reconstruction_80.png', dpi=150)
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 7. Увеличение частоты дискретизации в 4 раза
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fs4 = 4 * fs  # 320 Гц
N4 = int(fs4 * T_duration)  # 320 отсчетов
t_sampled4 = np.arange(N4) / fs4
y_sampled4 = A * np.cos(2 * np.pi * f * t_sampled4 + phi)

# ДПФ
Y4 = np.fft.fft(y_sampled4)
freqs4 = np.fft.fftfreq(N4, d=1/fs4)
Y4_mag = np.abs(Y4) / N4
mask4 = freqs4 >= 0

print(f"~~~ Часть 7 ~~~")
# Память
print(f"Память для fs=320: {N4 * 8} байт = {N4 * 8 / 1024:.2f} КБ")

plt.figure(figsize=(10, 4))
plt.stem(freqs4[mask4], Y4_mag[mask4], basefmt=' ')
plt.title('Амплитудный спектр (fs = 320 Гц, N = 320)')
plt.xlabel('f, Гц')
plt.ylabel('|Y(f)|')
plt.grid(True)
plt.tight_layout()
plt.savefig('fig6_fft_320.png', dpi=150)
plt.show()

# Восстановление
plt.figure(figsize=(10, 4))
plt.plot(t_continuous, y_continuous, 'b-', linewidth=2, label='Оригинал')
plt.plot(t_sampled4, y_sampled4, 'r.-', linewidth=1, markersize=4,
         label='Восстановленный (fs = 320 Гц)')
plt.title('Сравнение оригинала и восстановленного (fs = 320 Гц)')
plt.xlabel('t, с')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('fig7_reconstruction_320.png', dpi=150)
plt.show()