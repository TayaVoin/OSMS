import numpy as np
import matplotlib.pyplot as plt

P_UE = 24
P_BS = 46
G_BS = 21
G_MIMO = 3
L_feeder = 2.9
IM = 1
Pen = 15
NF_BS = 2.4
NF_UE = 6
SINR_UL = 4
SINR_DL = 2

def calculate_radius(BW_ul_mhz, BW_dl_mhz, f_mhz):
    """ Функция для расчета радиуса соты по модели UMiNLOS при заданных полосах и частоте."""
    f_ghz = f_mhz / 1000.0
    
    # Расчет MAPL для UL
    Therm_UL = -174 + 10 * np.log10(BW_ul_mhz * 1e6)
    RxSens_BS = NF_BS + Therm_UL + SINR_UL
    MAPL_UL = P_UE - L_feeder + G_BS + G_MIMO - IM - Pen - RxSens_BS
    
    # Расчет MAPL для DL
    Therm_DL = -174 + 10 * np.log10(BW_dl_mhz * 1e6)
    RxSens_UE = NF_UE + Therm_DL + SINR_DL
    MAPL_DL = P_BS - L_feeder + G_BS + G_MIMO - IM - Pen - RxSens_UE
    
    # Поиск расстояния (R) для модели UMiNLOS
    R_UL = 10 ** ((MAPL_UL - 26 * np.log10(f_ghz) - 22.7) / 36.7)
    R_DL = 10 ** ((MAPL_DL - 26 * np.log10(f_ghz) - 22.7) / 36.7)
    
    # Итоговый радиус ограничивается наименьшим (UL)
    return min(R_UL, R_DL)

# График 1: Зависимость радиуса от Ширины полосы (BW)
# Фиксируем частоту 1800 МГц. Меняем полосу от 1 до 100 МГц.
# Предположим, что UL и DL полосы одинаковы для чистоты эксперимента.
bw_array = np.linspace(1, 100, 100)
radii_bw = [calculate_radius(bw, bw, 1800) for bw in bw_array]

# График 2: Зависимость радиуса от Несущей частоты (f)
# Фиксируем полосы (UL = 10 МГц, DL = 20 МГц). Меняем частоту от 700 МГц до 3500 МГц.
f_array = np.linspace(700, 3500, 100)
radii_f = [calculate_radius(10, 20, f) for f in f_array]

# --- Построение графиков ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(bw_array, radii_bw, 'b-', linewidth=2)
ax1.set_title('Зависимость радиуса соты от ширины полосы частот')
ax1.set_xlabel('Ширина полосы, МГц')
ax1.set_ylabel('Радиус соты, м')
ax1.grid(True, linestyle='--', alpha=0.7)

ax2.plot(f_array, radii_f, 'r-', linewidth=2)
ax2.set_title('Зависимость радиуса соты от несущей частоты')
ax2.set_xlabel('Несущая частота, МГц')
ax2.set_ylabel('Радиус соты, м')
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('lab2_extra_dependencies.png', dpi=150)
plt.show()