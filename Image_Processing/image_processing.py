import numpy as np
from cv2 import cv2 as cv
from matplotlib import pyplot as plt




def getCanny(image, sigma_val=0.33):
    #get median of single channel pixel image
    num_image_median = np.median(image)
    #use median to apply automatic canny
    lower_param = int(max(0,(1.0-sigma_val)* num_image_median))
    upper_param = int(max(255,(1.0-sigma_val)* num_image_median))
    canny_edged_img = cv.Canny(image,lower_param,upper_param)
    
    #return canny image
    return canny_edged_img



def processImage(image):
    sketch = cv.imread(image)
    imgray = cv.cvtColor(sketch, cv.COLOR_BGR2GRAY)
    imgray = cv.bilateralFilter(imgray, 11, 17, 17)
    cannyImg = getCanny(imgray)
    # cv.imshow("Edges",cannyImg)
    ret, thresh = cv.threshold(cannyImg, 127, 255, 0)
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