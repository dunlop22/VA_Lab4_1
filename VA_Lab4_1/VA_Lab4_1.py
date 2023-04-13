import numpy as np
import matplotlib.pyplot as plt
import math
import getch
x1 = []
x_ = []
y1 = []
y_ = []

def print_znach(x1, y1):
    print("Значения X:    ", end = "")
    print_table(x1)
    print("Значения Y:    ", end = "")
    print_table(y1)
    

def print_table(st):
    for i in range(len(st)):
        drop = 3
        print(str(st[i]), end = "")
        
        if abs(st[i]) >= 100:
            drop = drop - 2
        elif abs(st[i]) >= 100:
            drop = drop - 1
        for g in range (drop):
          print(" ", end = " ") 
    print("\n")


##чтение файла со значениями
def read_file():
    return


#вычисление значений функции
def count_function(xs, func):
    ys = []
    for i in range(len(xs)):
        x = xs[i]
        ys.append(eval(func))
    return ys


##максимальное отклонение
def count_raznosti(iy, fy):
    raznosti = [[0, 0, 0]]
    k = 0

    for i in range(len(iy)):
        r = fy[i] - iy[i]
        if abs(r) > abs(raznosti[0][2]):
            raznosti[0][2] = r
            raznosti[0][0] = i
            raznosti[0][1] = fy[i]

    for i in range(len(iy)):
        r = fy[i] - iy[i]
        if abs(r) == abs(raznosti[0][2]) and i != raznosti[0][0]:
            raznosti.append([])
            k += 1
            raznosti[k].append(i)
            raznosti[k].append(fy[i])
            raznosti[k].append(r)

    return raznosti


##метод прогонки

#метод прогонки
def progonka(h, x1, y1):

    n = len(x1) - 1

    a = []
    b = []

    for k in range(n - 1):
        i = k + 1

        a.append([])
        
        if k == 0:
            a[k].append(0)
        else:
            a[k].append(h[k])

        a[k].append(2 * (h[k] + h[k + 1]))
        
        if k == n - 2:
            a[k].append(0)
        else:
            a[k].append(h[k + 1])

        b.append(6 * ((y1[i + 1] - y1[i]) / h[k + 1] - (y1[i] - y1[i - 1]) / h[k]))

    #прямой ход
    v = []
    u = []

    v.append(a[0][2] / a[0][1] * (-1))
    u.append(b[0] / a[0][1])
    
    for i in range(1, n - 2):
        v.append(a[i][2] / (a[i][1] * (-1) - a[i][0] * v[i - 1]))
        u.append((a[i][0] * u[i - 1] - b[i]) / (a[i][1] * (-1) - a[i][0] * v[i - 1]))

    v.append(0)
    u.append((a[n - 2][0] * u[n - 3] - b[n - 2]) / (a[n - 2][1] * (-1) - a[n - 2][0] * v[n - 3]))
    

    #обратный ход
    x = []

    x.append(u[n - 2])

    for i in range(n - 2):
        x.append(v[n - i - 3] * x[i] + u[n - i - 3])

    x.reverse()

    return x



#вычисление значения для интерполяции
def countS(a, b, c, d, xi, x):
    return a + b * (x - xi) + pow(x - xi, 2) * c / 2 + pow(x - xi, 3) * d / 6

#вычисление значений для интерполяции
def count_Splain(xs, b, c, d, x1, y1):
    k = len(xs)
    n = len(x1) - 1
    ys = np.zeros(k)
    i = 0
    
    for j in range(k):
        if xs[j] >= x1[i] and i < n:
            i += 1
        ys[j] = countS(y1[i], b[i - 1], c[i], d[i - 1], x1[i], xs[j])
    return ys




