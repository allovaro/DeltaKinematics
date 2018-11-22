import serial
import math


class Servo:
    def __init__(self):
        self.port = 0
        self.usecMin = 600
        self.usecMax = 2200
        self.degMin = 20
        self.degMax = 110
        self.nullPoint = 1400

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
        buff = 's1;' + str(math.ceil(self.deg_to_usec(theta1))) + ':' + \
               's2;' + str(math.ceil(self.deg_to_usec(theta2))) + ':' + \
               's3;' + str(math.ceil(self.deg_to_usec(theta3)))
        print(buff)
        self.port.write(buff.encode('ascii'))
        self.deg_to_usec(theta1)

    def deg_to_usec(self, theta):
        if theta < 0:
            return (self.usecMax - self.usecMin) * theta * -1 / self.degMax + self.nullPoint
        if theta > 0:
            return self.nullPoint - ((self.usecMax - self.usecMin) * theta / self.degMax)
        if theta == 0:
            return self.nullPoint

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

