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
from kivy.uix.relativelayout import RelativeLayout
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
import os
import sys
from kivy.core.window import Window

Window.fullscreen = 'auto'
size = Window.size

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
    def getpath(self):
        with open('pathfile.txt', 'r') as f:
            data = f.read()
        if (data != None):
            return data
        else:
            return ""
        print(data)
        print(self.rootpath)
    def selected(self,filename,*args):
            if (filename == True):
                
                global fp
                #store file path
                fp = args[0][0]
                with open('pathfile.txt', 'w') as f:
                    data = fp
                    head, tail = os.path.split(data)
                    f.write(head)
                    
                print(fp)
                #use file path to process as image in imageprocessing.py
                global coords
                coo = ip.processImage(fp)
                coords = sm.shape_model(coo)
                print(coords)
                b_grid = BoxGrid()
                popup.parent.add_widget(b_grid)
                popup.dismiss()
            else:
                self.ids.image.source = filename[0]
                
#layout class
class BoxGrid(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxGrid, self).__init__(**kwargs)
        custlay = CustomLayout()
        tessel = TessellationWidget()
        self.add_widget(custlay)
        self.add_widget(tessel)
#layout for the main canvas
class CustomLayout(BoxLayout):

    def __init__(self, **kwargs):
        print("Size is")
        print(Window.size)
        super(CustomLayout, self).__init__(**kwargs)
        self.canvas_edge = {}
        self.canvas_nodes = {}
        self.nodesize = [20, 20]
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
        


    def define_nodes(self):
        """define all the node canvas elements as a list"""
        print("Hello")
        #print(coords)
        poly = Polygon(coords)
        print(size)
        poly = affinity.translate(poly, xoff= size[0]/2, yoff= size[1]/2)
        poly = affinity.scale(poly, xfact= 1/poly.bounds[2], yfact= 1/poly.bounds[3])
        poly = affinity.scale(poly, xfact= 10, yfact= 10)
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
            poly = []
            i = 0
            for xy in self.canvas_nodes:
                poly.append(self.canvas_nodes[i].pos)
                i = i + 1
            print(poly)
            #poly = affinity.translate(poly, xoff= size[0]/2, yoff= size[1]/2)
            newply = Polygon(poly)
            newply = affinity.translate(newply, xoff= -size[0]/2, yoff= -size[1]/2)
            print(self.parent.children[0].polygon)
            self.parent.children[0].polygon = newply
            print(self.parent.children[0].polygon)  
            #self.parent.children[0].polygon = self.parent.children[0].shapely_to_kivy(self.parent.children[0].polygon)
            self.parent.children[0].tile_regular_polygon()
            
        else:
            pass
            
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

        self.controls = BoxLayout(orientation='horizontal', size_hint=(1,None), height=120)
        self.buttons = GridLayout(rows=3, cols=2)
        self.sliders = GridLayout(rows=4, cols=2)
        self.recommend_buttons = BoxLayout(orientation='horizontal', size_hint=(1,None), height=33)

        # Add slider and label to widget
        self.s = Slider(min=0, max=360, value=0, value_track = True)
        self.rotation_value = 0
        self.label = Label(text ='Rotation: ' + str(self.rotation_value) + ' degrees')
        self.sliders.add_widget(self.label) 
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
        self.rec_left = Button(text='Previous Recommendation', background_color = (1,1,1,1))
        self.recommend_buttons.add_widget(self.rec_left)
        self.rec_right = Button(text='Next Recommendation', background_color = (1,1,1,1))
        self.recommend_buttons.add_widget(self.rec_right)
        #self.add_widget(self.recommend_buttons)

        # Display initial tiling
        self.xNum = 5
        self.yNum = 5
        #points = [(5,5),(105,5),(125,50),(25,50)] #Rhombus
        points = [(0,0),(100,0),(100,100),(0,100),(0,0)] #Square
        self.type = 'regular'
        self.polygon = Polygon(points)
        self.base_unit = self.polygon
        polygon = self.shapely_to_kivy(self.polygon)
        self.tile_regular_polygon()

    # Tiles polygons in an xNum by yNum grid utilizing bounding boxes
    def tile_regular_polygon(self):
        polygon = self.shapely_to_kivy(self.polygon)
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

    # Takes a Shapely Polygon object and converts it to an array format for display
    # on a Kivy canvas 
    def shapely_to_kivy(self, polygon):
        kivy_points = []
        for p in polygon.exterior.coords:
            kivy_points.append(p[0])
            kivy_points.append(p[1])
        return kivy_points

    def kivy_to_shapely(self, polygon):
        shapely_points = []
        xs = []
        ys = []
        count = 0
        for p in polygon:
            if count % 2 == 0:
                xs.append(p)
            else:
                ys.append(p)
            count = count + 1
        for (x,y) in zip(xs,ys):
            shapely_points.append((x,y))
        return shapely_points

    # Rotates each polygon by the degrees specified by the slider
    def rotate_polygon(self, instance, degrees):
        self.polygon = affinity.rotate(self.base_unit, degrees)
        scale_factor = self.slide_scale.value / 100
        temp = []
        for p in self.polygon.exterior.coords:
            temp.append((p[0] * scale_factor, p[1] * scale_factor))
        self.polygon = Polygon(temp)
        self.tile_regular_polygon()
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
        self.tile_regular_polygon()

    # flips a polygon vertically across its center
    def flip_vertical(self, instance):
        yCenter = self.polygon.centroid.y
        flipped = []
        for p in self.polygon.exterior.coords:
            point = (p[0], (2 * yCenter) - p[1])
            flipped.append(point)
        self.polygon = Polygon(flipped)
        polygon = self.shapely_to_kivy(self.polygon)
        self.tile_regular_polygon()

    # resets the screen
    def reset(self, instance):
        self.slide_horizontal.value = 100
        self.xSpacing = 100
        self.slide_vertical.value = 100
        self.ySpacing = 100
        self.slide_scale.value = 100
        self.polygon = self.base_unit
        polygon = self.shapely_to_kivy(self.polygon)
        self.tile_regular_polygon()
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

        self.polygons = polygons
        self.draw_polygons()

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
        self.canvas_widget.lines.clear()
        self.canvas_widget.lines.add(Color(1., 0, 0))
        for polygon in self.polygons:
            self.canvas_widget.lines.add(Line(points = polygon, width=2.0))
        self.canvas_widget.canvas.add(self.canvas_widget.lines)

    # Adjusts horizontal spacing between polygons
    def adjust_horizontal_spacing(self, instance, amount):
        self.xSpacing = self.slide_horizontal.value
        if self.type == 'regular':
            self.tile_regular_polygon()

    # Adjusts vertical spacing between polygons
    def adjust_vertical_spacing(self, instance, amount):
        self.ySpacing = self.slide_vertical.value
        if self.type == 'regular':
            self.tile_regular_polygon()

    def scale_polygons(self, instance, amount):
        scale_factor = self.slide_scale.value / 100
        temp = []
        for p in self.base_unit.exterior.coords:
            temp.append((p[0] * scale_factor, p[1] * scale_factor))
        self.polygon = Polygon(temp)
        self.polygon = affinity.rotate(self.polygon, self.s.value)
        if self.type == 'regular':
            self.tile_regular_polygon()
## END TESSEL ENG ##

#main app class to build the root widget on program start
class DatoApp(App):
    def build(self):
       
        return RootWidget()

if __name__ == '__main__':
    DatoApp().run()
   
   