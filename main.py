from kinematicsinverse import Kinematics
from detection import Detection
from servocontrol import Servo
import serial
import time
import argparse
import imutils
import cv2

# robot = Kinematics()
# robot.x0 = float(input())
# robot.y0 = float(input())
# robot.z0 = float(input())
#
# robot.delta_calc_inverse()
#
# # Открытие COM1 порта для отправки углов
# ser = serial.Serial(
#     port='COM1',
#     baudrate=9600,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
#     timeout=1
# )


# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to the input image")
# args = vars(ap.parse_args())
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
# image = cv2.imread("IMG.jpg")
# resized = imutils.resize(image, width=300)
# ratio = image.shape[0] / float(resized.shape[0])
#
# # convert the resized image to grayscale, blur it slightly,
# # and threshold it
# gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
#
# # find contours in the thresholded image and initialize the
# # shape detector
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#                         cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
# sd = Detection()
# # loop over the contours
# for c in cnts:
#     # compute the center of the contour, then detect the name of the
#     # shape using only the contour
#     M = cv2.moments(c)
#     cX = int((M["m10"] / M["m00"]) * ratio)
#     cY = int((M["m01"] / M["m00"]) * ratio)
#     shape = sd.shape_detector(c)
#
#     # multiply the contour (x, y)-coordinates by the resize ratio,
#     # then draw the contours and the name of the shape on the image
#     c = c.astype("float")
#     c *= ratio
#     c = c.astype("int")
#     cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
#     cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
#                 0.5, (255, 255, 255), 2)
#
#     # show the output image
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)

# print(ser.name)
# visio.mygigatest()
# while 1:
#     time.sleep(1)
#     up = 0
#     if up == 0:
#         ser.write(b'Hello')
#ser.close()

# sd = Detection()
# sd.shape_center()
ki = Kinematics()
svr = Servo()
svr.connect_servo()
ki.x0 = 0
ki.y0 = 0
ki.z0 = -550
ki.delta_calc_inverse()
svr.cmd(ki.theta1, ki.theta2, ki.theta3)

