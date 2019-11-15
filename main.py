from Image_Processing import image_processing as ip
from Shape_Modeling import shape_modeling as sm
from Tessellation_Engine import tessellation_engine as te
from Tessellation_Engine import recommendation_system as rs
import sys

imageDirectory = "Image_Processing/Images/"
coords = ip.processImage(imageDirectory + sys.argv[1])
base_unit = sm.shape_model(coords)
base_tiling = te.tileRegularPolygon(base_unit, 5, 5, 1)
rs.generateRecommendations(base_unit, 5, 5)
te.exportTiling(base_tiling)