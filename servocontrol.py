import serial
import math


class Servo:
    def __init__(self):
        self.port = 0

        self.usecMin1 = 245
        self.usecMax1 = 2375
        self.degMin1 = 0
        self.degMax1 = 180
        self.nullPoint1 = 1260

        self.usecMin2 = 317
        self.usecMax2 = 2255
        self.degMin2 = 0
        self.degMax2 = 180
        self.nullPoint2 = 1250

        self.usecMin3 = 192
        self.usecMax3 = 2330
        self.degMin3 = 0
        self.degMax3 = 180
        self.nullPoint3 = 1260

        self.theta1_correction = 0
        self.theta2_correction = 0
        self.theta3_correction = 0
        # self.theta1_correction = -10
        # self.theta2_correction = -16.7
        # self.theta3_correction = -12

    # Открытие COM1 порта для отправки углов
    def connect_servo(self):
        self.port = serial.Serial(
            port='COM9',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

    def cmd(self, theta1, theta2, theta3):
        buff = str(math.ceil(self.deg_to_usec1(theta1 - self.theta1_correction))) + ';' + \
               str(math.ceil(self.deg_to_usec2(theta2 - self.theta2_correction))) + ';' + \
               str(math.ceil(self.deg_to_usec3(theta3 - self.theta3_correction))) + ';' + '\n'
        print(buff)
        self.port.write(buff.encode('ascii'))
        # self.deg_to_usec(theta1)

    def deg_to_usec1(self, theta):
        if theta < 0:
            return (self.usecMax1 - self.usecMin1) * theta * -1 / self.degMax1 + self.nullPoint1
        if theta > 0:
            return self.nullPoint1 - ((self.usecMax1 - self.usecMin1) * theta / self.degMax1)
        if theta == 0:
            return self.nullPoint1

    def deg_to_usec2(self, theta):
        if theta < 0:
            return (self.usecMax2 - self.usecMin2) * theta * -1 / self.degMax2 + self.nullPoint2
        if theta > 0:
            return self.nullPoint2 - ((self.usecMax2 - self.usecMin2) * theta / self.degMax2)
        if theta == 0:
            return self.nullPoint2

    def deg_to_usec3(self, theta):
        if theta < 0:
            return (self.usecMax3 - self.usecMin3) * theta * -1 / self.degMax3 + self.nullPoint3
        if theta > 0:
            return self.nullPoint3 - ((self.usecMax3 - self.usecMin3) * theta / self.degMax3)
        if theta == 0:
            return self.nullPoint3

    def read(self):
        cc = str(self.port.readline())
        print(cc[2:][:-5])
        cc = str(self.port.readline())
        print(cc[2:][:-5])
        cc = str(self.port.readline())
        print(cc[2:][:-5])
        cc = str(self.port.readline())
        print(cc[2:][:-5])
        cc = str(self.port.readline())
        print(cc[2:][:-5])
        cc = str(self.port.readline())
        print(cc[2:][:-5])
        cc = str(self.port.readline())
        print(cc[2:][:-5])
        cc = str(self.port.readline())
        print(cc[2:][:-5])
        cc = str(self.port.readline())
        print(cc[2:][:-5])

