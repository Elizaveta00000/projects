
import numpy as np
import matplotlib.pyplot as plt
from numpy.array_api import arange


fi = 35*np.pi/180      # угол фи равен ±35 градусов 26′
alpha = 45*np.pi/180   # угол альфа равен ±45 градусов

Matr = [[np.cos(alpha), np.sin(fi) * np.sin(alpha),  0, 0], #матрица аксонометрической проекции
        [0,                   np.sin(alpha),         0, 0],
        [np.sin(alpha), -np.sin(fi) * np.cos(alpha), 0, 0],
        [0,                     0,                  0, 1]]




def func1(t,p1,p2,p1_pr,p2_Pr):                                  # кривая Эрмита
    y = (2*t**3-3*t**2+1)*p1 + (3*t**2-2*t**3)*p2 + (t**3-2*t**2+t)*p1_pr + (t**3-t**2)*p2_Pr
    return y


def p2_pr(p1, p2, p3, p4, p1_pr, p4_pr):                             # P2'
    a = float(3 * (float(p4 - p2)) - 12 * (float(p3 - p1)) + 4 * p1_pr + p4_pr) / float(-15)
    return a


def p3_pr(p1, p2, p3, p4, p1_pr, p4_pr):                                # P3'
    b = float(12 * float(p4 - p2) - 3 * float(p3 - p1) + p1_pr + 4 * p4_pr) / float(15)
    return b


Px = [1, 3, 4, 10]   #точки по оси Х
Py = [1, 2, 3, 10]   #точки по оси Y
Pz = [1, 3, 4, 5]   #точки по оси Z


proizv1_array = []      #массив производных первых точек сегментов
proizv2_array = []      #массив производных последних точек сегментов
#в proizv1 добавим производные точек Р1,Р2,Р3, т.к. для соответствующих сегментов они будут начальными
proizv1_array.append(1)                                             #X
proizv1_array.append(p2_pr(Px[0], Px[1], Px[2], Px[3], 1, -1))
proizv1_array.append(p3_pr(Px[0], Px[1], Px[2], Px[3], 1, -1))
proizv1_array.append(1)                                             #Y
proizv1_array.append(p2_pr(Py[0], Py[1], Py[2], Py[3], 1, -1))
proizv1_array.append(p3_pr(Py[0], Py[1], Py[2], Py[3], 1, -1))
proizv1_array.append(1)                                             #Z
proizv1_array.append(p2_pr(Pz[0], Pz[1], Pz[2], Pz[3], 1, -1))
proizv1_array.append(p3_pr(Pz[0], Pz[1], Pz[2], Pz[3], 1, -1))
#в proizv2 добавим производные точек Р2,Р3,Р4, т.к. для соответствующих сегментов они будут конечными
proizv2_array.append(p2_pr(Px[0], Px[1], Px[2], Px[3], 1, -1))    #X
proizv2_array.append(p3_pr(Px[0], Px[1], Px[2], Px[3], 1, -1))
proizv2_array.append(-1)
proizv2_array.append(p2_pr(Py[0], Py[1], Py[2], Py[3], 1, -1))     #Y
proizv2_array.append(p3_pr(Py[0], Py[1], Py[2], Py[3], 1, -1))
proizv2_array.append(-1)
proizv2_array.append(p2_pr(Pz[0], Pz[1], Pz[2], Pz[3], 1, -1))     #Z
proizv2_array.append(p3_pr(Pz[0], Pz[1], Pz[2], Pz[3], 1, -1))
proizv2_array.append(-1)



fig = plt.figure()                          #задание поля для отрисовки
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x')  # подпись оси x
ax.set_ylabel('y')  # подпись оси y
ax.set_zlabel('z')  # подпись оси z


x_array=[]     #массивы для запоминания координат точек составной кривой Эрмита
y_array=[]     #понадобятся для построения поверхности вращения
z_array=[]


for i in range (0,3,1):     #построение составной кривой Эрмита
    for t in arange (0, 1, 0.1):
        LineX = np.linspace(func1(t, Px[i], Px[i+1], proizv1_array[i], proizv2_array[i]), \
                               func1(t+0.1, Px[i], Px[i+1], proizv1_array[i], proizv2_array[i]))
        LineY = np.linspace(func1(t, Py[i], Py[i+1], proizv1_array[i+3], proizv2_array[i+3]), \
                               func1(t+0.1, Py[i], Py[i+1], proizv1_array[i+3], proizv2_array[i+3]))
        LineZ = np.linspace(func1(t, Pz[i], Pz[i + 1], proizv1_array[i+6], proizv2_array[i+6]),\
                               func1(t+0.1, Pz[i], Pz[i + 1], proizv1_array[i+6], proizv2_array[i+6]))

        x_array.append(LineX)   #запоминаем полученные координаты
        y_array.append(LineY)
        z_array.append(LineZ)

        ax.plot(LineX, LineY, LineZ, color = 'red')  #отрисовка полученной кривой


x1_array=[]     #массивы для запоминания координат точек поверхности вращения
y1_array=[]
z1_array=[]

for i in range(0, 30, 1):                  #нахождение координат поверхности вращения
    for betta in arange (0, 2*np.pi, np.pi/360):
        x1 = x_array[i]*np.cos(betta)           # X * cos(betta)
        y1 = y_array[i]*np.sin(betta)           # Y * sin(betta)
        z1 = z_array[i]                         # Z ни на что не умножаем, т.к. вращаем вокруг оси Z

        x1_array.append(x1)                     # запоминаем полученные значения
        y1_array.append(y1)
        z1_array.append(z1)
                                                                                #поcтроение поверхности
#ax.plot_wireframe(np.array(x1_array), np.array(y1_array), np.array(z1_array), color='blue', rcount = 10, ccount = 10)
ax.plot_surface(np.array(x1_array), np.array(y1_array), np.array(z1_array), color='blue', antialiased=False)

ax.view_init(elev=35.433333, azim=-45)                      #визуализация в изометрической проекции
plt.show()                              #функция для отображения построеныых элементов

