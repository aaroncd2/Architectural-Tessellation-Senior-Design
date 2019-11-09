from Image_Processing import image_processing as ip
from Shape_Modeling import shape_modeling as sm

imageDirectory = "Image_Processing/Images/"
coords = ip.processImage(imageDirectory + "ellipse.jpg")
sm.shape_model(coords)