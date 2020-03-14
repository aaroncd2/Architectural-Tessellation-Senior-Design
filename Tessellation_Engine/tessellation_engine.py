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
        
        # create row for canvas
        self.canvas_widget = CanvasWidget()
        imageRow = BoxLayout(orientation='horizontal', padding=0, spacing=0)
        imageRow.add_widget(self.canvas_widget)
        self.add_widget(imageRow)

        self.controls = BoxLayout(orientation='horizontal', size_hint=(1,None), height=160)
        self.buttons = GridLayout(rows=4, cols=2)
        self.sliders = GridLayout(rows=4, cols=2)

        # Add slider and label to widget
        self.s = Slider(min=0, max=360, value=0, value_track = True)
        self.rotation_value = 0
        self.label_box = BoxLayout(orientation='horizontal', size_hint=(1,None), height=40)
        self.input_box = TextInput(text='0', input_filter='float', multiline=False)
        self.input_box.bind(on_text_validate=self.on_enter)
        self.label = Label(text ='Rotation:')
        self.label_box.add_widget(self.label)
        self.label_box.add_widget(self.input_box)
        self.sliders.add_widget(self.label_box) 
        self.sliders.add_widget(self.s)
        self.s.bind(value=self.rotate_polygon)

        # Add horizontal translation slider
        self.h_label = Label(text='Horizontal Spacing')
        self.sliders.add_widget(self.h_label)
        self.slide_horizontal = Slider(min=0, max=200, value=100, value_track = True)
        self.xSpacing = 100
        self.slide_horizontal.bind(value = self.adjust_horizontal_spacing)
        self.sliders.add_widget(self.slide_horizontal)

        # Add vertical translation slider
        self.v_label = Label(text='Vertical Spacing')
        self.sliders.add_widget(self.v_label)
        self.slide_vertical = Slider(min=0, max=200, value=100, value_track = True)
        self.ySpacing = 100
        self.slide_vertical.bind(value = self.adjust_vertical_spacing)
        self.sliders.add_widget(self.slide_vertical)

        # Add scale slider
        self.scale_label = Label(text='Scale')
        self.sliders.add_widget(self.scale_label)
        self.slide_scale = Slider(min=0, max=200, value=100, value_track = True)
        self.slide_scale.bind(value = self.scale_polygons)
        self.sliders.add_widget(self.slide_scale)

        self.controls.add_widget(self.sliders)

        # Add flip horizontal button
        self.horizontal_button = Button(text = 'Flip Horizontal', background_color = (1,1,1,1))
        self.buttons.add_widget(self.horizontal_button)
        self.horizontal_button.bind(on_press=self.flip_horizontal)

        # Add flip vertical button
        self.vertical_button = Button(text = 'Flip Vertical', background_color = (1,1,1,1))
        self.buttons.add_widget(self.vertical_button)
        self.vertical_button.bind(on_press=self.flip_vertical)

        # Add alternate row button
        self.alternate_row_button = Button(text = 'Alternate Rows', background_color = (1,1,1,1))
        self.buttons.add_widget(self.alternate_row_button)
        self.alternate_row_button.bind(on_press=self.alternate_rows)

        # Add alternate column button
        self.alternate_col_button = Button(text = 'Alternate Columns', background_color = (1,1,1,1))
        self.buttons.add_widget(self.alternate_col_button)
        self.alternate_col_button.bind(on_press=self.alternate_cols)

        # Add export button
        self.export_button = Button(text = 'Export', background_color = (1,1,1,1))
        self.buttons.add_widget(self.export_button)
        self.export_button.bind(on_press=self.export_tiling)

        # Add reset button
        self.reset_button = Button(text = 'Reset', background_color = (1,1,1,1))
        self.buttons.add_widget(self.reset_button)
        self.reset_button.bind(on_press=self.reset)

        # Add control row
        self.controls.add_widget(self.buttons)
        self.add_widget(self.controls)

        # Add recommendation buttons
        self.rec_label = Label(text='Tessellation Type:')
        self.buttons.add_widget(self.rec_label)
        self.rec_type = Label(text='Freeform')
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
        self.type = 'regular'
        polygon = tu.shapely_to_kivy(self.polygon)
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
        self.canvas_widget.canvas.add(Color(1., 0, 0))

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
        shape = tu.make_positive(self.rec_shape[0])
        exterior = tu.make_positive(self.rec_shape[3])
        bounds = exterior.bounds
        count = 0
        while count < 4:
            if exterior.exterior.coords[count][0] == bounds[2]:
                if count == 0:
                    xInc = max(exterior.exterior.coords[1][0], exterior.exterior.coords[3][0]) - bounds[0]
                elif count == 3:
                    xInc = max(exterior.exterior.coords[0][0], exterior.exterior.coords[2][0]) - bounds[0] 
                else:
                    xInc = max(exterior.exterior.coords[count + 1][0], exterior.exterior.coords[count - 1][0]) - bounds[0]   
            if exterior.exterior.coords[count][1] == bounds[3]:
                if count == 0:
                    if self.max_x_is_max_y(exterior):
                        yInc = min(exterior.exterior.coords[1][1], exterior.exterior.coords[3][1]) - bounds[1]
                    else:
                        yInc = max(exterior.exterior.coords[1][1], exterior.exterior.coords[3][1]) - bounds[1]
                elif count == 3:
                    if self.max_x_is_max_y(exterior):
                        yInc = min(exterior.exterior.coords[0][1], exterior.exterior.coords[2][1]) - bounds[1]
                    else:
                        yInc = max(exterior.exterior.coords[0][1], exterior.exterior.coords[2][1]) - bounds[1]
                else:
                    if self.max_x_is_max_y(exterior):
                        yInc = min(exterior.exterior.coords[count + 1][1], exterior.exterior.coords[count - 1][1]) - bounds[1]
                    else:
                        yInc = max(exterior.exterior.coords[count + 1][1], exterior.exterior.coords[count - 1][1]) - bounds[1]
            count = count + 1

        xInc2 = abs((bounds[2]-bounds[0]) - xInc)
        yInc2 = abs((bounds[3] - bounds[1])- yInc)
        if self.max_x_is_max_y(exterior):
            xInc3 = xInc2
            yInc3 = yInc2
        else:
            xInc3 = xInc - xInc2
            yInc3 = yInc2 + yInc
        #print(str(exterior))
        #print('X1: ' + str(xInc) + ' X2: ' + str(xInc2) + ' MAX X: ' + str(bounds[2]) + ' MIN X: ' + str(bounds[0]))
        #print('Y1: ' + str(yInc) + ' Y2: ' + str(yInc2) + ' MAX Y: ' + str(bounds[3]) + ' MIN Y: ' + str(bounds[1]))
        xInc = xInc * (self.xSpacing / 100)
        yInc = yInc * (self.ySpacing / 100)
        xCount = 1
        yCount = 1
        self.polygons = []
        while yCount <= self.yNum:
            while xCount <= self.xNum:
                temp = []
                for p in shape.exterior.coords:
                    px = ((p[0] + (xInc * xCount)) * scale_factor)  + ((xInc3 * (yCount - 1)) * scale_factor)
                    py = ((p[1] + (yInc * xCount)) * scale_factor) + ((yInc3 * (yCount - 1)) * scale_factor)
                    temp.append((px,py))
                temp_poly = Polygon(temp)
                temp_poly = affinity.rotate(temp_poly, self.s.value)
                self.polygons.append(tu.shapely_to_kivy(temp_poly))
                temp = None
                xCount = xCount + 1
            xCount = 1
            yCount = yCount + 1
        self.draw_polygons()

    # tiles a hexagon
    def tile_hexagon(self):
        bounds = self.polygon.bounds
        count = 0
        while count < 6:
            if self.polygon.exterior.coords[count][0] == bounds[2]:
                if count == 0:
                    xInc = max(self.polygon.exterior.coords[1][0], self.polygon.exterior.coords[5][0]) - bounds[0]
                elif count == 5:
                    xInc = max(self.polygon.exterior.coords[0][0], self.polygon.exterior.coords[4][0]) - bounds[0] 
                else:
                    xInc = max(self.polygon.exterior.coords[count + 1][0], self.polygon.exterior.coords[count - 1][0]) - bounds[0]    
            if self.polygon.exterior.coords[count][1] == bounds[3]:
                if count == 0:
                    yInc = max(self.polygon.exterior.coords[1][1], self.polygon.exterior.coords[5][1]) - bounds[1]
                elif count == 5:
                     yInc = max(self.polygon.exterior.coords[0][1], self.polygon.exterior.coords[4][1]) - bounds[1] 
                else:
                    yInc = max(self.polygon.exterior.coords[count + 1][1], self.polygon.exterior.coords[count - 1][1]) - bounds[1]
            count = count + 1

        xInc = xInc * (self.xSpacing / 100)
        yInc = yInc * (self.ySpacing / 100)
        xCount = 1
        yCount = 1
        self.polygons = []
        while yCount <= self.yNum:
            while xCount <= self.xNum:
                if xCount % 2 == 0:
                    temp_inc = (yInc/4) * -1
                else:
                    temp_inc = (yInc/4)
                temp = []
                for p in self.polygon.exterior.coords:
                    temp.append(((p[0] + (xInc * xCount)), (p[1] + (yInc * yCount))+temp_inc))
                temp_poly = Polygon(temp)
                self.polygons.append(tu.shapely_to_kivy(temp_poly))
                temp = None
                xCount = xCount + 1
            xCount = 1
            yCount = yCount + 1
        self.draw_polygons()

    # Rotates each polygon by the degrees specified by the slider
    def rotate_polygon(self, instance, degrees):
        self.polygon = affinity.rotate(self.base_unit, degrees)
        scale_factor = self.slide_scale.value / 100
        temp = []
        for p in self.polygon.exterior.coords:
            temp.append((p[0] * scale_factor, p[1] * scale_factor))
        self.polygon = Polygon(temp)
        if self.type == 'regular':
            self.tile_regular_polygon()
        elif self.type == 'parallelogram':
            self.tile_parallelogram()
        elif self.type == 'hexagon':
            self.tile_hexagon()
        self.label.text = 'Rotation:'
        self.input_box.text = str(round(self.s.value, 2))

    # Handles textbox input
    def on_enter(self, value):
        self.s.value = float(self.input_box.text)
        self.rotate_polygon(self.input_box, float(self.input_box.text))

    # flips a polygon horizontally across its center
    def flip_horizontal(self, instance):
        xCenter = self.polygon.centroid.x
        flipped = []
        for p in self.polygon.exterior.coords:
            point = ((2 * xCenter) - p[0], p[1])
            flipped.append(point)
        self.polygon = Polygon(flipped)
        polygon = tu.shapely_to_kivy(self.polygon)
        if self.type == 'regular':
            self.tile_regular_polygon()
        elif self.type == 'parallelogram':
            self.tile_parallelogram()
        elif self.type == 'hexagon':
            self.tile_hexagon()

    # flips a polygon vertically across its center
    def flip_vertical(self, instance):
        yCenter = self.polygon.centroid.y
        flipped = []
        for p in self.polygon.exterior.coords:
            point = (p[0], (2 * yCenter) - p[1])
            flipped.append(point)
        self.polygon = Polygon(flipped)
        polygon = tu.shapely_to_kivy(self.polygon)
        if self.type == 'regular':
            self.tile_regular_polygon()
        elif self.type == 'parallelogram':
            self.tile_parallelogram()
        elif self.type == 'hexagon':
            self.tile_hexagon()

    # resets the screen
    def reset(self, instance):
        self.slide_horizontal.value = 100
        self.xSpacing = 100
        self.slide_vertical.value = 100
        self.ySpacing = 100
        if instance != 1:
            self.slide_scale.value = 100
        #self.base_unit = self.original_base_unit
        self.polygon = self.base_unit
        self.tile_regular_polygon()
        self.type = 'regular'
        self.rec_type.text = 'Freeform'
        self.s.value = 0

    # Flips alternating rows across their center vertically
    def alternate_rows(self, instance):
        self.slide_horizontal.value = 100
        self.slide_vertical.value = 100
        bounds = self.polygon.bounds
        xInc = abs(bounds[2] - bounds[0])
        yInc = abs(bounds[3] - bounds[1])

        polygons = []
        temp = []
        xCount = 1
        yCount = 1
        self.canvas_widget.canvas.add(Color(1., 0, 0))

        while yCount <= self.yNum:
            yCenter = self.polygon.centroid.y
            flipped = []
            for p in self.polygon.exterior.coords:
                point = (p[0], (2 * yCenter) - p[1])
                flipped.append(point)
            self.polygon = Polygon(flipped)
            polygon = tu.shapely_to_kivy(self.polygon)
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

    # flips alternating columns across their center horizontally
    def alternate_cols(self, instance):
        self.slide_horizontal.value = 100
        self.slide_vertical.value = 100
        bounds = self.polygon.bounds
        xInc = abs(bounds[2] - bounds[0])
        yInc = abs(bounds[3] - bounds[1])

        polygons = []
        temp = []
        xCount = 1
        yCount = 1
        self.canvas_widget.canvas.add(Color(1., 0, 0))

        while yCount <= self.yNum:
            while xCount <= self.xNum:
                xCenter = self.polygon.centroid.x
                flipped = []
                for p in self.polygon.exterior.coords:
                    point = ((2 * xCenter) - p[0], p[1])
                    flipped.append(point)
                self.polygon = Polygon(flipped)
                polygon = tu.shapely_to_kivy(self.polygon)
                
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

    # Exports the currently displayed polygons to a CSV file
    def export_tiling(self, instance):
        points = {}
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
        df = pd.DataFrame(points)
        df.to_csv(r'output.csv', index=None)

    # Draws an array of polygons to the canvas
    def draw_polygons(self):
        self.scale_to_fit_window()
        self.canvas_widget.lines.clear()
        self.canvas_widget.lines.add(Color(1., 0, 0))
        for polygon in self.polygons:
            self.canvas_widget.lines.add(Line(points = polygon, width=2.0, close=False))
        self.canvas_widget.canvas.add(self.canvas_widget.lines)

    # Adjusts horizontal spacing between polygons
    def adjust_horizontal_spacing(self, instance, amount):
        self.xSpacing = self.slide_horizontal.value
        if self.type == 'regular':
            self.tile_regular_polygon()
        elif self.type == 'parallelogram':
            self.tile_parallelogram()
        elif self.type == 'hexagon':
            self.tile_hexagon()
            
    # Adjusts vertical spacing between polygons
    def adjust_vertical_spacing(self, instance, amount):
        self.ySpacing = self.slide_vertical.value
        if self.type == 'regular':
            self.tile_regular_polygon()
        elif self.type == 'parallelogram':
            self.tile_parallelogram()
        elif self.type == 'hexagon':
            self.tile_hexagon()

    def scale_polygons(self, instance, amount):
        scale_factor = self.slide_scale.value / 100
        temp = []
        for p in self.base_unit.exterior.coords:
            temp.append((p[0] * scale_factor, p[1] * scale_factor))
        self.polygon = Polygon(temp)
        self.polygon = affinity.rotate(self.polygon, self.s.value)
        if self.type == 'regular':
            self.tile_regular_polygon()
        elif self.type == 'parallelogram':
            self.tile_parallelogram()
        elif self.type == 'hexagon':
            self.tile_hexagon()

    # displays the next recommendation to the screen
    def draw_recommendation(self, index):
        self.reset(0)
        self.rec_shape = self.shape_info[index]
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

    # determines if a coordinate in a shape is (maxX, maxY)
    def max_x_is_max_y(self, polygon):
        bounds = polygon.bounds
        for p in polygon.exterior.coords:
            if (p[0] == bounds[2] and p[1] == bounds[3]) or (p[0] == bounds[0] and p[1] == bounds[3]):
                return True
        return False

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