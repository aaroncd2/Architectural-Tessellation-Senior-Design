from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import *
from shapely.geometry import Polygon # for geometric objects
from shapely import affinity # for transformations
import matplotlib.pyplot as plt # for display
import math # for trig functions
import pandas as pd # for export
import numpy as np # for math

class CanvasWidget(Widget):
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
        imageRow = BoxLayout(orientation='horizontal')
        imageRow.add_widget(self.canvas_widget)
        self.add_widget(imageRow)

        self.rotateRow = BoxLayout(orientation='horizontal', size_hint=(1,None), height=50)
        

        # Add slider and label to widget
        self.s = Slider(min=0, max=360, value=0, value_track = True)
        self.rotation_value = 0
        self.label = Label(text ='Rotation: ' + str(self.rotation_value) + ' degrees')
        self.rotateRow.add_widget(self.label) 
        self.rotateRow.add_widget(self.s)
        self.s.bind(value=self.rotate_polygon)
        self.add_widget(self.rotateRow)

        self.controlRow = BoxLayout(orientation='horizontal', size_hint=(1,None), height=50)

        # Add flip horizontal button
        self.horizontal_button = Button(text = 'Flip Horizontal', background_color = (1,1,1,1))
        self.controlRow.add_widget(self.horizontal_button)
        self.horizontal_button.bind(on_press=self.flip_horizontal)

        # Add flip vertical button
        self.vertical_button = Button(text = 'Flip Vertical', background_color = (1,1,1,1))
        self.controlRow.add_widget(self.vertical_button)
        self.vertical_button.bind(on_press=self.flip_vertical)

        # Add alternate row button
        self.alternate_row_button = Button(text = 'Alternate Rows', background_color = (1,1,1,1))
        self.controlRow.add_widget(self.alternate_row_button)
        self.alternate_row_button.bind(on_press=self.alternate_rows)

        # Add alternate column button
        self.alternate_col_button = Button(text = 'Alternate Columns', background_color = (1,1,1,1))
        self.controlRow.add_widget(self.alternate_col_button)
        self.alternate_col_button.bind(on_press=self.alternate_cols)

        # Add export button
        self.export_button = Button(text = 'Export', background_color = (1,1,1,1))
        self.controlRow.add_widget(self.export_button)
        self.export_button.bind(on_press=self.export_tiling)

        # Add reset button
        self.reset_button = Button(text = 'Reset', background_color = (1,1,1,1))
        self.controlRow.add_widget(self.reset_button)
        self.reset_button.bind(on_press=self.reset)

        # Add control row
        self.add_widget(self.controlRow)

        # Display initial tiling
        points = [(5,5),(100,5),(100,100),(5,100),(5,5)] #Square
        self.xNum = 5
        self.yNum = 5
        #points = [(0,0),(50,0),(80,40),(30,40)] #Rhombus
        #points = [(0,0),(100,0),(100,50),(0,50)] #Rectangle
        #points = [(100,100),(0,100),(76.25,50),(50,150),(12.5,25)] #Star
        self.polygon = Polygon(points)
        self.base_unit = self.polygon
        polygon = self.shapely_to_kivy(self.polygon)
        self.tile_regular_polygon(polygon)


    # Tiles polygons in an xNum by yNum grid utilizing bounding boxes
    def tile_regular_polygon(self, polygon):
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

        self.canvas_widget.lines.clear()
        self.canvas_widget.lines.add(Color(1., 0, 0))
        self.polygons = polygons
        for polygon in polygons:
            self.canvas_widget.lines.add(Line(points = polygon, width=2.0))
        self.canvas_widget.canvas.add(self.canvas_widget.lines)

    # Takes a Shapely Polygon object and converts it to an array format for display
    # on a Kivy canvas 
    def shapely_to_kivy(self, polygon):
        kivy_points = []
        for p in polygon.exterior.coords:
            kivy_points.append(p[0])
            kivy_points.append(p[1])
        return kivy_points

    # Rotates each polygon by the degrees specified by the slider
    def rotate_polygon(self, instance, degrees):
        self.polygon = affinity.rotate(self.base_unit, degrees)
        polygon = self.shapely_to_kivy(self.polygon)
        self.tile_regular_polygon(polygon)
        self.label.text = 'Rotation: ' + str(round(self.s.value, 2)) + ' degrees'

    # flips a polygon horizontally across its center
    def flip_horizontal(self, instance):
        xCenter = self.polygon.centroid.x
        flipped = []
        for p in self.polygon.exterior.coords:
            point = ((2 * xCenter) - p[0], p[1])
            flipped.append(point)
        self.polygon = Polygon(flipped)
        polygon = self.shapely_to_kivy(self.polygon)
        self.tile_regular_polygon(polygon)

    # flips a polygon vertically across its center
    def flip_vertical(self, instance):
        yCenter = self.polygon.centroid.y
        flipped = []
        for p in self.polygon.exterior.coords:
            point = (p[0], (2 * yCenter) - p[1])
            flipped.append(point)
        self.polygon = Polygon(flipped)
        polygon = self.shapely_to_kivy(self.polygon)
        self.tile_regular_polygon(polygon)

    # resets the screen
    def reset(self, instance):
        self.polygon = self.base_unit
        polygon = self.shapely_to_kivy(self.polygon)
        self.tile_regular_polygon(polygon)
        self.s.value = 0

    # Flips alternating rows across their center vertically
    def alternate_rows(self, instance):
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
            polygon = self.shapely_to_kivy(self.polygon)
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

        self.canvas_widget.lines.clear()
        self.canvas_widget.lines.add(Color(1., 0, 0))
        self.polygons = polygons
        for polygon in polygons:
            self.canvas_widget.lines.add(Line(points = polygon, width=2.0))
        self.canvas_widget.canvas.add(self.canvas_widget.lines)

    # flips alternating columns across their center horizontally
    def alternate_cols(self, instance):
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
                polygon = self.shapely_to_kivy(self.polygon)
                
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

        self.canvas_widget.lines.clear()
        self.canvas_widget.lines.add(Color(1., 0, 0))
        self.polygons = polygons
        for polygon in polygons:
            self.canvas_widget.lines.add(Line(points = polygon, width=2.0))
        self.canvas_widget.canvas.add(self.canvas_widget.lines)

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
        df.to_csv(r'output.csv', index=False)

class MyTestApp(App):
    def build(self):
        return TessellationWidget()


if __name__ == '__main__':
    MyTestApp().run()