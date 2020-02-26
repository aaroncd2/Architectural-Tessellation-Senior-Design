from Image_Processing import image_processing as ip
from Shape_Modeling import shape_modeling as sm
from Tessellation_Engine import tessellation_engine as te
from Tessellation_Engine.tessellation_engine import TessellationWidget
from Tessellation_Engine.tessellation_engine import CanvasWidget
from Tessellation_Engine import recommendation_system as rs
from Shape_Identification import tiling_rules as tr
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



def angle(a, c, b):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    if abs(ang) > 170 and abs(ang) < 190:
        return True
    else:
        return False

def midpoint(points):
    mid = [(points[0]+points[2])/2 - 10, (points[1] + points[3])/2 - 10]
    return mid

#adds button on init to open file dialog class
class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        global size
        size = Window.size
         #self.cb = Button(text='select a file')
         #bind and add file dialog button to root widget
         #self.cb.bind(on_press=self.file_diag)
         #self.add_widget(self.cb)
        fchooser = FileChooser()
        self.add_widget(fchooser)
    #file dialog button callback to open popup
    #def file_diag(self,instance):
        #remove button
        #self.remove_widget(self.cb)
        #open file dialog popup
        #popup = Popup(title='Select File',content=FileChooser())
        #popup.open()
               
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
                self.parent.add_widget(b_grid)
                self.parent.remove_widget(self)
            else:
                self.ids.image.source = filename[0]

class ReccomendationButton(Button):
    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        #self.size = 175, 145
        self.index = None
        if (the_poly != None):
            with self.canvas.after:
                Line(points = the_poly)
            with self.canvas.before:
                Line(points = the_poly) 

    def on_press(self, **kwargs):
        print(self.index)
        self.parent.parent.parent.children[1].draw_recommendation(self.index)
