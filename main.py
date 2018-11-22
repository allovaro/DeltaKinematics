from kinematicsinverse import Kinematics
from detection import Detection
from servocontrol import Servo
import time
import math

svr = Servo()
sd = Detection()
ki = Kinematics()
# frame = sd.countours2(sd.get_next_image())
#
# while True:
#     frame = sd.countours2(sd.get_next_image())
#     center = sd.detection_process(frame)

svr.connect_servo()
# svr.read()
# ki.x0 = 250
# ki.y0 = 250
# ki.z0 = -450
ki.x0 = 10
ki.y0 = 0
ki.z0 = -443
deg = 1
r = 100
print(ki.x0, ki.y0)

# Движение по окружности с радиусом r
while True:
    ki.x0 = r * math.sin(math.radians(deg))
    ki.y0 = r * math.sin(math.radians(90 - deg))
    time.sleep(1)
    print(ki.x0, ki.y0)
    deg += 1

ki.delta_calc_inverse()
svr.cmd(ki.theta1, ki.theta2, ki.theta3)


# while True:
#     ki.z0 -= 5
#     ki.delta_calc_inverse()
#     svr.cmd(ki.theta1, ki.theta2, ki.theta3)
#     # svr.read()
#     time.sleep(0.1)

