#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <iomanip>

using namespace std;

// Функция для вычисления остатка (CRC) от деления по модулю 2
string calculate_crc(string data, string poly) {
    int poly_len = poly.length();
    string padded_data = data + string(poly_len - 1, '0');
    string remainder = padded_data;
    
    // Выполняем деление в столбик с помощью XOR
    for (int i = 0; i <= remainder.length() - poly_len; i++) {
        if (remainder[i] == '1') {
            for (int j = 0; j < poly_len; j++) {
                remainder[i + j] = (remainder[i + j] == poly[j]) ? '0' : '1';
            }
        }
    }
    return remainder.substr(remainder.length() - (poly_len - 1));
}

// Функция проверки пакета на ошибки
bool check_crc(string packet, string poly) {
    int poly_len = poly.length();
    string temp = packet;
    
    for (int i = 0; i <= temp.length() - poly_len; i++) {
        if (temp[i] == '1') {
            for (int j = 0; j < poly_len; j++) {
                temp[i + j] = (temp[i + j] == poly[j]) ? '0' : '1';
            }
        }
    }
    // Если остаток не нулевой - есть ошибка
    for (int i = temp.length() - (poly_len - 1); i < temp.length(); i++) {
        if (temp[i] == '1') return false;
    }
    return true;
}

int main() {
    string poly = "11110111";
    
    cout << "~~~ Пункт 1-3: Работа с пакетом длиной 24 бита ~~~" << endl;
    string data_24 = "101100111000111100001111";
    cout << "Исходные данные (24 бита): " << data_24 << endl;
    cout << "Порождающий полином:      " << poly << endl;
    
    string crc = calculate_crc(data_24, poly);
    cout << "Вычисленный CRC (7 бит):  " << crc << endl;
    
    string packet_24 = data_24 + crc;
    cout << "Пакет для передачи:       " << packet_24 << endl;
    
    bool is_error_24 = !check_crc(packet_24, poly);
    cout << "Проверка на приемнике:    " << (is_error_24 ? "ОШИБКА!" : "Ошибок нет (ОК)") << endl << endl;

    cout << "~~~ Пункт 4-5: Работа с пакетом 250 бит и искажение бит ~~~" << endl;
    
    // Генерируем случайные 250 бит
    srand(time(0));
    string data_250 = "";
    for (int i = 0; i < 250; i++) {
        data_250 += to_string(rand() % 2);
    }
    
    string crc_250 = calculate_crc(data_250, poly);
    string packet_250 = data_250 + crc_250; // Полный пакет (257 бит)
    
    cout << "Длина исходных данных: 250 бит" << endl;
    cout << "Длина пакета с CRC:    " << packet_250.length() << " бит" << endl;
    cout << "Начинаем цикл искажения каждого бита..." << endl;
    
    int detected = 0;
    int undetected = 0;
    
    // Цикл по всем битам пакета (250 + 7 = 257 итераций)
    for (int i = 0; i < packet_250.length(); i++) {
        string corrupted_packet = packet_250;
        // Инвертируем (искажаем) i-й бит
        corrupted_packet[i] = (corrupted_packet[i] == '0') ? '1' : '0';
        
        // Проверяем на приемнике
        if (!check_crc(corrupted_packet, poly)) {
            detected++;
        } else {
            undetected++;
        }
    }
    
    cout << "\nРезультаты теста:" << endl;
    cout << "Всего искажений (итераций): " << packet_250.length() << endl;
    cout << "Обнаружено ошибок:          " << detected << endl;
    cout << "НЕ обнаружено ошибок:       " << undetected << endl;
    
    return 0;
}