#первый вариант работы программы
def functional_1():
    
    read_file()
    n = len(x1) - 1
    ag = x1[0]
    bg = x1[n]

    while(True):
        print('Введите x: ', end='')
        xzn = float(input())

        if xzn >= ag and xzn <= bg:
            break


    h = []
    for i in range(n):
        h.append(x1[i + 1] - x1[i])

    c = progonka(h, x1, y1)
    c.append(0)
    c.insert(0, 0)

    d = []
    b = []

    for i in range(n):
        d.append((c[i + 1] - c[i]) / h[i])
        b.append((h[i] * c[i + 1]) / 2 - d[i] * pow(h[i], 2) / 6 + (y1[i + 1] - y1[i]) / h[i])


    for i in range(n):
        if xzn >= x1[i] and xzn <= x1[i + 1]:
            result = countS(y1[i + 1], b[i], c[i + 1], d[i], x1[i + 1], xzn)
            break

    print('\nИскомое значение: ', result)

    xt = []
    yt = []

    for i in range(len(x1)):
        xt.append(x1[i])
        yt.append(y1[i])

    x = np.arange(x1[0], x1[len(x1) - 1], 0.001)
    plt.plot(x, count_Splain(x,  b, c, d, x1, y1), 'm')
    plt.plot(xt, yt, 'bo')
    plt.plot(xzn, result, 'ro')
    plt.grid(True)

    plt.xlabel(r'$x$', fontsize=14)
    plt.ylabel(r'$y$', fontsize=14)

    plt.show()

    return

#второй вариант работы прораммы
def functional_2():
    print('Введите функцию: y = ', end='')
    func = input()
    print('\n')

    for i in range(len(x_)):
        x = x_[i]
        y_.append(eval(func))
        print('x = ', x_[i], '   y = ', y_[i], sep='')

    n = len(x_) - 1

    h = []
    for i in range(n):
        h.append(x_[i + 1] - x_[i])

    c = progonka(h, x_, y_)
    c.append(0)
    c.insert(0, 0)

    d = []
    b = []

    for i in range(n):
        d.append((c[i + 1] - c[i]) / h[i])
        b.append((h[i] * c[i + 1]) / 2 - d[i] * pow(h[i], 2) / 6 + (y_[i + 1] - y_[i]) / h[i])

    xt = []
    yt = []

    for i in range(len(x_)):
        xt.append(x_[i])
        yt.append(y_[i])

    x = np.arange(x_[0], x_[len(x_) - 1], 0.001)

    sy = count_Splain(x, b, c, d, x_, y_)
    plt.plot(x, sy, 'm')

    fy = count_function(x, func)
    plt.plot(x, fy, 'c', label=r'f(x)')

    plt.plot(xt, yt, 'bo')
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)

    plt.xlabel(r'$x$', fontsize=14)
    plt.ylabel(r'$y$', fontsize=14)

    razn = count_raznosti(sy, fy)   ##вычисление разности
        
    for i in range(len(razn)):
        razn[i][0] = x_[0] + razn[i][0] * 0.001
        
    print('\n\nМаксимальное отклонение: ', abs(razn[0][2]))
    plt.show()
    return

    
while True:
    while True:
        print('1) Определить приближённое значение функции в точке по таблице\n2) Вычислить таблицу значений функции  по заданной аналитически функции y = f(x)\n\nРежим: ', end='')
        functional = input()

        with open("file.txt", "r") as file:
            temp = file.readline()  
        
            x1 = [float(t) for t in temp.split()]
            temp = file.readline()
            y1 = [float(t) for t in temp.split()]
            temp = file.readline()
            x_ = [float(t) for t in temp.split()]
            x_.sort()       ##сортировка значений в массиве
    
        file.close()   ##закрытие файла


        ##сортировка методом пузырька
        for i in range(len(x1)-1):
            for j in range(len(x1)-i-1):
                if x1[j] > x1[j+1]:
                    x1[j], x1[j+1] = x1[j+1], x1[j]
                    y1[j], y1[j+1] = y1[j+1], y1[j]
        print_znach(x1, y1)

        print('\n')
        if len(functional) == 1 and (functional[0] == '1' or functional[0] == '2'):
            if functional == '1':
                functional_1()
            else:
                functional_2()
            break
    print('\n\nЧтобы продолжить нажмите Enter. Для выхода из программы нажмите любую другую клавишу. ', end='')
    cont = getch.getch()
   
    if cont == '\n' or cont == b'\r':
        print('\n\n')
    else:
        break
