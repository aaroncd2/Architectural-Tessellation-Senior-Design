import numpy as np
from cv2 import cv2 as cv
from matplotlib import pyplot as plt

def processImage(image):
    sketch = cv.imread(image)
    imgray = cv.cvtColor(sketch, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    coords = list()
    numVertices = len(contours[0])
    for i in range (0, len(contours[0])):
        # x coordinate
        coords.append(contours[0][i][0][0])
        # y coordinate
        coords.append(contours[0][i][0][1])
    cv.waitKey(0)
    cv.destroyAllWindows()
    return coords