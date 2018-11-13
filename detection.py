import cv2
import imutils
import numpy as np
import math


class Detection:

    def __init__(self):
        # self.cap = cv2.VideoCapture(0)
        self.img = cv2.imread('IMG.jpg')

    def get_next_image(self):
        #flag, img = self.cap.read()
        img = cv2.imread('IMG.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Конвертируем в серые тона
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Применяем эффект размытия
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]  # Делаем пороговое выделение
        return thresh

    def countours(self, thresh):
        # Поиск контуров в подготовленном изображении
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        return cnts

    def detection_process(self, countours):
        # Перебираем все найденные контуры в цикле
        for cnt in countours:
            rect = cv2.minAreaRect(cnt)  # Пытаемся вписать прямоугольник
            box = cv2.boxPoints(rect)  # Поиск четырех вершин прямоугольника
            center = (int(rect[0][0]), int(rect[0][1]))
            area = int(rect[1][0]*rect[1][1])  # вычисление площади
            if 20000 < area < 25000:
                # вычисление координат двух векторов, являющихся сторонам прямоугольника
                edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
                edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

                # выясняем какой вектор больше
                usedEdge = edge1
                if cv2.norm(edge2) > cv2.norm(edge1):
                    usedEdge = edge2
                reference = (1, 0)  # горизонтальный вектор, задающий горизонт

                # вычисляем угол между самой длинной стороной прямоугольника и горизонтом
                angle = 180.0 / math.pi * math.acos(
                    (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))
                color_yellow = (0, 255, 255)
                cv2.circle(self.img, center, 5, color_yellow, 1)
                cv2.putText(self.img, "%d" % int(angle), (center[0] + 20, center[1] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
                #cv2.drawContours(img, [box], 0, (255, 0, 0), 2)  # рисуем прямоугольник

        cv2.imshow('contours', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(center)
        return center

    def shape_detector(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if 0.95 >= ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        # return the name of the shape
        return shape

    def vision(self):
        # load the image and resize it to a smaller factor so that
        # the shapes can be approximated better
        image = cv2.imread("IMG.jpg")
        resized = imutils.resize(image, width=300)
        ratio = image.shape[0] / float(resized.shape[0])

        # convert the resized image to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # loop over the contours
        for c in cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
            else:
                cX = 0
                cY = 0
            shape = self.shape_detector(c)
            if shape == "rectangle" or shape == "square":
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)

            # show the output image
            cv2.imshow("Image", image)
            cv2.waitKey(0)

    def vision2(self):
        # load the image and resize it to a smaller factor so that
        # the shapes can be approximated better
        image = cv2.imread("IMG.jpg")
        resized = imutils.resize(image, width=300)
        ratio = image.shape[0] / float(resized.shape[0])

        hsv_min = np.array((0, 0, 255), np.uint8)
        hsv_max = np.array((72, 51, 255), np.uint8)

        # convert the resized image to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        _, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        color_blue = (255, 0, 0)
        color_red = (0, 0, 128)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)
        # loop over the contours
        for c in cnts:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            center = (int(rect[0][0]), int(rect[0][1]))
            area = int(rect[1][0] * rect[1][1])

            edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
            edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

            usedEdge = edge1
            if cv2.norm(edge2) > cv2.norm(edge1):
                usedEdge = edge2

            reference = (1, 0)  # horizontal edge
            angle = 180.0 / math.pi * math.acos(
                (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))

            if area > 500:
                cv2.drawContours(image, [box], 0, color_blue, 2)
                cv2.circle(image, center, 5, color_red, 2)
                cv2.putText(image, "%d" % int(angle), (center[0] + 20, center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                           color_red, 2)
        cv2.imshow('result', image)
        cv2.waitKey(0)

    def vision3(self):
        cv2.namedWindow("result")
        # cap = cv2.VideoCapture(0)

        hsv_min = np.array((0, 0, 255), np.uint8)
        hsv_max = np.array((72, 51, 255), np.uint8)

        color_blue = (255, 0, 0)
        color_red = (0, 0, 128)

        while True:
            img = cv2.imread("IMG.jpg")
            img = cv2.flip(img, 1)
            try:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                thresh = cv2.inRange(hsv, hsv_min, hsv_max)
                _, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                for cnt in contours0:
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    center = (int(rect[0][0]), int(rect[0][1]))
                    area = int(rect[1][0] * rect[1][1])

                    edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
                    edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

                    usedEdge = edge1
                    if cv2.norm(edge2) > cv2.norm(edge1):
                        usedEdge = edge2

                    reference = (1, 0)  # horizontal edge
                    angle = 180.0 / math.pi * math.acos((reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (
                                cv2.norm(reference) * cv2.norm(usedEdge)))

                    if area > 500:
                        cv2.drawContours(img, [box], 0, color_blue, 2)
                        cv2.circle(img, center, 5, color_red, 2)
                        cv2.putText(img, "%d" % int(angle), (center[0] + 20, center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                   color_red, 2)
                cv2.imshow('result', img)
                cv2.imshow('hsv', hsv)
            except:
                raise
            ch = cv2.waitKey(5)
            if ch == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
