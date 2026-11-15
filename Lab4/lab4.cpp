#include <iostream>
#include <vector>
#include <iomanip>
#include <cmath>

using namespace std;

// Функция генерации последовательности Голда
vector<int> generate_gold(vector<int> x_seed, vector<int> y_seed, int length) {
    vector<int> x = x_seed;
    vector<int> y = y_seed;
    vector<int> sequence;
    
    for (int i = 0; i < length; i++) {
        // Выходной бит - это XOR от последних разрядов (x5 и y5)
        int out_bit = x[4] ^ y[4];
        sequence.push_back(out_bit);
        // Обратная связь
        int x_fb = x[3] ^ x[4];
        int y_fb = y[3] ^ y[4];
        // Сдвигаем регистры вправо (от индекса 4 к 1)
        for (int j = 4; j > 0; j--) {
            x[j] = x[j-1];
            y[j] = y[j-1];
        }
        // Записываем новые биты в начало (индекс 0)
        x[0] = x_fb;
        y[0] = y_fb;
    }
    return sequence;
}

// Функция вычисления нормированной автокорреляции
double calc_correlation(const vector<int>& seq1, const vector<int>& seq2) {
    int matches = 0;
    int mismatches = 0;
    int n = seq1.size();
    
    for (int i = 0; i < n; i++) {
        if (seq1[i] == seq2[i]) matches++;
        else mismatches++;
    }
    return (double)(matches - mismatches) / n;
}

// Функция циклического сдвига влево
vector<int> cyclic_shift(const vector<int>& seq, int shift) {
    int n = seq.size();
    vector<int> shifted(n);
    for (int i = 0; i < n; i++) {
        shifted[i] = seq[(i + shift) % n];
    }
    return shifted;
}

int main() {
    vector<int> x_seed = {0, 0, 1, 0, 0};
    vector<int> y_seed = {0, 1, 0, 1, 1};
    int L = 31; // Длина m-последовательности (2^5 - 1)

    // 1. Генерация
    vector<int> gold_seq1 = generate_gold(x_seed, y_seed, L);
    
    cout << "Сгенерированная последовательность Голда (x=4, y=11):" << endl;
    for (int bit : gold_seq1) cout << bit << " ";
    cout << "\n\n";

    // 2. Автокорреляция и таблица
    cout << "Таблица автокорреляции:" << endl;
    cout << "Сдвиг | Первые 5 бит сдвинутой | Автокорреляция" << endl;
    cout << "------------------------------------------------" << endl;
    
    for (int shift = 0; shift < 5; shift++) { // Покажем первые 5 сдвигов для примера
        vector<int> shifted_seq = cyclic_shift(gold_seq1, shift);
        double corr = calc_correlation(gold_seq1, shifted_seq);
        
        cout << setw(5) << shift << " | ";
        for (int i = 0; i < 5; i++) cout << shifted_seq[i] << " ";
        cout << "             | " << fixed << setprecision(2) << corr << endl;
    }
    
    // 3 и 4. Вторая последовательность и взаимная корреляция
    // x = x + 1 = 5 (00101), y = y - 5 = 6 (00110)
    vector<int> x_seed_new = {0, 0, 1, 0, 1};
    vector<int> y_seed_new = {0, 0, 1, 1, 0};
    
    vector<int> gold_seq2 = generate_gold(x_seed_new, y_seed_new, L);
    
    cout << "\nВторая последовательность (x=5, y=6):" << endl;
    for (int bit : gold_seq2) cout << bit << " ";
    cout << "\n\n";
    
    // Взаимная корреляция (без сдвига)
    double cross_corr = calc_correlation(gold_seq1, gold_seq2);
    cout << "Взаимная корреляция исходной и новой последовательностей: " << fixed << setprecision(4) << cross_corr << endl;

    return 0;
}