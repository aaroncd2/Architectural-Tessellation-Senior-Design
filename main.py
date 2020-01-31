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
from kivy.uix.boxlayout import BoxLayout
from shapely.geometry import Polygon, Point
from shapely import affinity
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
        try:
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
        except:
            pass
        
        
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


#main app class to build the root widget on program start
class DatoApp(App):
    def build(self):
       
        return RootWidget()

if __name__ == '__main__':
    DatoApp().run()
   
   
    