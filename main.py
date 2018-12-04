from kinematicsinverse import Kinematics
from detection import Detection
from servocontrol import Servo
import time
import math


def pick_and_place(x0):
    z1 = -565
    x1 = -130

    z2 = -565
    x2 = 200

    z3 = -400
    x3 = 50

    a = (z3 - ((x3 * (z2 - z1) + x2 * z1 - x1 * z1) / (x2 - x1))) / (x3 * (x3 - x1 - x2) + x1 * x2)
    b = (z2 - z1) / (x2 - x1) - a * (x1 + x2)
    c = (x2 * z1 - x1 * z2) / (x2 - x1) + a * x1 * x2
    z0 = a * x0 * x0 + b * x0 + c
    return z0


def trapeze_trj(start, end, svr, ki):
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]

    ki.y0 = (ki.x0 - x1) / (x2 - x1) * (y2 - y1) + y1
    d = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    if (x2 - x1) != 0:
        ki.x0 = x1
        ki.y0 = y1
        ki.delta_calc_inverse()
        print(ki.x0, ki.y0, ki.z0)
        svr.cmd(ki.theta1, ki.theta2, ki.theta3)
        time.sleep(1)
        cnt = 5
        diff = (x2 - x1) / cnt
        for i in range(cnt):
            if i == i + 1 or i == cnt - 1:
                ki.z0 = -550
            else:
                ki.z0 = -450
            ki.x0 = ki.x0 + diff
            ki.y0 = ki.y0 = (ki.x0 - x1) / (x2 - x1) * (y2 - y1) + y1
            ki.delta_calc_inverse()
            svr.cmd(ki.theta1, ki.theta2, ki.theta3)
            time.sleep(1)
            print(ki.x0, ki.y0, ki.z0)
            print(i)
    return start


svr = Servo()
sd = Detection()
ki = Kinematics()

result = ki.transform(427, 345)


while True:
    frame = sd.countours1()
    center = sd.detection_process(frame)
    if not center:
        x_new = center[0][0]
    else:
        x_new =100
    if not center:
        y_new = center[0][1]
    else:
        y_new = 100
    result = ki.transform(x_new, y_new)
    print(round(result[0], 2), round(result[1], 2))

svr.connect_servo()
start = [0, 0]
end = [1, -150]
# trapeze_trj(start, end, svr, ki)
r = 160
deg = 1
while True:
    ki.x0 = r * math.sin(math.radians(deg))
    #ki.y0 = ki.x0
    ki.y0 = r * math.sin(math.radians(90 - deg))
    ki.z0 = 500
    ki.delta_calc_inverse()
    svr.cmd(ki.theta1, ki.theta2, ki.theta3, 0)
    print(deg, ki.z0, ki.x0)
    deg += 0.5
    time.sleep(0.01)


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
time.sleep(3)
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
    time.sleep(0.01)
    deg += 5