class ReccomendationButtons(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        
        
        self.size_hint= None, None 
    def setup_btns(self):
        
        self.btns_info = self.parent.main_shape_info
        self.numreccs = len(self.btns_info) #hardcoded for now
        print("shape info")
        print(self.btns_info)
        print(self.numreccs)
        self.reccrows= GridLayout(rows=self.numreccs , cols=1)
        self.reccrows.size_hint = None, None
        global the_poly
        the_poly = self.make_positive(self.btns_info[0][0])

        poly = Polygon(the_poly)
        sizeX = Window.size[0] * (.14)
        sizeY = Window.size[1] / self.numreccs
        xdistnace = (poly.bounds[2] - poly.bounds[0])
        ydistance = (poly.bounds[3] - poly.bounds[1])
        xscale = sizeX * .5 / xdistnace
        yscale = sizeY * .5 / ydistance
        center = (poly.centroid.coords[0])
        xoff = (sizeX/2) - center[0]
        Yoff = (sizeY/2) - center[1]
        
        if xscale > yscale:
            the_poly = affinity.scale(the_poly, xfact= xscale, yfact= yscale)
        else:
            the_poly = affinity.scale(the_poly, xfact= xscale, yfact= xscale)
        
        the_poly = affinity.translate(the_poly, xoff= xoff, yoff=Yoff)

        

        the_poly = self.shapely_to_kivy(the_poly)
        with self.canvas.after:
            Line(points = the_poly)

        self.reccrows.size = (Window.size[0] * (.14)), Window.size[1]
        for k in range(0, self.numreccs):
            if (k != 0):
                the_poly = self.make_positive(self.btns_info[k][0])
                btn_height = (Window.size[1] / self.numreccs)
                yoff = (btn_height * k)
                the_poly = affinity.translate(the_poly, xoff= xoff, yoff=Yoff + yoff)
                if xscale > yscale:
                    the_poly = affinity.scale(the_poly, xfact= xscale, yfact= yscale)
                else:
                    the_poly = affinity.scale(the_poly, xfact= xscale, yfact= xscale)
                the_poly = self.shapely_to_kivy(the_poly)
            else:
                the_poly = None
            temp = ReccomendationButton()
            the_poly = None
            if (self.numreccs == 3):
                if (k==0):
                    temp.index = 2
                elif (k ==1):
                    temp.index = 1
                elif (k == 2):
                    temp.index = 0
            elif (self.numreccs == 2):
                if (k==0):
                    temp.index = 1
                elif (k ==1):
                    temp.index = 0
            #temp.index = k
            
            #temp.lines.add(Line(points = self.shapely_to_kivy(self.btns_info[k][0]) , width = 2.0, close = False)) 
            self.reccrows.add_widget(temp)            

        self.add_widget(self.reccrows)
    
    def shapely_to_kivy(self, polygon):
        kivy_points = []
        for p in polygon.exterior.coords:
            kivy_points.append(p[0])
            kivy_points.append(p[1])
        return kivy_points
    #offsets a polygon to ensure all its vertices are positive
    def make_positive(self, polygon):
        bounds = polygon.bounds
        temp = []
        if bounds[0] < 0 and bounds[1] < 0:
            for p in polygon.exterior.coords:
                temp.append((p[0] + abs(bounds[0]), p[1] + abs(bounds[1])))
            return Polygon(temp)
        elif bounds[1] < 0:
            for p in polygon.exterior.coords:
                temp.append((p[0], p[1] + abs(bounds[1])))
            return Polygon(temp)
        elif bounds[0] < 0:
            for p in polygon.exterior.coords:
                temp.append((p[0] + abs(bounds[0]), p[1]))
            return Polygon(temp)
        else:
            return polygon

        
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
        self.main_shape_info = tessel.shape_info
        btn = ReccomendationButtons()
        self.add_widget(btn)
        btn.setup_btns()
#layout for the main canvas

class CustomLayout(BoxLayout):
    def __init__(self, **kwargs):

        super(CustomLayout, self).__init__(**kwargs)

        Window.bind(on_key_down=self.key_action) #Binds Keyboard for key detection

        self.c_coords = f_coords
        self.pressed = False
        self.index = -1
        self.edge = -1 
        
        self.canvas_edge = {}
        self.canvas_nodes = {}
        self.nodesize = [20, 20]

        self.grabbed = {}

        self.configCoords()

        #declare a canvas
        with self.canvas.after:
            pass

        self.define_nodes()

        i = 0
        for points in self.c_coords:
            self.canvas.add(self.canvas_nodes[i])
            i = i + 1
        
        self.define_edge()

        i = 0
        for i in range(len(self.c_coords)):
            self.canvas.add(self.canvas_edge[i])
            i = i + 1
       
    def configCoords(self):
        poly = Polygon(self.c_coords)

        sizeX = Window.size[0]
        sizeY = Window.size[1]
        xdistnace = (poly.bounds[2] - poly.bounds[0])
        ydistance = (poly.bounds[3] - poly.bounds[1])
        xscale = sizeX * .25 / xdistnace
        yscale = sizeY * .25 / ydistance
        center = (poly.centroid.coords[0])
        xoff = (sizeX/4) - center[0]
        yoff = (sizeY/4) - center[1]

        poly = affinity.translate(poly, xoff= xoff, yoff= yoff)
        if xscale > yscale:
            poly = affinity.scale(poly, xfact= yscale, yfact= yscale)
        else:
            poly = affinity.scale(poly, xfact= xscale, yfact= xscale)
        self.c_coords = list(poly.exterior.coords)
        self.c_coords.pop(-1)
        
        temp2 = []
        for x in self.c_coords:
            temp = []
            for y in x:
                temp.append(int(y))
            temp2.append(tuple(temp))
        self.c_coords = temp2
        self.orgi_coords = self.c_coords
        
    def key_action(self, *args):
       
        key_pressed = list(args)
        print(key_pressed)

        #Delete when pressing delete
        if key_pressed[2] == 42 and self.pressed and len(self.canvas_edge) > 3:
            self.pressed = False
            self.canvas.children.remove(self.highlight)

            if self.edge:
                self.canvas.children.remove(self.canvas_edge[self.index])
                self.canvas.children.remove(self.canvas_nodes[self.index])
                self.canvas.children.remove(self.canvas_nodes[(self.index+1)%len(self.canvas_nodes)])

                mid = midpoint(self.canvas_edge[self.index].points)

                self.c_coords.insert((self.index+1)%len(self.canvas_nodes), tuple(mid))
                self.c_coords.remove(self.canvas_nodes[self.index].pos)
                self.c_coords.remove(self.canvas_nodes[(self.index+1)%len(self.canvas_nodes)].pos)
            elif not self.edge:
                self.canvas.children.remove(self.canvas_nodes[self.index])
                self.c_coords.remove(self.canvas_nodes[self.index].pos)

            self.draw()

        #Add when pressing a
        elif key_pressed[2] == 4 and self.pressed:
            try:
                self.canvas.children.remove(self.highlight)
                mid = midpoint(self.canvas_edge[self.index].points)
                print(self.highlight.points)
                self.c_coords.insert((self.index+1)%len(self.canvas_nodes), tuple(mid))
                self.draw()
                
            except:
                print(' Point selected')
            self.pressed = False
        
        #Reset when pressing r
        elif key_pressed[2] == 21:
            self.c_coords = self.orgi_coords
            self.draw()
                
        poly = []
        i = 0
        for xy in self.canvas_nodes:
            poly.append(self.canvas_nodes[i].pos)
            i = i + 1

        newply = Polygon(poly)
        newply = affinity.translate(newply, xoff= -size[0]/2, yoff= -size[1]/2)
        self.parent.children[1].reset(0)
        self.parent.children[1].polygon = newply
        self.parent.children[1].tile_regular_polygon()

    def draw(self):
        self.canvas.clear()
        self.define_nodes()
        i = 0
        for i in range(len(self.c_coords)):
            self.canvas.add(self.canvas_nodes[i])
            i = i + 1
        self.define_edge()

        i = 0
        for i in range(len(self.c_coords)):
            self.canvas.add(self.canvas_edge[i])
            i = i + 1        
    
    def define_nodes(self):

        self.canvas_nodes.clear()
        
        """define all the node canvas elements as a list"""
       
        i = 0
        for points in self.c_coords:
            x,y = points
            self.canvas_nodes[i] = Ellipse(
                size = self.nodesize,
                pos =  [x,y],
                )
            i = i + 1
            
    def define_edge(self):
        """define an edge canvas elements"""
        self.canvas_edge.clear()
        i = 0
        xy = []
        for points in self.c_coords:
            xy.append(self.canvas_nodes[i].pos[0] + self.nodesize[0] / 2)
            xy.append(self.canvas_nodes[i].pos[1] + self.nodesize[1] / 2)
            i = i + 1

        test = []
        i = 0
        while i < (len(xy)):
            if i + 2 == len(xy):
                test.append((xy[-2], xy[-1],xy[0], xy[1]))
            else:
                test.append(tuple(xy[i:i+4]))
            i = i + 2

        i = 0
        for point in test:
            self.canvas_edge[i] =  Line(
                points =  test[i],
                joint = 'round',
                cap = 'round',
                width = 3,
                close = False
                )
            i = i + 1

    def on_touch_down(self, touch):       
        i = 0
        for lines in self.canvas_edge:
            x,y = self.canvas_edge[i].points[0], self.canvas_edge[i].points[1]
            a = [x,y]
            x,y = self.canvas_edge[i].points[2], self.canvas_edge[i].points[3]
            b = [x,y]
            c = list(touch.pos)
            if angle(a,b,c) and not self.pressed:
                points = [a,b]
                self.canvas.add(Color(1,0,0, .5))
                self.highlight = Line(
                    points = points, 
                    width = 5
                    )
                self.canvas.add(self.highlight)
                self.pressed = True
                self.index = i
                self.edge = 1
                break
            else:
                if self.pressed:
                    self.pressed = False
                    self.canvas.children.remove(self.highlight)
            i = i + 1
           
        for key, value in self.canvas_nodes.items():
            if (value.pos[0] - self.nodesize[0]) <= touch.pos[0] <= (value.pos[0] + self.nodesize[0]):
                if (value.pos[1] - self.nodesize[1]) <= touch.pos[1] <= (value.pos[1] + self.nodesize[1]):                    
                    touch.grab(self)
                    self.grabbed = self.canvas_nodes[key]       
                    self.canvas.add(Color(1,0,0, .5))
                    self.highlight = Ellipse(
                        size = self.nodesize,
                        pos =  self.canvas_nodes[key].pos
                        )
                    if not self.pressed:
                        self.canvas.add(self.highlight)
                        self.pressed = True
                        self.index = key
                        self.edge = 0
                    elif self.pressed:
                        self.pressed = False
                        try:
                            self.canvas.children.remove(self.highlight)
                        except:
                            pass
                    return True
            
    def on_touch_move(self, touch):
        self.pressed = False
        if touch.grab_current is self:
            self.grabbed.pos = [touch.pos[0] - self.nodesize[0] / 2, touch.pos[1] - self.nodesize[1] / 2]
            self.canvas.clear()
            i = 0
            for i in range(len(self.c_coords)):
                self.canvas.add(self.canvas_nodes[i])
                i = i + 1
            self.define_edge()

            i = 0
            for i in range(len( self.c_coords)):
                self.canvas.add(self.canvas_edge[i])
                i = i + 1

            poly = []
            i = 0
            for xy in self.canvas_nodes:
                poly.append(self.canvas_nodes[i].pos)
                i = i + 1

            newply = Polygon(poly)
            newply = affinity.translate(newply, xoff= -size[0]/2, yoff= -size[1]/2)
            self.parent.children[1].reset(0)
            self.parent.children[1].polygon = newply
            self.parent.children[1].tile_regular_polygon()
        else:
            pass
    
    def on_touch_up(self, touch):    
        temp = []
        i = 0
        for i in range(len(self.c_coords)):
            temp.append(self.canvas_nodes[i].pos)
            i = i + 1
        self.c_coords = temp

        if touch.grab_current is self:
            touch.ungrab(self)
            poly = []
            i = 0
            for xy in self.canvas_nodes:
                poly.append(self.canvas_nodes[i].pos)
                i = i + 1

            print(poly)
            newply = Polygon(poly)
            newply = affinity.translate(newply, xoff= -size[0]/2, yoff= -size[1]/2)
            print(self.parent.children[1].polygon)
            self.parent.children[1].reset(0)
            self.parent.children[1].polygon = newply
            self.parent.children[1].base_unit = newply
            #self.parent.children[1].get_new_recommendations()
            print(self.parent.children[1].polygon)  
            self.parent.children[1].tile_regular_polygon()

        else:
            pass
            

#main app class to build the root widget on program start
class DatoApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    Window.fullscreen = False
    DatoApp().run()
   
   
