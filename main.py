import sys, os
 
dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
print("directory: " + foldername)
print("image processing dir: " + dirpath + '/Image Processing')
print("shape modeling dir: " + dirpath + '/Shape Modeling')

sys.path.insert(0, dirpath + '/Image Processing')
sys.path.insert(0, dirpath + '/Image Processing/Images')
sys.path.insert(0, dirpath + '/Shape Modeling')

import image_processing as ip
# import shape_modeling as sm

# print(ip.processImage("square.jpg"))
ip.printHello()
# sm.shape_print()