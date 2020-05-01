import numpy as np
from cv2 import cv2 as cv
from matplotlib import pyplot as plt

# gaussian blur algorithm that 
# also helps reduce external noise in a passed in image.
# This is mostly utilized for hand drawn sketches scanned in
def gaussian_kernel(size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return g

# edge detection algorithm that reduces noise in the image prior
# to grabbing the vertex coordinates
def getCanny(image, sigma_val=0.33):
    #get median of single channel pixel image
    num_image_median = np.median(image)
    #use median to apply automatic canny
    lower_param = int(max(0,(1.0-sigma_val)* num_image_median))
    upper_param = int(max(255,(1.0-sigma_val)* num_image_median))
    canny_edged_img = cv.Canny(image,lower_param,upper_param)
    #return canny image
    return canny_edged_img

# main function that processes the images
# passed in by the user
def processImage(image):
    sketch = cv.imread(image)
    #sketch_flipped = cv.flip(sketch,0)
    imgray = cv.cvtColor(sketch, cv.COLOR_BGR2GRAY)
    imgray = cv.GaussianBlur(imgray,(5,5),0)
    imgray = cv.bilateralFilter(imgray, 11, 17, 17)
    cannyImg = getCanny(imgray)
    ret, thresh = cv.threshold(cannyImg, 127, 255, 0)
    # opencv function that finds all the edges (contours) in the image
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # list of coordinates generated by the findCountours function. 
    # there will be an even number of numbers in the coords list, since each coordinate's 
    # x coordinate is placed in the list, then the y coordinate is placed in the list
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
