from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import *
from kivy.graphics.vertex_instructions import Mesh
from kivy.core.window import Window

import sys
sys.path.insert(1, '../Shape_Identification/tiling_rules.py')
from Shape_Identification import tiling_rules as tr

from shapely.geometry import Polygon # for geometric objects
from shapely import affinity # for transformations
import matplotlib.pyplot as plt # for display
import math # for trig functions
import pandas as pd # for export
import numpy as np # for math
from Tessellation_Engine import tessellation_utilities as tu #for utility functions
from Tessellation_Engine.save_dialog import SaveDialog
from Tessellation_Engine.custom_slider import CustomSlider

### START TESSELLATION ENGINE ###
class CanvasWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        self.lines = InstructionGroup()
        
class TessellationWidget(GridLayout):
    def __init__(self, **kwargs):
        super(TessellationWidget, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.polygons = []
        self.actions = []
        self.exterior = None
        self.type = None
        self.stroke_color = [255,255,255,1]
        self.fill_color = [0,0,1,1]
        
        # create row for canvas
        self.canvas_widget = CanvasWidget()
        imageRow = BoxLayout(orientation='horizontal', padding=0, spacing=0)
        imageRow.add_widget(self.canvas_widget)
        self.add_widget(imageRow)

        self.controls = BoxLayout(orientation='horizontal', size_hint=(1,.30))
        self.buttons = GridLayout(rows=5, cols=2)
        self.sliders = GridLayout(rows=4, cols=2)

        # Add slider and label to widget
        self.rotation_slider = CustomSlider(min=0, max=360, value=0, value_track = True)
        self.rotation_value = 0
        self.label_box = BoxLayout(orientation='horizontal', size_hint=(1,1))
        self.input_box = TextInput(text='0', input_filter='float', multiline=False, font_size='12dp')
        self.input_box.bind(on_text_validate=self.on_enter)
        self.label = Label(text ='Rotation:', font_size='12dp')
        self.label_box.add_widget(self.label)
        self.label_box.add_widget(self.input_box)
        self.sliders.add_widget(self.label_box) 
        self.sliders.add_widget(self.rotation_slider)
        self.rotation_slider.bind(value=self.rotate_polygon)

        # Add horizontal translation slider
        self.h_label = Label(text='Horizontal Spacing', font_size='12dp')
        self.sliders.add_widget(self.h_label)
        self.slide_horizontal = CustomSlider(min=0, max=200, value=100, value_track = True)
        self.xSpacing = 100
        self.slide_horizontal.bind(value = self.adjust_horizontal_spacing)
        self.sliders.add_widget(self.slide_horizontal)

        # Add vertical translation slider
        self.v_label = Label(text='Vertical Spacing', font_size='12dp')
        self.sliders.add_widget(self.v_label)
        self.slide_vertical = CustomSlider(min=0, max=200, value=100, value_track = True)
        self.ySpacing = 100
        self.slide_vertical.bind(value = self.adjust_vertical_spacing)
        self.sliders.add_widget(self.slide_vertical)

        # Add scale slider
        self.scale_label = Label(text='Scale', font_size='12dp')
        self.sliders.add_widget(self.scale_label)
        self.slide_scale = CustomSlider(min=0, max=200, value=100, value_track = True)
        self.slide_scale.bind(value = self.scale_polygons)
        self.sliders.add_widget(self.slide_scale)

        self.controls.add_widget(self.sliders)

        # Add save state btn
        self.save_state_button = Button(text = 'Save State', background_color = (1,1,1,1), font_size='10dp')
        self.buttons.add_widget(self.save_state_button)
        self.save_state_button.bind(on_press=self.save_state)

        # Add export button
        self.export_button = Button(text = 'Export', background_color = (1,1,1,1), font_size='10dp')
        self.buttons.add_widget(self.export_button)
        self.export_button.bind(on_press=self.export_tiling)

        # Add flip horizontal button
        self.horizontal_button = Button(text = 'Flip Horizontal', background_color = (1,1,1,1), font_size='10dp')
        self.buttons.add_widget(self.horizontal_button)
        self.horizontal_button.bind(on_press=self.flip_horizontal)

        # Add flip vertical button
        self.vertical_button = Button(text = 'Flip Vertical', background_color = (1,1,1,1), font_size='10dp')
        self.buttons.add_widget(self.vertical_button)
        self.vertical_button.bind(on_press=self.flip_vertical)

        # Add alternate row button
        self.alternate_row_button = Button(text = 'Alternate Rows', background_color = (1,1,1,1), font_size='10dp')
        self.buttons.add_widget(self.alternate_row_button)
        self.alternate_row_button.bind(on_press=self.alternate_rows)

        # Add alternate column button
        self.alternate_col_button = Button(text = 'Alternate Cols', background_color = (1,1,1,1), font_size='10dp')
        self.buttons.add_widget(self.alternate_col_button)
        self.alternate_col_button.bind(on_press=self.alternate_cols)

        # Add undo button
        self.undo_button = Button(text = 'Undo', background_color = (1,1,1,1), font_size='10dp')
        self.buttons.add_widget(self.undo_button)
        self.undo_button.bind(on_press=self.undo)

        # Add reset button
        self.reset_button = Button(text = 'Reset', background_color = (1,1,1,1), font_size='10dp')
        self.buttons.add_widget(self.reset_button)
        self.reset_button.bind(on_press=self.reset)

        # Add control row
        self.controls.add_widget(self.buttons)
        self.add_widget(self.controls)

        # Add tiling type label
        self.rec_label = Label(text='Tessellation Type:', font_size='10dp')
        self.buttons.add_widget(self.rec_label)
        self.rec_type = Label(text='Freeform', font_size='10dp')
        self.buttons.add_widget(self.rec_type)

    # Display initial tiling
    def display_initial_tiling(self):
        self.xNum = 5
        self.yNum = 5
        points = self.parent.b_coords
        self.polygon = Polygon(points)
        self.base_unit = self.polygon
        self.original_base_unit = self.polygon
        self.shape_info = tr.identify_shape(self.base_unit)
        if self.type == None:
            self.type = 'regular'
        if self.type == 'regular':
            self.tile_regular_polygon()
        elif self.type == 'parallelogram':
            self.tile_parallelogram()
        elif self.type == 'hexagon':
            self.tile_hexagon()

    def set_coords(self, num):
        self.points = num

    # Tiles polygons in an xNum by yNum grid utilizing bounding boxes
    def tile_regular_polygon(self):
        polygon = tu.shapely_to_kivy(self.polygon)
        bounds = self.polygon.bounds
        xInc = abs(bounds[2] - bounds[0]) * (self.xSpacing / 100)
        yInc = abs(bounds[3] - bounds[1]) * (self.ySpacing / 100)

        polygons = []
        temp = []
        xCount = 1
        yCount = 1

        while yCount <= self.yNum:
            while xCount <= self.xNum:
                xNext = xCount * xInc
                yNext = yCount * yInc
                count = 0
                for p in polygon:
                    if count % 2 == 0:
                        temp.append(p + xNext)
                    else:
                        temp.append(p + yNext)
                    count = count + 1
                xCount = xCount + 1
                polygons.append(temp)
                temp = []
            yCount = yCount + 1
            xCount = 1

        self.polygons = polygons
        self.draw_polygons()

    # tiles a parallelogram
    def tile_parallelogram(self):
        # calculate increment between shapes
        scale_factor = self.slide_scale.value / 100
        shape = self.polygon
        exterior = tu.make_positive(self.rec_shape[3])
        self.exterior = exterior
        bounds = exterior.bounds
        count = 0
        while count < 4:
            # calculate horizontal increments
            if exterior.exterior.coords[count][0] == bounds[2]:
                if count == 0:
                    xInc = max(exterior.exterior.coords[1][0], exterior.exterior.coords[3][0]) - bounds[0]
                    xInc2 = min(exterior.exterior.coords[1][0], exterior.exterior.coords[3][0]) - bounds[0]
                elif count == 3:
                    xInc = max(exterior.exterior.coords[0][0], exterior.exterior.coords[2][0]) - bounds[0]
                    xInc2 = min(exterior.exterior.coords[0][0], exterior.exterior.coords[2][0]) - bounds[0]
                else:
                    xInc = max(exterior.exterior.coords[count + 1][0], exterior.exterior.coords[count - 1][0]) - bounds[0]
                    xInc2 = min(exterior.exterior.coords[count + 1][0], exterior.exterior.coords[count - 1][0]) - bounds[0]
            # calculate vertical increments
            if exterior.exterior.coords[count][1] == bounds[3]:
                if count == 0:
                    yInc = max(exterior.exterior.coords[1][1], exterior.exterior.coords[3][1]) - bounds[1]
                    yInc2 = min(exterior.exterior.coords[1][1], exterior.exterior.coords[3][1]) - bounds[1]
                elif count == 3:
                    yInc = max(exterior.exterior.coords[0][1], exterior.exterior.coords[2][1]) - bounds[1]
                    yInc2 = min(exterior.exterior.coords[0][1], exterior.exterior.coords[2][1]) - bounds[1]
                else:
                    yInc = max(exterior.exterior.coords[count + 1][1], exterior.exterior.coords[count - 1][1]) - bounds[1]
                    yInc2 = min(exterior.exterior.coords[count + 1][1], exterior.exterior.coords[count - 1][1]) - bounds[1]
            count = count + 1
        xInc = xInc * (self.xSpacing / 100)
        yInc = yInc * (self.ySpacing / 100)
        xInc2 = xInc2 * (self.xSpacing / 100)
        yInc2 = yInc2 * (self.ySpacing / 100)
    
        # determine direction of parallelogram
        pLeft = None 
        pRight = None
        pointsRight = False
        pointsUp = False
        hasDoubleMax = False
        count = 0
        while count < 4:
            if exterior.exterior.coords[count][0] == bounds[2]:
                pRight = exterior.exterior.coords[count]
                if exterior.exterior.coords[count][1] == bounds[3] or exterior.exterior.coords[count][1] == bounds[1]:
                    hasDoubleMax = True
                if count == 0 or count == 2:
                    xMax = max(exterior.exterior.coords[1][0], exterior.exterior.coords[3][0])
                    if xMax == exterior.exterior.coords[1][0] and exterior.exterior.coords[1][1] > exterior.exterior.coords[3][1]:
                        pointsUp = True
                    elif xMax == exterior.exterior.coords[3][0] and exterior.exterior.coords[3][1] > exterior.exterior.coords[1][1]:
                        pointsUp = True
                elif count == 1 or count == 3:
                    xMax = max(exterior.exterior.coords[0][0], exterior.exterior.coords[2][0])
                    if xMax == exterior.exterior.coords[0][0] and exterior.exterior.coords[0][1] > exterior.exterior.coords[2][1]:
                        pointsUp = True
                    elif xMax == exterior.exterior.coords[2][0] and exterior.exterior.coords[2][1] > exterior.exterior.coords[0][1]:
                        pointsUp = True
            if exterior.exterior.coords[count][0] == bounds[0]:
                pLeft = exterior.exterior.coords[count]
                if exterior.exterior.coords[count][1] == bounds[3] or exterior.exterior.coords[count][1] == bounds[1]:
                    hasDoubleMax = True
            count = count + 1
        if pRight[1] >= pLeft[1]:
            pointsRight = True
    
        xCount = 1
        yCount = 1
        self.polygons = []
        while yCount <= self.yNum:
            while xCount <= self.xNum:
                temp = []
                for p in shape.exterior.coords:
                    if xInc2 == 0 and yInc2 == 0:
                        px = (p[0] + (xInc * xCount)) * scale_factor
                        py = (p[1] + (yInc * yCount)) * scale_factor
                    elif pointsRight:
                        if hasDoubleMax:
                            if pointsUp:
                                #print("RIGHT DMAX UP")
                                px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                py = (p[1] + (yInc2 * xCount) + (yInc * yCount)) * scale_factor
                            else:
                                #print("RIGHT DMAX DOWN")
                                px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                py = (p[1] + (yInc * xCount) + (yInc2 * yCount)) * scale_factor
                        else:
                            if pointsUp:
                                #print("RIGHT UP")
                                px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                py = (p[1] + (yInc * xCount) - (yInc2 * yCount)) * scale_factor
                            else:
                                #print("RIGHT DOWN")
                                px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                py = (p[1] - (yInc2 * xCount) + (yInc * yCount)) * scale_factor
                    else:
                        if hasDoubleMax:
                            if pointsUp:
                                #print("LEFT DMAX DOWN")
                                px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                py = (p[1] - (yInc2 * xCount) - (yInc * yCount)) * scale_factor
                            else:
                                #print("LEFT DMAX UP")
                                px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                py = (p[1] - (yInc2 * xCount) - (yInc * yCount)) * scale_factor
                        else:
                            if pointsUp:
                                #print("LEFT UP")
                                px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                py = (p[1] + (yInc2 * xCount) - (yInc * yCount)) * scale_factor
                            else:
                                #print("LEFT DOWN")
                                px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                py = (p[1] + (yInc2 * xCount) - (yInc * yCount)) * scale_factor
                    temp.append((px,py))
                temp_poly = Polygon(temp)
                temp_poly = affinity.rotate(temp_poly, self.rotation_slider.value)
                self.polygons.append(tu.shapely_to_kivy(temp_poly))
                temp = None
                xCount = xCount + 1
            xCount = 1
            yCount = yCount + 1
        self.draw_polygons()

    # tiles a hexagon (with 3 sets of parallel edges)
    def tile_hexagon(self):
        # calculate increment between shapes
        scale_factor = self.slide_scale.value / 100
        shape = self.polygon
        exterior = tu.make_positive(self.rec_shape[3])
        self.exterior = exterior
        bounds = exterior.bounds
        count = 0
        while count < 6:
            # calculate horizontal increments
            if exterior.exterior.coords[count][0] == bounds[2]:
                if count == 0:
                    xInc = max(exterior.exterior.coords[1][0], exterior.exterior.coords[5][0]) - bounds[0]
                    xInc2 = min(exterior.exterior.coords[1][0], exterior.exterior.coords[5][0]) - bounds[0]
                elif count == 5:
                    xInc = max(exterior.exterior.coords[0][0], exterior.exterior.coords[4][0]) - bounds[0]
                    xInc2 = min(exterior.exterior.coords[0][0], exterior.exterior.coords[4][0]) - bounds[0]
                else:
                    xInc = max(exterior.exterior.coords[count + 1][0], exterior.exterior.coords[count - 1][0]) - bounds[0]
                    xInc2 = min(exterior.exterior.coords[count + 1][0], exterior.exterior.coords[count - 1][0]) - bounds[0]
            # calculate vertical increments
            if exterior.exterior.coords[count][1] == bounds[3]:
                if count == 0:
                    yInc = max(exterior.exterior.coords[1][1], exterior.exterior.coords[5][1]) - bounds[1]
                    yInc2 = min(exterior.exterior.coords[1][1], exterior.exterior.coords[5][1]) - bounds[1]
                elif count == 5:
                    yInc = max(exterior.exterior.coords[0][1], exterior.exterior.coords[4][1]) - bounds[1]
                    yInc2 = min(exterior.exterior.coords[0][1], exterior.exterior.coords[4][1]) - bounds[1]
                else:
                    yInc = max(exterior.exterior.coords[count + 1][1], exterior.exterior.coords[count - 1][1]) - bounds[1]
                    yInc2 = min(exterior.exterior.coords[count + 1][1], exterior.exterior.coords[count - 1][1]) - bounds[1]
            count = count + 1
        xInc = xInc * (self.xSpacing / 100)
        yInc = yInc * (self.ySpacing / 100)
        xInc2 = xInc2 * (self.xSpacing / 100)
        yInc2 = yInc2 * (self.ySpacing / 100)
    
        # determine direction of hexagon
        pointsUp = False
        pointsRight = False
        tiltsUp = False
        tiltsRight = False
        hasDoubleMax = False
        isLeftHorizontal = False
        isRightHorizontal = False
        count = 0
        while count < 6:
            if exterior.exterior.coords[count][0] == bounds[0]:
                pLeft = exterior.exterior.coords[count]
            if exterior.exterior.coords[count][0] == bounds[2]:
                if exterior.exterior.coords[count][1] == bounds[3] or exterior.exterior.coords[count][1] == bounds[1]:
                    hasDoubleMax = True
                pRight = exterior.exterior.coords[count]
                if count == 0:
                    xMax = max(exterior.exterior.coords[1][0], exterior.exterior.coords[5][0])
                    if xMax == exterior.exterior.coords[1][0] and exterior.exterior.coords[1][1] > exterior.exterior.coords[5][1]:
                        tiltsUp = True
                    elif xMax == exterior.exterior.coords[5][0] and exterior.exterior.coords[5][1] > exterior.exterior.coords[1][1]:
                        tiltsUp = True
                elif count == 5:
                    xMax = max(exterior.exterior.coords[0][0], exterior.exterior.coords[4][0])
                    if xMax == exterior.exterior.coords[0][0] and exterior.exterior.coords[0][1] > exterior.exterior.coords[4][1]:
                        tiltsUp = True
                    elif xMax == exterior.exterior.coords[4][0] and exterior.exterior.coords[4][1] > exterior.exterior.coords[0][1]:
                        tiltsUp = True
                else:
                    xMax = max(exterior.exterior.coords[count - 1][0], exterior.exterior.coords[count + 1][0])
                    if xMax == exterior.exterior.coords[count - 1][0] and exterior.exterior.coords[count - 1][1] > exterior.exterior.coords[count + 1][1]:
                        tiltsUp = True
                    elif xMax == exterior.exterior.coords[count + 1][0] and exterior.exterior.coords[count + 1][1] > exterior.exterior.coords[count - 1][1]:
                        tiltsUp = True
            if exterior.exterior.coords[count][1] == bounds[1]:
                pDown = exterior.exterior.coords[count]
            if exterior.exterior.coords[count][1] == bounds[3]:
                pUp = exterior.exterior.coords[count]
                if count == 0:
                    yMax = max(exterior.exterior.coords[1][1], exterior.exterior.coords[5][1])
                    if yMax == exterior.exterior.coords[1][1] and exterior.exterior.coords[1][0] > exterior.exterior.coords[5][0]:
                        tiltsRight = True
                    elif yMax == exterior.exterior.coords[5][1] and exterior.exterior.coords[5][0] > exterior.exterior.coords[1][0]:
                        tiltsRight = True
                    if exterior.exterior.coords[1][0] == bounds[0] or exterior.exterior.coords[5][0] == bounds[0]:
                        isLeftHorizontal = True
                    if exterior.exterior.coords[1][0] == bounds[2] or exterior.exterior.coords[5][0] == bounds[2]:
                        isRightHorizontal = True
                elif count == 5:
                    yMax = max(exterior.exterior.coords[0][1], exterior.exterior.coords[4][1])
                    if yMax == exterior.exterior.coords[0][1] and exterior.exterior.coords[0][0] > exterior.exterior.coords[4][0]:
                        tiltsRight = True
                    elif yMax == exterior.exterior.coords[4][1] and exterior.exterior.coords[4][0] > exterior.exterior.coords[0][0]:
                        tiltsRight = True
                    if exterior.exterior.coords[0][0] == bounds[0] or exterior.exterior.coords[4][0] == bounds[0]:
                        isLeftHorizontal = True
                    if exterior.exterior.coords[0][0] == bounds[2] or exterior.exterior.coords[4][0] == bounds[2]:
                        isRightHorizontal = True
                else:
                    yMax = max(exterior.exterior.coords[count - 1][1], exterior.exterior.coords[count + 1][1])
                    if yMax == exterior.exterior.coords[count - 1][1] and exterior.exterior.coords[count - 1][0] > exterior.exterior.coords[count + 1][0]:
                         tiltsRight = True
                    elif yMax == exterior.exterior.coords[count + 1][1] and exterior.exterior.coords[count + 1][0] > exterior.exterior.coords[count - 1][0]:
                        tiltsRight = True
                    if exterior.exterior.coords[count - 1][0] == bounds[0] or exterior.exterior.coords[count + 1][0] == bounds[0]:
                        isLeftHorizontal = True
                    if exterior.exterior.coords[count - 1][0] == bounds[2] or exterior.exterior.coords[count + 1][0] == bounds[2]:
                        isRightHorizontal = True
            count = count + 1
        if pRight[1] >= pLeft[1]:
            pointsUp = True
        if pUp[0] >= pDown[0]:
            pointsRight = True

        # build tiling
        xCount = 1
        yCount = 1
        self.polygons = []
        while yCount <= self.yNum:
            while xCount <= self.xNum:
                temp = []
                for p in shape.exterior.coords:
                    if pointsRight:
                        if pointsUp:
                            if tiltsUp:
                                if tiltsRight:
                                    #print("RIGHT + UP | UP + RIGHT")
                                    if isRightHorizontal:
                                        px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                        py = (p[1] + (yInc * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                    else:
                                        px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                        py = (p[1] - (yInc2 * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                else:
                                    #print("RIGHT + UP | UP + LEFT")
                                    px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                    py = (p[1] + (yInc2 * xCount) - ((yInc - yInc2) * yCount)) * scale_factor
                            else:
                                if tiltsRight:
                                    #print("RIGHT + UP | DOWN + RIGHT")
                                    px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                    py = (p[1] + (yInc * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                else:
                                    #print("RIGHT + UP | DOWN + LEFT")
                                    if hasDoubleMax:
                                        px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                        py = (p[1] + (yInc * xCount) + (yInc2 * yCount)) * scale_factor
                                    else:
                                        px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                        py = (p[1] + (yInc2 * xCount) - ((yInc - yInc2) * yCount)) * scale_factor
                        else:
                            if tiltsUp:
                                if tiltsRight:
                                    #print("RIGHT + DOWN | UP + RIGHT")
                                    px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                    py = (p[1] - (yInc2 * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                else:
                                    #print("RIGHT + DOWN | UP + LEFT")
                                    if isRightHorizontal:
                                        px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                        py = (p[1] + (yInc2 * xCount) - ((yInc - yInc2) * yCount)) * scale_factor
                                    else:
                                        px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                        py = (p[1] - (yInc * xCount) - ((yInc - yInc2) * yCount)) * scale_factor
                            else:
                                if tiltsRight:
                                    #print("RIGHT + DOWN | DOWN + RIGHT")
                                    px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                    py = (p[1] - (yInc2 * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                else:
                                    #print("RIGHT + DOWN | DOWN + LEFT")
                                    px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                    py = (p[1] + (yInc2 * xCount) - ((yInc - yInc2) * yCount)) * scale_factor
                    else:
                        if pointsUp:
                            if tiltsUp:
                                if tiltsRight:
                                    #print("LEFT + UP | UP + RIGHT")
                                    px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                    py = (p[1] - (yInc2 * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                else:
                                    #print("LEFT + UP | UP + LEFT")
                                    px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                    py = (p[1] - (yInc2 * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                            else:
                                if tiltsRight:
                                    #print("LEFT + UP | DOWN + RIGHT")
                                    if isLeftHorizontal:
                                        px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                        py = (p[1] - (yInc2 * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                    else:
                                        px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                        py = (p[1] + (yInc * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                else:
                                    #print("LEFT + UP | DOWN + LEFT")
                                    px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                    py = (p[1] + (yInc2 * xCount) - ((yInc - yInc2) * yCount)) * scale_factor
                        else:
                            if tiltsUp:
                                if tiltsRight:
                                    #print("LEFT + DOWN | UP + RIGHT")
                                    if hasDoubleMax:
                                        px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                        py = (p[1] - (yInc2 * xCount) - (yInc * yCount)) * scale_factor
                                    else:
                                        px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                        py = (p[1] - (yInc2 * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                else:
                                    #print("LEFT + DOWN | UP + LEFT")
                                    px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                    py = (p[1] - (yInc * xCount) - ((yInc - yInc2) * yCount)) * scale_factor 
                            else:
                                if tiltsRight:
                                    #print("LEFT + DOWN | DOWN + RIGHT")
                                    px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                    py = (p[1] - (yInc2 * xCount) + ((yInc - yInc2) * yCount)) * scale_factor
                                else:
                                    #print("LEFT + DOWN | DOWN + LEFT")
                                    if isLeftHorizontal:
                                        px = (p[0] + (xInc * xCount) + (xInc2 * yCount)) * scale_factor
                                        py = (p[1] - (yInc * xCount) - ((yInc - yInc2) * yCount)) * scale_factor
                                    else:
                                        px = (p[0] + (xInc2 * xCount) + (xInc * yCount)) * scale_factor
                                        py = (p[1] + (yInc2 * xCount) - ((yInc - yInc2) * yCount)) * scale_factor
                    temp.append((px,py))
                temp_poly = Polygon(temp)
                temp_poly = affinity.rotate(temp_poly, self.rotation_slider.value)
                self.polygons.append(tu.shapely_to_kivy(temp_poly))
                temp = None
                xCount = xCount + 1
            xCount = 1
            yCount = yCount + 1
        self.draw_polygons()

    # Rotates each polygon by the degrees specified by the slider
    def rotate_polygon(self, instance, degrees):
        if instance == 0:
            rotation_amount = degrees - self.rotation_slider.value
        else:
            rotation_amount = self.rotation_slider.value - self.rotation_value
        self.rotation_value = self.rotation_slider.value
        temp = []
        for polygon in self.polygons:
            temp_poly = Polygon(tu.kivy_to_shapely(polygon))
            temp_poly = affinity.rotate(temp_poly, rotation_amount)
            temp_poly = tu.shapely_to_kivy(temp_poly)
            temp.append(temp_poly)
        self.input_box.text = str(round(self.rotation_slider.value, 2))
        self.polygons = temp
        self.draw_polygons()
        if self.rotation_slider.action_complete == True:
            self.actions.append(('rotate', self.rotation_slider.previous_value))
            self.rotation_slider.action_complete = False

    # Handles textbox input
    def on_enter(self, value):
        self.rotation_slider.value = float(self.input_box.text)
        if self.rotation_slider.value > 360:
            self.rotation_slider.value = self.rotation_slider.value % 360
        self.rotate_polygon(0, float(self.input_box.text))

    def save_state(self, instance):
        print("saving state")
        #self.shape_info.append((self.polygon,self.type, True , self.polygons))
    
        self.parent.children[2].add_saved_state(self.polygon, self.type, True, self.polygons)
        #self.parent.children[0].add_saved_session_btn(self.polygon, self.polygons, self.type)



    # flips a polygon horizontally across its center
    def flip_horizontal(self, instance):
        if instance != 0:
            self.actions.append(('horizontal flip', 0))
        polygons = []
        for polygon in self.polygons:
            shapely_poly = Polygon(tu.kivy_to_shapely(polygon))
            bounds = shapely_poly.bounds
            temp = []
            centerX = bounds[0] + ((bounds[2] - bounds[0]) / 2.0)
            count = 0
            for p in polygon:
                if count % 2 == 0:
                    temp.append((2 * centerX) - p)
                else:
                    temp.append(p)
                count = count + 1
            polygons.append(temp)
        self.polygons = polygons
        self.draw_polygons()

    # flips a polygon vertically across its center
    def flip_vertical(self, instance):
        if instance != 0:
            self.actions.append(('vertical flip', 0))
        polygons = []
        for polygon in self.polygons:
            shapely_poly = Polygon(tu.kivy_to_shapely(polygon))
            bounds = shapely_poly.bounds
            temp = []
            centerY = bounds[1] + ((bounds[3] - bounds[1]) / 2.0)
            count = 0
            for p in polygon:
                if count % 2 == 0:
                    temp.append(p)
                else:
                    temp.append((2 * centerY) - p)
                count = count + 1
            polygons.append(temp)
        self.polygons = polygons
        self.draw_polygons()

    # undoes last action performed by user
    def undo(self, instance):
        if len(self.actions) > 0:
            action = self.actions.pop()
            if action[0] == 'horizontal flip':
                self.flip_horizontal(0)
            elif action[0] == 'vertical flip':
                self.flip_vertical(0)
            elif action[0] == 'alternate rows':
                self.alternate_rows(0)
            elif action[0] == 'alternate cols':
                self.alternate_cols(0)
            elif action[0] == 'rotate':
                self.rotate_polygon(0, action[1])
                self.input_box.text = str(round(action[1], 2))
                self.rotation_slider.value = float(self.input_box.text)
            elif action[0] == 'scale':
                self.slide_scale.value = action[1]
                self.polygons = action[2]
                self.draw_polygons()

    # resets the screen
    def reset(self, instance):
        self.rotation_slider.value = 0
        self.rotation_value = 0
        self.slide_horizontal.value = 100
        self.xSpacing = 100
        self.slide_vertical.value = 100
        self.ySpacing = 100
        if instance != 1:
            self.slide_scale.value = 100
        self.base_unit = self.original_base_unit
        self.polygon = self.base_unit
        self.tile_regular_polygon()
        self.type = 'regular'
        self.rec_type.text = 'Freeform'

    # Flips alternating rows across their center vertically
    def alternate_rows(self, instance):
        if instance != 0:
            self.actions.append(('alternate rows', 0))
        polygons = []
        poly_count = 0
        flip = False
        for polygon in self.polygons:
            if flip == True:
                shapely_poly = Polygon(tu.kivy_to_shapely(polygon))
                bounds = shapely_poly.bounds
                temp = []
                centerY = bounds[1] + ((bounds[3] - bounds[1]) / 2.0)
                count = 0
                for p in polygon:
                    if count % 2 == 0:
                        temp.append(p)
                    else:
                        temp.append((2 * centerY) - p)
                    count = count + 1
            else:
                temp = polygon
            polygons.append(temp)
            poly_count = poly_count + 1
            if poly_count % self.xNum == 0:
                if flip:
                    flip = False
                else:
                    flip = True
        self.polygons = polygons
        self.draw_polygons()

    # flips alternating columns across their center horizontally
    def alternate_cols(self, instance):
        if instance != 0:
            self.actions.append(('alternate cols', 0))
        polygons = []
        poly_count = 0
        flip = False
        for polygon in self.polygons:
            if flip == True:
                shapely_poly = Polygon(tu.kivy_to_shapely(polygon))
                bounds = shapely_poly.bounds
                temp = []
                centerX = bounds[0] + ((bounds[2] - bounds[0]) / 2.0)
                count = 0
                for p in polygon:
                    if count % 2 == 0:
                        temp.append((2 * centerX) - p)
                    else:
                        temp.append(p)
                    count = count + 1
                flip = False
            else:
                temp = polygon
                flip = True
            polygons.append(temp)
            poly_count = poly_count + 1
            if poly_count % self.xNum == 0:
                flip = False
        self.polygons = polygons
        self.draw_polygons()

    # Exports the currently displayed polygons to a CSV file
    def export_tiling(self, instance):
        points = {}
        points['type'] = self.type
        num = 1
        for poly in self.polygons:
            xs = []
            ys = []
            count = 0
            for p in poly:
                if count % 2 == 0:
                    xs.append(p)
                else:
                    ys.append(p)
                count = count + 1
            points['x' + str(num)] = xs
            points['y' + str(num)] = ys
            num += 1
        self.df = pd.DataFrame(points)
        SaveDialog(self).open()

    # Draws an array of polygons to the canvas
    def draw_polygons(self):
        self.scale_to_fit_window()
        self.canvas_widget.lines.clear()
        indices = tu.make_indices_list(self.polygons[0])
        for polygon in self.polygons:
            mesh_points = tu.make_mesh_list(polygon)
            r,g,b,a = self.fill_color[0], self.fill_color[1], self.fill_color[2], self.fill_color[3]
            self.canvas_widget.lines.add(Color(r,g,b,a))
            self.canvas_widget.lines.add(Mesh(vertices=mesh_points, indices=indices, mode='triangle_strip'))
            r,g,b,a = self.stroke_color[0], self.stroke_color[1], self.stroke_color[2], self.stroke_color[3]
            self.canvas_widget.lines.add(Color(r,g,b,a))
            self.canvas_widget.lines.add(Line(points = polygon, width=2.0, close=False))
        self.canvas_widget.canvas.add(self.canvas_widget.lines)

    # Adjusts horizontal spacing between polygons
    def adjust_horizontal_spacing(self, instance, amount):
        increment = (self.slide_horizontal.value - 100) / 5
        poly_count = 0
        temp = []
        for polygon in self.polygons:
            count = 0
            temp_poly = []
            for p in polygon:
                if count % 2 == 0:
                    temp_poly.append(p + ((increment * (poly_count % self.xNum))))
                else:
                    temp_poly.append(p)
                count = count + 1
            temp.append(temp_poly)
            poly_count = poly_count + 1
        self.polygons = temp
        self.draw_polygons()
            
    # Adjusts vertical spacing between polygons
    def adjust_vertical_spacing(self, instance, amount):
        increment = (self.slide_horizontal.value - 100) / 5
        poly_count = 0
        row_count = 0
        temp = []
        for polygon in self.polygons:
            count = 0
            temp_poly = []
            for p in polygon:
                if count % 2 == 0:
                    temp_poly.append(p)
                else:
                    temp_poly.append(p + (increment * row_count))
                count = count + 1
            temp.append(temp_poly)
            poly_count = poly_count + 1
            if poly_count % self.xNum == 0:
                row_count = row_count + 1
        self.polygons = temp
        self.draw_polygons()

    # scales polygons
    def scale_polygons(self, instance, amount):
        scale_factor = self.slide_scale.value / 100
        temp = []
        for polygon in self.polygons:
            temp_poly = []
            for p in polygon:
                temp_poly.append(p * scale_factor)
            temp.append(temp_poly)
        self.polygons = temp
        self.draw_polygons()
        if self.slide_scale.action_complete == True:
            self.actions.append(('scale', self.slide_scale.previous_value, self.polygons))
            self.rotation_slider.action_complete = False


    # displays the next recommendation to the screen
    def draw_recommendation(self, index):
        self.reset(0)
        self.rec_shape = self.shape_info[index]
        if self.rec_shape[3] == None:
            self.parent.children[2].config_from_shapely_poly(self.rec_shape[0])
        self.base_unit = tu.make_positive(self.rec_shape[0])
        self.polygon = tu.make_positive(self.rec_shape[0])
        self.type = self.rec_shape[1]
        if self.type == 'regular':
            self.tile_regular_polygon()
            self.rec_type.text = 'Freeform'
        elif self.type == 'parallelogram':
            self.tile_parallelogram()
            self.rec_type.text = 'Parallelogram'
        elif self.type == 'hexagon':
            self.tile_hexagon()
            self.rec_type.text = 'Hexagon'

    #scales tiling before drawing to ensure it fits on window
    def scale_to_fit_window(self):
        size = Window.size
        max_width = size[0] / 2
        max_height = size[1] - self.controls.height

        max_x = self.polygons[0][0]
        min_x = self.polygons[0][0]
        max_y = self.polygons[0][1]
        min_y = self.polygons[0][1]
        for polygon in self.polygons:
            count = 0
            for p in polygon:
                if count % 2 == 0:
                    if p < min_x:
                        min_x = p
                    if p > max_x:
                        max_x = p
                else:
                    if p < min_y:
                        min_y = p
                    if p > max_y:
                        max_y = p
                count += 1

        tessel_width = max_x - min_x
        tessel_height = max_y - min_y
        new_width = tessel_width
        new_height = tessel_height
        scale_factor = 1
        while new_width > max_width or new_height > max_height:
            scale_factor = scale_factor - .01
            new_width= tessel_width * scale_factor
            new_height = tessel_height * scale_factor
       
        max_x = max_x * scale_factor
        min_x = min_x * scale_factor
        max_y = max_y * scale_factor
        min_y = min_y * scale_factor
        xOff = 0
        yOff = 0
        if min_x < 0:
            xOff = min_x * -1
        elif max_x > (size[0] / 2):
            xOff = min_x * -1
        if min_y < 0:
            yOff = min_y * -1
        elif max_y > (size[1] - self.controls.height):
            yOff = min_y * -1
        self.fit_to_screen(xOff, yOff, scale_factor)

    # translates the bottom-left corner of the tiling to the origin of the widget
    def fit_to_screen(self, xOff, yOff, scale_factor):
        temp_polygons = []
        for polygon in self.polygons:
            count = 0
            temp_poly = []
            for p in polygon:
                if count % 2 == 0:
                    temp_poly.append((p * scale_factor) + xOff)
                    #temp_poly.append((p * scale_factor))
                else:
                    temp_poly.append((p * scale_factor) + yOff)
                    #temp_poly.append((p * scale_factor))
                count += 1
            temp_polygons.append(temp_poly)
        self.polygons = temp_polygons