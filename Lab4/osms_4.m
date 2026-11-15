% Параметры
L = 31; 
x_seed = [0 0 1 0 0];
y_seed = [0 1 0 1 1];

% Генерация 1-й последовательности
x = x_seed; y = y_seed;
seq1 = zeros(1, L);

for i = 1:L
    seq1(i) = xor(x(end), y(end)); % Выход
    fb_x = xor(x(end-1), x(end));  % Обратная связь x
    fb_y = xor(y(end-1), y(end));  % Обратная связь y

    x = [fb_x, x(1:end-1)]; % Сдвиг
    y = [fb_y, y(1:end-1)]; % Сдвиг
end

% Вывод последовательности в командное окно
disp('Последовательность 1:');
disp(seq1);

% Вычисление автокорреляции с помощью встроенной функции
% Заменяем 0 на -1 для корректного математического расчета корреляции
seq1_bipolar = 2*seq1 - 1; 
[acf, lags] = xcorr(seq1_bipolar, 'normalized'); % 'normalized' дает макс пик = 1

% Построение графика автокорреляции
figure;
stem(lags, acf, 'filled');
title('Автокорреляционная функция (АКФ)');
xlabel('Сдвиг (lag)');
ylabel('Нормированная корреляция');
grid on;

% Генерация 2-й последовательности (x=5, y=6)
x2_seed = [0 0 1 0 1];
y2_seed = [0 0 1 1 0];
x = x2_seed; y = y2_seed;
seq2 = zeros(1, L);
for i = 1:L
    seq2(i) = xor(x(end), y(end));
    fb_x = xor(x(end-1), x(end));
    fb_y = xor(y(end-1), y(end));
    x = [fb_x, x(1:end-1)];
    y = [fb_y, y(1:end-1)];
end

% Вычисление взаимной корреляции
seq2_bipolar = 2*seq2 - 1;
[ccf, lags_ccf] = xcorr(seq1_bipolar, seq2_bipolar, 'normalized');

% Построение графика взаимной корреляции
figure;
stem(lags_ccf, ccf, 'filled');
title('Взаимная корреляционная функция (ВКФ)');
xlabel('Сдвиг (lag)');
ylabel('Нормированная корреляция');
grid on;