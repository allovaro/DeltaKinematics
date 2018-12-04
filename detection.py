import cv2
import imutils
import numpy as np
import math


class Detection:

    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        # self.cap = cv2.VideoCapture('VID_20181122_140853.mp4')
        self.ret, self.img = self.cap.read()
        self.img = cv2.imread('IMG.jpg')

    def countours1(self):
        flag, self.img = self.cap.read()
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)  # Конвертируем в серые тона
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Применяем эффект размытия
        thresh = cv2.threshold(blurred, 175, 255, cv2.THRESH_BINARY)[1]  # Делаем пороговое выделение
        cv2.imshow('thresh', thresh)

        # Поиск контуров в подготовленном изображении
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        return cnts

    def countours2(self):
        flag, self.img = self.cap.read()
        # Поиск контуров в подготовленном изображении
        hsv_min = np.array((0, 54, 5), np.uint8)
        hsv_max = np.array((140, 255, 253), np.uint8)

        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
        hsv_img = cv2.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
        _, cnts, hierarchy = cv2.findContours(hsv_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return cnts

    def detection_process(self, countours):
        # Перебираем все найденные контуры в цикле
        result = [[]]
        i = 0
        for cnt in countours:
            rect = cv2.minAreaRect(cnt)  # Пытаемся вписать прямоугольник
            box = cv2.boxPoints(rect)  # Поиск четырех вершин прямоугольника
            center = (int(rect[0][0]), int(rect[0][1]))

            area = int(rect[1][0]*rect[1][1])  # вычисление площади


            if 10 < area < 50000 and 102 > rect[1][0] > 50 and 102 > rect[1][1] > 50:
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
                    (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv2.norm(reference) *
                                                                                 cv2.norm(usedEdge)))
                if angle > 90:
                    angle1 = angle - 180
                else:
                    angle1 = angle

                color_yellow = (0, 255, 255)
                cv2.circle(self.img, center, 5, color_yellow, 1)
                cv2.putText(self.img, "%d" % int(angle1), (center[0] + 20, center[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 1)
                ctr = np.array(box).reshape((-1, 1, 2)).astype(np.int32)
                cv2.drawContours(self.img, [ctr], -1, (0, 255, 0), 2)

                result[i].append(center[0])
                result[i].append(center[1])
                result[i].append(angle1)
                result.append([])
                i += 1

        cv2.imshow('contours', self.img)
        # print(result[0])
        cv2.waitKey(33)
        # print(center)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return result

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