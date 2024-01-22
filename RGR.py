import matplotlib.pyplot as plt
import numpy as np

def crc_create(array):
    G = [1, 0, 0, 0, 0, 1, 1, 1]
    length_array = len(array)
    array += [0] * 7  # добавление 7 нулей
    array = np.array(array)
    for i in range(length_array-1):
        if array[i] == 1:
            array[i:i+8] ^= G
    
    return array[length_array:]

def crc_p(array):
    G = [1, 0, 0, 0, 0, 1, 1, 1]
    length_array = len(array)
    for i in range(length_array-8):
        if array[i] == 1:
            for j in range(8):
                array[i+j] ^= G[j]
    
    return array[-7:]

def gold_create():
    # Вариант 16
    x = [1, 0, 0, 0, 0] 
    y = [1, 0, 1, 1, 1] 
    gold = []
    for i in range(31):
        gold.append(x[4] ^ y[4])
        sum = x[3] ^ x[4]
        x = x[:-1]
        x.insert(0, sum)
        sum = y[1] ^ y[4]
        y = y[:-1]
        y.insert(0, sum)
        
    return list(gold)

def correlate_p(array, posl_g):
    posl_g_x10 = np.repeat(posl_g, 10)
    
    index = np.correlate(array, posl_g_x10, mode='full')
    index = index / (len(posl_g_x10)/2)
    plt.figure(10)
    plt.plot(index)
    index_max = []
    for i in range(len(index)):
        if index[i] > 0.93:
           index_max.append(i) 
    #print(index_max)       
    if len(index_max) == 2:
        max1 = index_max[0]
        max2 = index_max[1]
    else:
        print('Не найдены 2 синхронизации')
    
    #index = np.argmax(index)
    return array[max1:max2]
    
def decod(array):
    decod_bit = []
    for i in range(0, len(array), 10):
        sred = sum(array[i:i+10])
        sred = int(sred) / 10
        if sred > 0.5:
            decod_bit.append(1)
        else:
            decod_bit.append(0)
    
    return decod_bit

name_input = input("Введите ваше имя: ")
sname_input = input("Введите вашу фамилию: ")

# Кодирование в ASCII и запись в массив, преобразование в int
bitpos_input = list(''.join(format(ord(char), '08b') for char in name_input + ' ' + sname_input)) # Добавил пробел
bitpos_input = [int(bit) for bit in bitpos_input]

print('Биты -  ', bitpos_input)

bitpos_copy_input = bitpos_input.copy() # копирование чтобы небыло искажений
crc_input = crc_create(bitpos_copy_input)
print('CRC - ', crc_input)
posl_g_input = gold_create()
print('Gold_posledov - ', posl_g_input)

bitpos_Nx_input = np.concatenate((posl_g_input, bitpos_input, crc_input, posl_g_input))
bitpos_Nx_input = np.repeat(bitpos_Nx_input, 10) # повторение каждого бита

plt.figure(1,figsize=(8,8))
plt.subplot(221)
plt.title("2")
plt.plot(bitpos_input)

plt.subplot(222)
plt.title("5")
plt.plot(bitpos_Nx_input)

index_input = int(input("Введите число до {}: ".format(len(bitpos_Nx_input))))

# Вставка в массив*2
bitpos_Nx_2_input = np.zeros(len(bitpos_Nx_input)*2) # создание пустого массива
bitpos_Nx_2_input[index_input:index_input+len(bitpos_Nx_input)] = bitpos_Nx_input 

noice_input = np.random.uniform(-0.2, 0.2, len(bitpos_Nx_2_input)) 

bitpos_Nx_2_noice_input = bitpos_Nx_2_input + noice_input

plt.subplot(223)
plt.title("6")
plt.plot(bitpos_Nx_2_input)

plt.subplot(224)
plt.title("7")
plt.plot(bitpos_Nx_2_noice_input)

singal_input = correlate_p(bitpos_Nx_2_noice_input, posl_g_input) # сигнал без лишнего в начале
signal_decod_input = decod(singal_input)
signal_decod_input = signal_decod_input[:-31] # убираем gold в конце

check_input = crc_p(signal_decod_input.copy()) # копировние чтобы небыло ошибки
print("Проверка crc: ", check_input)
if 1 in check_input:
    print("Не правльно передалось!!!!")
else:
    signal_decod_input = signal_decod_input[:-7]

print("Получены биты", signal_decod_input)
 
bstr_input = ''.join(str(bit) for bit in signal_decod_input) # в строку

# Делим строку на байты и декодируем в буквы
text_input = ''.join([chr(int(bstr_input[i:i+8], 2)) for i in range(0, len(bstr_input), 8)])

print(text_input)

plt.figure(2,figsize=(8,6))
plt.subplot(211)
plt.title("8")
plt.plot(singal_input)

plt.subplot(212)
plt.title("9")
plt.plot(signal_decod_input)

#### 13 
fft_otpr_input = np.fft.fft(bitpos_Nx_2_input) + 100
fft_pol_input = np.fft.fft(bitpos_Nx_2_noice_input) 
plt.figure(3)
plt.title('Полученный и переданный(с шумом)')
plt.plot(fft_otpr_input)
plt.plot(fft_pol_input)

# Разной длительность на бит
x05_input = np.repeat(bitpos_input, 5)
x1_input = np.repeat(bitpos_input, 10)
x2_input = np.repeat(bitpos_input, 20)

# 05 длинной 1, 2 длинной 1
x05_input = np.concatenate((x05_input, x05_input))
x2_input = x2_input[:len(x1_input)]

t = np.arange(-len(x1_input)/2, len(x2_input)/2)
# ось х в Гц, тк мы передаём сигнал длинной x05_input за 1 сек 
# нормированная частота(будет 1) = наши отсчёты / частота дискретизации
fft_05_input = abs(np.fft.fftshift(np.fft.fft(x05_input)))/len(x05_input) + 0.5
fft_1_input = abs(np.fft.fftshift(np.fft.fft(x1_input)))/len(x05_input) + 0.25
fft_2_input = abs(np.fft.fftshift(np.fft.fft(x2_input)))/len(x05_input)

plt.figure(4)
plt.xlabel('Частота [Гц]')
plt.ylabel('Амплитуда')
plt.title('3 разные по длительности')
plt.plot(t,fft_05_input) 
plt.plot(t,fft_1_input)
plt.plot(t,fft_2_input)

plt.show()
