from kinematicsinverse import Kinematics
from detection import Detection
from servocontrol import Servo
import time


svr = Servo()
sd = Detection()
ki = Kinematics()

#sd.vision()
sd.vision2()
# svr.connect_servo()
# svr.read()
# ki.x0 = 250
# ki.y0 = 250
# ki.z0 = -450
# ki.delta_calc_inverse()
# svr.cmd(ki.theta1, ki.theta2, ki.theta3)


# while True:
#     ki.z0 -= 5
#     ki.delta_calc_inverse()
#     svr.cmd(ki.theta1, ki.theta2, ki.theta3)
#     # svr.read()
#     time.sleep(0.1)

