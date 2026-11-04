import numpy as np
import matplotlib.pyplot as plt

f_mhz = 1800
f_ghz = f_mhz / 1000
f_hz = f_mhz * 1e6
c = 3e8

P_BS = 46       # дБм
P_UE = 24       # дБм
G_BS = 21       # дБи
L_feeder = 2.9  # дБ (2 + 0.4 + 0.5)
G_MIMO = 3      # дБ (2 антенны)
IM = 1          # дБ
Penetration = 15 # дБ

BW_UL = 10e6    # Гц
BW_DL = 20e6    # Гц
NF_BS = 2.4     # дБ
NF_UE = 6       # дБ
SINR_UL = 4     # дБ
SINR_DL = 2     # дБ

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1. Расчет бюджета UL (MAPL_UL)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ThermalNoise_UL = -174 + 10 * np.log10(BW_UL)
RxSens_BS = NF_BS + ThermalNoise_UL + SINR_UL
MAPL_UL = P_UE - L_feeder + G_BS + G_MIMO - IM - Penetration - RxSens_BS

print(f"~~~ Пункт 1: Бюджет UL ~~~")
print(f"Тепловой шум UL: {ThermalNoise_UL:.2f} дБм")
print(f"Чувствительность БС: {RxSens_BS:.2f} дБм")
print(f"MAPL_UL: {MAPL_UL:.2f} дБ\n")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. Расчет бюджета DL (MAPL_DL)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ThermalNoise_DL = -174 + 10 * np.log10(BW_DL)
RxSens_UE = NF_UE + ThermalNoise_DL + SINR_DL
MAPL_DL = P_BS - L_feeder + G_BS + G_MIMO - IM - Penetration - RxSens_UE

print(f"~~~ Пункт 2: Бюджет DL ~~~")
print(f"Тепловой шум DL: {ThermalNoise_DL:.2f} дБм")
print(f"Чувствительность UE: {RxSens_UE:.2f} дБм")
print(f"MAPL_DL: {MAPL_DL:.2f} дБ\n")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3. Модели распространения
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Задаем массив расстояний от 10 метров до 10 км
d_m = np.logspace(1, 4, 500) 
d_km = d_m / 1000

# 3.1. FSPM
PL_FSPM = 20 * np.log10(4 * np.pi * d_m * f_hz / c)

# 3.2. UMiNLOS
PL_UMi = 26 * np.log10(f_ghz) + 22.7 + 36.7 * np.log10(d_m)

# 3.3. COST 231 Hata (Urban)
h_BS = 30
h_ms = 1.5
A = 46.33
B = 33.9
a_hms = 3.2 * (np.log10(11.75 * h_ms))**2 - 4.97
s = (47.88 + 13.9 * np.log10(f_mhz) - 13.9 * np.log10(h_BS)) / np.log10(50)

PL_Hata = A + B * np.log10(f_mhz) - 13.82 * np.log10(h_BS) - a_hms + s * np.log10(d_km) + 0

plt.figure(figsize=(12, 6))
plt.plot(d_m, PL_FSPM, 'k--', label='FSPM')
plt.plot(d_m, PL_UMi, 'b-', label='UMiNLOS (Микросоты)')
plt.plot(d_m, PL_Hata, 'g-', label='COST 231 Hata (Макросоты)')

plt.axhline(y=MAPL_UL, color='r', linestyle='-.', label=f'MAPL_UL ({MAPL_UL:.1f} дБ)')
plt.axhline(y=MAPL_DL, color='m', linestyle='-.', label=f'MAPL_DL ({MAPL_DL:.1f} дБ)')

plt.xscale('log')
plt.xlabel('Расстояние, м (лог. шкала)')
plt.ylabel('Потери сигнала, дБ')
plt.title('Зависимость потерь радиосигнала от расстояния')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('lab2_models.png', dpi=150)
plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 4. Определение радиуса и количества БС
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def find_intersection(mapl, d_array, pl_array):
    """Функция для нахождения расстояния, где PL = MAPL"""
    idx = np.argmin(np.abs(pl_array - mapl))
    return d_array[idx]

