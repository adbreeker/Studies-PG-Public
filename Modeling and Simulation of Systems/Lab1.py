"""
Laboratory Class 1: 
Body moving in a uniform gravitational field
"""

import random
import matplotlib.pyplot as plt

import numpy as np

g = 10
N = 100000

v0_min = 1
v0_max = 30
alfa_min = 1
alfa_max = 89   

R1_y = 5
R1_x_min = 4
R1_x_max = 5 # not crossed

R2_y = 5
R2_x_min = 7
R2_x_max = 10 # not crossed

R3_x = 2
R3_y_min = 2
R3_y_max = 8 # crossed

R4_x = 11
R4_y_min = 3
R4_y_max = 7 # crossed

g_v0 = []
dobre_alfa = []
t_maxy = []
licznik = 0

t_max_max = 0

if __name__ == "__main__":
    for i in range(0,N):
        v0 = random.uniform(v0_min,v0_max)
        alfa = random.uniform(alfa_min,alfa_max)
        alfa_rad = np.deg2rad(alfa)
        v0x = v0 * np.cos(alfa_rad)
        v0y = v0 * np.sin(alfa_rad)
        t_max = 2 * v0y / g

        # R1
        delta =v0y**2 - 4*(-1/2)*g * -5
        if delta>0:
            t1 = (-v0y - np.sqrt(delta))/(-g)
            t2 = (-v0y + np.sqrt(delta)) / (-g)

            x1 = v0x * t1
            x2 = v0x * t2
            if 4 <= x1 <= 5:
                continue

            if 4 <= x2 <= 5:
                continue

        # R2
        delta = v0y ** 2 - 4 * (-1 / 2) * g * -5
        if delta > 0:
            t1 = (-v0y - np.sqrt(delta)) / (-g)
            t2 = (-v0y + np.sqrt(delta)) / (-g)

            x1 = v0x * t1
            x2 = v0x * t2
            if 7 <= x1 <= 10:
                continue

            if 7 <= x2 <= 10:
                continue

        # R3
        t= 2/v0x

        y = v0y*t - (1/2)*g*(t**2)
        if not (2 < y < 8):
            continue

        #R4
        t = 11 / v0x
        y = v0y * t - (1 / 2) * g * (t ** 2)
        if not (3 < y < 7):
            continue

        dobre_alfa.append(np.deg2rad(alfa))
        g_v0.append(v0)
        licznik += 1
        t_maxy.append(t_max)

    for i in range(0,5):
        x = np.linspace(0,40, 10000)
        y = -1/2 * g * (1/ (g_v0[i]*np.cos(dobre_alfa[i]))**2) * (x**2) + np.tan(dobre_alfa[i])*x
        mask = y > 0
        plt.plot(x[mask],y[mask], color='cyan')

    plt.draw()

    x1, y1 = [4, 5], [5, 5]
    x2, y2 = [7, 10], [5, 5]
    plt.plot(x1, y1, color='red')
    plt.plot(x2, y2, color='red')
    x3, y3 = [2, 2], [2, 8]
    plt.plot(x3, y3, color='green')
    x4, y4 = [11,11], [3, 7]
    plt.plot(x4, y4, color='green')


    print(t_max_max)
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Projectile Trajectories with Obstacles')
    plt.savefig('Resources/Lab1/Projectile_Trajectories.png')
    plt.show()

    print("licznik: ", licznik)
    print('procent: ' +  str(round(licznik/N*100, 2)) + "%")

    plt.scatter(dobre_alfa, g_v0, color='red')
    plt.xlabel('Angle [rad]')
    plt.ylabel('Initial Velocity [m/s]')
    plt.title('Accepted Initial Parameters')
    plt.savefig('Resources/Lab1/Accepted_Parameters.png')
    plt.show()







