from kinematicsinverse import Kinematics
from detection import Detection
from servocontrol import Servo
import time
import math

svr = Servo()
sd = Detection()
ki = Kinematics()
frame = sd.countours1()

# while True:
#     frame = sd.countours1()
#     center = sd.detection_process(frame)

svr.connect_servo()
# svr.read()
# ki.x0 = 250
# ki.y0 = 250
# ki.z0 = -450
ki.x0 = 0
ki.y0 = 0
ki.z0 = -565
ki.theta1 = 0
ki.theta2 = 0
ki.theta3 = 0
ki.delta_calc_inverse()
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
my_coordin = [0, 1, 2, 3]
while True:
    ki.y0 = 0
    ki.x0 = 0
    ki.z0 = -550
    ki.delta_calc_inverse()
    svr.cmd(ki.theta1, ki.theta2, ki.theta3)
    time.sleep(3)
    ki.y0 = -150
    ki.x0 = 0
    ki.z0 = -550
    ki.delta_calc_inverse()
    svr.cmd(ki.theta1, ki.theta2, ki.theta3)
    time.sleep(3)
r = 100
deg = 1
fwdMove = True
revMove = False
z1 = -565
x1 = -130
z2 = -565
x2 = 200
z3 = -400
x3 = 50
a = (z3 - ((x3 * (z2 - z1) + x2 * z1 - x1 * z1) / (x2 - x1))) / (x3 * (x3 - x1 - x2) + x1 * x2)
b = (z2 - z1) / (x2 - x1) - a * (x1 + x2)
c = (x2 * z1 - x1 * z2) / (x2 - x1) + a * x1 * x2
ki.z0 = a * ki.x0 * ki.x0 + b * ki.x0 + c
time.sleep(3)
# print(a, b, c)
while True:
    # ki.x0 = r * math.sin(math.radians(deg))
    # #ki.y0 = ki.x0
    # ki.x0 = r * math.sin(math.radians(90 - deg))
    # ki.z0 -= 450
    # print(deg, ki.z0, ki.x0)
    # ki.z0 = -530
    if fwdMove:
        # ki.y0 -= 1
        ki.y0 += 1
        # ki.z0 += 1
        # deg += 2
    if revMove:
        # ki.y0 += 1
        # ki.z0 -= 1
        ki.y0 -= 1
        # deg -= 2
    if ki.y0 > 0:
        fwdMove = False
        revMove = True
    if ki.y0 < -150:
        fwdMove = True
        revMove = False
    if ki.z0 > -560:
        ki.z0 -= 1
    # print(ki.y0)
    # ki.x0 = -130
    # ki.y0 = 75
    # ki.z0 = -560
    ki.delta_calc_inverse()
    svr.cmd(ki.theta1, ki.theta2, ki.theta3)
    # if ki.y0 < 200:
    #     ki.y0 += 1
    #     ki.z0 = a * ki.y0 * ki.y0 + b * ki.y0 + c
    #     ki.delta_calc_inverse()
    #     svr.cmd(ki.theta1, ki.theta2, ki.theta3)
    # print(ki.z0, ki.x0)
    # if ki.z0 > - 560:
    #     ki.z0 -= 1
        # ki.delta_calc_inverse()
        # svr.cmd(ki.theta1, ki.theta2, ki.theta3)
    # else:
    #     ki.x0 += 1
    #     ki.y0 += 1
    time.sleep(0.01)
    deg += 5

