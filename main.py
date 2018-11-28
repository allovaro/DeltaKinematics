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
ki.z0 = -445.86
print(ki.x0, ki.y0)
ki.delta_calc_inverse()
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(0.5)
svr.cmd(ki.theta1, ki.theta2, ki.theta3)
time.sleep(5)

r = 150
deg = 1
while True:
    ki.x0 = r * math.sin(math.radians(deg))
    ki.y0 = r * math.sin(math.radians(90 - deg))
    # if ki.z0 > -550:
    #     ki.z0 -= 5
    ki.delta_calc_inverse()
    svr.cmd(ki.theta1, ki.theta2, ki.theta3)
    time.sleep(0.04)
    # print(ki.x0, ki.y0)
    deg += 3
