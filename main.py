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
ki.z0 = -462.4
ki.delta_calc_inverse()
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
ki.delta_calc_inverse()
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
ki.delta_calc_inverse()
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(1)
print(ki.x0, ki.y0)

time.sleep(0.5)
# svr.cmd(ki.theta1, ki.theta2, ki.theta3)
# time.sleep(0.5)
# svr.cmd(ki.theta1, ki.theta2, ki.theta3)
# time.sleep(5)

r = 80
deg = 1
fwdMove = True
revMove = False
while True:
    # ki.x0 = r * math.sin(math.radians(deg))
    # ki.y0 = r * math.sin(math.radians(90 - deg))

    # if fwdMove:
    #     ki.y0 += 1
    #     ki.x0 += 1
    # if revMove:
    #     ki.y0 -= 1
    #     ki.x0 -= 1
    # if ki.y0 > 100:
    #     fwdMove = False
    #     revMove = True
    # if ki.y0 < 0:
    #     fwdMove = True
    #     revMove = False
    if ki.z0 > -535:
        # ki.z0 -= 0.1
        print(ki.z0)
    ki.delta_calc_inverse()
    svr.cmd(ki.theta1, ki.theta2, ki.theta3)
    time.sleep(0.05)
    # print(ki.x0, ki.y0)
    deg += 3
