from kinematicsinverse import Kinematics
from detection import Detection
from servocontrol import Servo

svr = Servo()
sd = Detection()
ki = Kinematics()

sd.vision()
svr.connect_servo()
ki.x0 = 0
ki.y0 = 0
ki.z0 = -445.5
ki.delta_calc_inverse()
svr.cmd(ki.theta1, ki.theta2, ki.theta3)


