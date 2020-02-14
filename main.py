from Image_Processing import image_processing as ip
from Shape_Modeling import shape_modeling as sm
from Tessellation_Engine import tessellation_engine as te
from Tessellation_Engine.tessellation_engine import TessellationWidget
from Tessellation_Engine.tessellation_engine import CanvasWidget
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
                global f_coords
                coo = ip.processImage(fp)
                f_coords = sm.shape_model(coo)
                print(f_coords)
                b_grid = BoxGrid()
                popup.parent.add_widget(b_grid)
                popup.dismiss()
            else:
                self.ids.image.source = filename[0]
                
#layout class
class BoxGrid(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxGrid, self).__init__(**kwargs)
        self.b_coords = f_coords
        custlay = CustomLayout()
        tessel = TessellationWidget()
        self.add_widget(custlay)
        self.add_widget(tessel)
        tessel.display_initial_tiling()
#layout for the main canvas
class CustomLayout(BoxLayout):

    def __init__(self, **kwargs):
        self.c_coords = f_coords
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
        for points in self.c_coords:
            self.canvas.add(self.canvas_nodes[i])
            i = i + 1
        self.define_edge()
        self.canvas.add(self.canvas_edge)
        


    def define_nodes(self):
        """define all the node canvas elements as a list"""
        print("Hello")
        #print(coords)
        poly = Polygon(self.c_coords)
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
        for points in self.c_coords:
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
            for points in self.c_coords:
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
            


#main app class to build the root widget on program start
class DatoApp(App):
    def build(self):
       
        return RootWidget()

if __name__ == '__main__':
    DatoApp().run()
   
   