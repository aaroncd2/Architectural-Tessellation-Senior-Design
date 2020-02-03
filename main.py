from Image_Processing import image_processing as ip
from Shape_Modeling import shape_modeling as sm
from Tessellation_Engine import tessellation_engine as te
from Tessellation_Engine import recommendation_system as rs
import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from shapely.geometry import Polygon, Point
from shapely import affinity
import matplotlib.pyplot as plt # for display
import math # for trig functions
import pandas as pd # for export
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
import numpy
import sys
from kivy.core.window import Window

#Window.fullscreen = 'auto'
size = Window.size

#not sure yet best way to store these coords 
#for now they are global vars

#root widget class using the box layout
#adds button on init to open file dialog class
class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
         super(RootWidget, self).__init__(**kwargs)
         self.cb = Button(text='select a file')
         #bind and add file dialog button to root widget
         self.cb.bind(on_press=self.file_diag)
         self.add_widget(self.cb)
    #file dialog button callback to open popup
    def file_diag(self,instance):
        #remove button
        self.remove_widget(self.cb)
        global popup
        #open file dialog popup
        popup = Popup(title='Select File',
                      content=FileChooser())
        popup.open()
        
        
#gile chooser class
class FileChooser(FileChooserListView):
    def selected(self,filename,*args):
            print(filename==True)
            print(filename==False)
            print(args)
            if (filename == True):
                print("here")
                print(args[0][0])
                global fp
                #store file path
                fp = args[0][0]
                print(fp)
                #use file path to process as image in imageprocessing.py
                global coords
                coo = ip.processImage(fp)
                coords = sm.shape_model(coo)
                print(coords)
                print("Coo =")
                print(coo)
                custlay = CustomLayout()
                popup.parent.add_widget(custlay)
                popup.dismiss()
                print("dismiss called")
            else:
                self.ids.image.source = filename[0]
        
        
class CustomLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(CustomLayout, self).__init__(**kwargs)
        print("Im here")
        self.canvas_edge = {}
        self.canvas_nodes = {}
        self.nodesize = [20, 20]
        print("he now")
        self.grabbed = {}

        #declare a canvas
        with self.canvas.after:
            pass
        print("here now")
        self.define_nodes()
        print("define nodes")
        i = 0
        for points in coords:
            self.canvas.add(self.canvas_nodes[i])
            i = i + 1
        self.define_edge()
        self.canvas.add(self.canvas_edge)
        tessel = TessellationWidget()
        print('hello')
        print(self.parent)
        self.parent.add_widget(tessel)


    def define_nodes(self):
        """define all the node canvas elements as a list"""
        print("Hello")
        #print(coords)
        poly = Polygon(coords)
        print(size)
        poly = affinity.translate(poly, xoff= size[0]/2, yoff= size[1]/2)
        #poly = affinity.scale(poly, xfact= 1/poly.bounds[2], yfact= 1/poly.bounds[3])
        # poly = affinity.scale(poly, xfact= 10, yfact= 10)
        coords2 = list(poly.exterior.coords)

        i = 0
        for points in coords2:
            x,y = points
            self.canvas_nodes[i] = Ellipse(
                size = self.nodesize,
                pos =  [x,y]
                )
            i = i + 1

    def define_edge(self):
        """define an edge canvas elements"""
        i = 0
        xy = []
        for points in coords:
            xy.append(self.canvas_nodes[i].pos[0] + self.nodesize[0] / 2)
            xy.append(self.canvas_nodes[i].pos[1] + self.nodesize[1] / 2)
            i = i + 1
        self.canvas_edge = Line(
            points =  xy,
            joint = 'round',
            cap = 'round',
            width = 3,
            close = True
            )

    def on_touch_down(self, touch):

        for key, value in self.canvas_nodes.items():
            if (value.pos[0] - self.nodesize[0]) <= touch.pos[0] <= (value.pos[0] + self.nodesize[0]):
                if (value.pos[1] - self.nodesize[1]) <= touch.pos[1] <= (value.pos[1] + self.nodesize[1]):
                    touch.grab(self)
                    self.grabbed = self.canvas_nodes[key]
                    return True

    def on_touch_move(self, touch):

        if touch.grab_current is self:
            self.grabbed.pos = [touch.pos[0] - self.nodesize[0] / 2, touch.pos[1] - self.nodesize[1] / 2]
            self.canvas.clear()
            i = 0
            for points in coords:
                self.canvas.add(self.canvas_nodes[i])
                i = i + 1
            self.define_edge()
            self.canvas.add(self.canvas_edge)
        else:
            pass

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        else:
            pass

### START TESSELLATION ENGINE ###
            
class CanvasWidget(Widget):
    def __init__(self, **kwargs):
        print("canvas widge")
        super(CanvasWidget, self).__init__(**kwargs)
        print("super")
        self.lines = InstructionGroup()
        print("yolo")

class TessellationWidget(GridLayout):
    def __init__(self, **kwargs):
        print("hello")
        super(TessellationWidget, self).__init__(**kwargs)
        self.cols = 1
        print (self.cols)
        self.rows = 3
        print (self.rows)
        self.polygons = []
        print (self.polygons)
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
        
        
## END TESSEL ENG ##

#main app class to build the root widget on program start
class DatoApp(App):
    def build(self):
       
        return RootWidget()

if __name__ == '__main__':
    DatoApp().run()
   
   
    