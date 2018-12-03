import math


class Kinematics:

    def __init__(self):
        # Размеры робота
        self.e = 115.389  # Радиус окружности нижнего треугольника 33.31 в мм
        self.f = 450.333  # Радиус окружности верхенго треугольника 130 в мм
        self.re = 550  # Длина предплечья в мм
        self.rf = 195.385  # Длина бицепса в мм

        self.theta = 0
        self.theta1 = 0
        self.theta2 = 0
        self.theta3 = 0
        self.x0 = 0
        self.y0 = 0
        self.z0 = 0
        self.x0_rotated = 0
        self.y0_rotated = 0

        self.sin120 = math.sin(math.radians(120))
        self.cos120 = math.cos(math.radians(120))
        self.tan60 = math.tan(math.radians(60))
        self.sin30 = math.sin(math.radians(30))
        self.tan30 = math.tan(math.radians(30))

    # Прямая кинематика
    def delta_calc_forward(self):
        self.theta1 *= -1
        self.theta2 *= -1
        self.theta3 *= -1

        t = (self.f - self.e) * self.tan30 / 2

        y1 = -(t + self.rf * math.cos(math.radians(self.theta1)))
        z1 = -self.rf * math.sin(math.radians(self.theta1))

        y2 = (t + self.rf * math.cos(math.radians(self.theta2))) * self.sin30
        x2 = y2 * self.tan60
        z2 = -self.rf * math.sin(math.radians(self.theta2))

        y3 = (t + self.rf * math.cos(math.radians(self.theta3))) * self.sin30
        x3 = -y3 * self.tan60
        z3 = -self.rf * math.sin(math.radians(self.theta3))

        dnm = (y2 - y1) * x3 - (y3 - y1) * x2

        w1 = y1 * y1 + z1 * z1
        w2 = x2 * x2 + y2 * y2 + z2 * z2
        w3 = x3 * x3 + y3 * y3 + z3 * z3

        # x = (a1 * z + b1) / dnm
        a1 = (z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)
        b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2.0

        # y = (a2 * z + b2) / dnm
        a2 = -(z2 - z1) * x3 + (z3 - z1) * x2
        b2 = ((w2 - w1) * x3 - (w3 - w1) * x2) / 2.0

        # a * z ^ 2 + b * z + c = 0
        a = a1 * a1 + a2 * a2 + dnm * dnm
        b = 2 * (a1 * b1 + a2 * (b2 - y1 * dnm) - z1 * dnm * dnm)
        c = (b2 - y1 * dnm) * (b2 - y1 * dnm) + b1 * b1 + dnm * dnm * (z1 * z1 - self.re * self.re)

        # дискриминант
        d = b * b - 4.0 * a * c
        if d < 0:
            print('Несуществующая позиция')
            return -1  # несуществующая позиция

        self.z0 = -0.5 * (b + math.sqrt(d)) / a
        self.x0 = (a1 * self.z0 + b1) / dnm
        self.y0 = (a2 * self.z0 + b2) / dnm
        print('x = ' + self.x0.__str__() + '; y = ' + self.y0.__str__() + '; z = ' + self.z0.__str__())
        return 0

    def delta_calc_angle_yz(self, x0, y0, z0):
        rf = self.rf
        re = self.re
        y1 = -(self.f / 2 * self.tan30)  # f / 2 * tg30
        y0 -= self.e / 2 * self.tan30  # сдвигаем центр к краю
        # z = a + b * y
        a = (x0 * x0 + y0 * y0 + z0 * z0 + rf * rf - re * re - y1 * y1) / (2 * z0)
        b = (y1 - y0) / z0

        # дискриминант
        d = -(a + b * y1) * (a + b * y1) + rf * (b * b * rf + rf)
        if d < 0:
            print('несуществующая точка')
            return 65535  # несуществующая точка
        yj = (y1 - a * b - math.sqrt(d)) / (b * b + 1)  # выбираем внешнюю точку
        zj = a + b * yj
        theta = math.degrees(math.atan(zj / (y1 - yj)))
        return theta

    # обратная кинематика: (x0, y0, z0) -> (theta1, theta2, theta3)
    # возвращаемый статус: 65535 = несуществующая позиция
    def delta_calc_inverse(self):
        self.theta = self.theta1 = self.theta2 = self.theta3 = 0
        self.theta1 = self.delta_calc_angle_yz(self.x0, self.y0, self.z0)

        if self.theta1 != 65535:
            # rotate coords to +120 deg
            self.x0_rotated = self.x0 * self.cos120 + self.y0 * self.sin120
            self.y0_rotated = self.y0 * self.cos120 - self.x0 * self.sin120
            self.theta2 = self.delta_calc_angle_yz(self.x0_rotated, self.y0_rotated, self.z0)
        if self.theta2 != 65535:
            # rotate coords to -120 deg
            self.x0_rotated = self.x0*self.cos120 - self.y0*self.sin120
            self.y0_rotated = self.y0*self.cos120+self.x0*self.sin120
            self.theta3 = self.delta_calc_angle_yz(self.x0_rotated, self.y0_rotated, self.z0)
        # print('t1 =', round(self.theta1, 2), end=' | ')
        # print('t2 =', round(self.theta2, 2), end=' | ')
        # print('t1 =', round(self.theta3, 2))
        return 0

    def pick_and_place(self, xy, ):
        zyz = xy[0]
        zyz += 1
        return zyz
if __name__ == '__main__':
    robot = Kinematics()
    robot.x0 = float(input())
    robot.y0 = float(input())
    robot.z0 = float(input())


#    robot.theta1 = float(input())
#    robot.theta2 = float(input())
#    robot.theta3 = float(input())

    robot.delta_calc_inverse()
#    robot.delta_calc_forward()
