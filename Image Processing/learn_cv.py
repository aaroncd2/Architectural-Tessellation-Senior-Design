import numpy as np
from cv2 import cv2 as cv
from matplotlib import pyplot as plt

sketch = cv.imread('rectangles.jpg')

imgray = cv.cvtColor(sketch, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(sketch, contours, -1, (0,255,0), 3)

plt.subplot(121),plt.imshow(sketch, cmap = 'gray')
plt.show()
'''
plt.subplot(121),plt.imshow(sketch, cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()
'''

for i in range (0, len(contours)):
    '''
    for j in range (0, len(contours[i])):
        cv.circle(sketch, (contours[i][j], contours[i][j + 1]), 5, (0, 0, 255), -1)
    print('x: ', contours[i][0][0], 'y: ', contours[i][0][0])'''
    print(contours[i])

print(len(contours[0]))

cv.imshow('Output Sketch', sketch)
cv.waitKey(0)
cv.destroyAllWindows()