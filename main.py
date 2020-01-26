
from Image_Processing import image_processing as ip
from Shape_Modeling import shape_modeling as sm
from Tessellation_Engine import tessellation_engine as te
from Tessellation_Engine import recommendation_system as rs
import kivy 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
import numpy as np
import sys

#not sure yet best way to store these coords 
#for now they are global vars
coords = None
base_unit = None

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
        print('hello')
        global popup
        #open file dialog popup
        popup = Popup(title='Select File',
                      content=MyFileChooser(),
                      size_hint=(None, None), size=(400,400))
        popup.open()
        print('hello')
        
        
#gile chooser class
class MyFileChooser(FileChooserListView):
    #on picking of a file...
    def on_submit(*args):
        print(args[1][0])
        global fp
        #store file path
        fp = args[1][0]
        print(fp)
        #use file path to process as image in imageprocessing.py
        coords = ip.processImage(fp)
        base_unit = sm.shape_model(coords)
        print(coords)
        print(base_unit)
        popup.dismiss()
        
#canvas widget
#Note: lines not being drawn from generated coords
class CanvasWidget(Widget):
    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        with self.canvas:
            # add your instruction for main canvas here
            print('we here')
            Line(points=(coords))

#main app class to build the root widget on program start
class DatoApp(App):
    def build(self):
       
        return RootWidget()

if __name__ == '__main__':
    DatoApp().run()
   
   
    