# ~~~ Для микро/фемтосот (UMiNLOS) ~~~
d_UL_micro = find_intersection(MAPL_UL, d_m, PL_UMi)
d_DL_micro = find_intersection(MAPL_DL, d_m, PL_UMi)
R_micro = min(d_UL_micro, d_DL_micro)
# Площадь одной 3-секторной БС (1.95 * R^2), R в км
S_micro = 1.95 * (R_micro / 1000)**2
N_micro = np.ceil(4 / S_micro)

print(f"~~~ Пункт 4: Результаты ~~~")
print(f"[Микросоты] Радиус UL: {d_UL_micro:.2f} м, Радиус DL: {d_DL_micro:.2f} м")
print(f"[Микросоты] Радиус соты (R): {R_micro:.2f} м")
print(f"[Микросоты] Площадь 1 БС: {S_micro:.2f} кв. км")
print(f"[Микросоты] Требуется БС для 4 кв. км: {N_micro:.0f} шт.\n")

# ~~~ Для макросот (COST 231) ~~~
d_UL_macro = find_intersection(MAPL_UL, d_m, PL_Hata)
d_DL_macro = find_intersection(MAPL_DL, d_m, PL_Hata)
R_macro = min(d_UL_macro, d_DL_macro)
S_macro = 1.95 * (R_macro / 1000)**2
N_macro = np.ceil(100 / S_macro)

print(f"[Макросоты] Радиус UL: {d_UL_macro:.2f} м, Радиус DL: {d_DL_macro:.2f} м")
print(f"[Макросоты] Радиус соты (R): {R_macro:.2f} м")
print(f"[Макросоты] Площадь 1 БС: {S_macro:.2f} кв. км")
print(f"[Макросоты] Требуется БС для 100 кв. км: {N_macro:.0f} шт.")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 5. Дополнительная визуализация для отчета
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# ~~~ График для Микросот (UMiNLOS) ~~~
ax1.plot(d_m, PL_UMi, 'b-', label='UMiNLOS')
ax1.axhline(y=MAPL_UL, color='r', linestyle='--', label=f'MAPL_UL ({MAPL_UL:.1f} дБ)')
ax1.axhline(y=MAPL_DL, color='m', linestyle='--', label=f'MAPL_DL ({MAPL_DL:.1f} дБ)')
ax1.axvline(x=d_UL_micro, color='r', linestyle=':', label=f'R_UL = {d_UL_micro:.0f} м')
ax1.axvline(x=d_DL_micro, color='m', linestyle=':', label=f'R_DL = {d_DL_micro:.0f} м')
ax1.set_xscale('log')
ax1.set_xlim(10, 3000)
ax1.set_ylim(60, 160)
ax1.set_title('Микросоты (UMiNLOS)')
ax1.set_xlabel('Расстояние, м')
ax1.set_ylabel('Потери, дБ')
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend()

# ~~~ График для Макросот (COST 231) ~~~
ax2.plot(d_m, PL_Hata, 'g-', label='COST 231 Hata')
ax2.axhline(y=MAPL_UL, color='r', linestyle='--', label=f'MAPL_UL ({MAPL_UL:.1f} дБ)')
ax2.axhline(y=MAPL_DL, color='m', linestyle='--', label=f'MAPL_DL ({MAPL_DL:.1f} дБ)')
ax2.axvline(x=d_UL_macro, color='r', linestyle=':', label=f'R_UL = {d_UL_macro:.0f} м')
ax2.axvline(x=d_DL_macro, color='m', linestyle=':', label=f'R_DL = {d_DL_macro:.0f} м')
ax2.set_xscale('log')
ax2.set_xlim(10, 3000)
ax2.set_ylim(60, 160)
ax2.set_title('Макросоты (COST 231 Hata)')
ax2.set_xlabel('Расстояние, м')
ax2.set_ylabel('Потери, дБ')
ax2.grid(True, which="both", ls="--", alpha=0.5)
ax2.legend()

plt.tight_layout()
plt.savefig('lab2_intersections.png', dpi=150)
plt.show()