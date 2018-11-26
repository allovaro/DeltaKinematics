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

#svr.connect_servo()
# svr.read()
# ki.x0 = 250
# ki.y0 = 250
# ki.z0 = -450
ki.x0 = 0
ki.y0 = 0
ki.z0 = -443
ki.theta1 = 1.01125
ki.theta2 = 1.01125
ki.theta3 = 1.01125
print(ki.x0, ki.y0)
ki.delta_calc_forward()
# ki.delta_calc_inverse()
#svr.cmd(ki.theta1, ki.theta2, ki.theta3)

r = 150
deg = 1
# while True:
#     ki.x0 = r * math.sin(math.radians(deg))
#     ki.y0 = r * math.sin(math.radians(90 - deg))
#     ki.delta_calc_inverse()
#     svr.cmd(ki.theta1, ki.theta2, ki.theta3)
#     time.sleep(0.05)
#     print(ki.x0, ki.y0)
#     deg += 5
