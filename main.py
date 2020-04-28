from Image_Processing import image_processing as ip
from Shape_Modeling import shape_modeling as sm
from Tessellation_Engine import tessellation_engine as te
from Tessellation_Engine.tessellation_engine import TessellationWidget
from Tessellation_Engine.tessellation_engine import CanvasWidget
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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from shapely.geometry import Polygon, Point
from shapely import affinity
import matplotlib.pyplot as plt # for display
import math # for trig functions
import pandas as pd # for export
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from Shape_Identification import tiling_rules as tr
import csv
import numpy
import os
import sys
from kivy.core.window import Window
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.togglebutton import ToggleButton


from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


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
        self.main_menu = MainMenuWidget()
        self.add_widget(self.main_menu)
         #self.cb = Button(text='select a file')
         #bind and add file dialog button to root widget
         #
       #  #self.add_widget(self.cb)
        #fchooser = FileChooser()
        #self.add_widget(fchooser)
    #file dialog button callback
    def run_file_diag(self):
        self.remove_widget(self.main_menu)
        fchooser = FileChooser()
        self.add_widget(fchooser)
    def load_existing(self):
        self.remove_widget(self.main_menu)
        load_existing_chooser = LoadExistingChooser()
        self.add_widget(load_existing_chooser)
    def back_to_start(self):
        self.children[0].remove_widget(self.children[0].children[0])
        self.children[0].remove_widget(self.children[0].children[1])
        self.children[0].remove_widget(self.children[0].children[0])
        self.remove_widget(self.children[0])
        self.main_menu = MainMenuWidget()
        self.add_widget(self.main_menu)

class Tooltip(Label):
    pass

#widget for main menu 'splash screen'
class MainMenuWidget(GridLayout):
    def __init__(self, **kwargs):
        super(MainMenuWidget, self).__init__(**kwargs)
        
        self.cols=2
        self.rows=2
        self.add_widget(Label(text="Welcome To DATO"))
        menu_img = Image(source='Image_Processing/Images/flower_pic.jpg')
        self.add_widget(menu_img)
        self.cb = FileDiagButton()
        self.add_widget(self.cb)
        self.loadbtn = LoadExistingButton()
        self.add_widget(self.loadbtn)

class FileDiagButton(Button):
    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.text ="Choose New Image"
    def on_press(self, **kwargs):
        self.parent.parent.run_file_diag()


#class for tooltip btns
# class ToolBtn(Button):
#     def __init__(self, **kwargs):
       


class LoadExistingButton(Button):
    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.text = "Load Existing CSV"
    def on_press(self, **kwargs):
        self.parent.parent.load_existing()
    

#file dialog prompt to load csv file of existing polygon
class LoadExistingChooser(FileChooserListView):
    def getpath(self):
        with open('csvpathfile.txt', 'r') as f:
            data = f.read()
        if (data != None):
            return data
        else:
            return ""
        #print(data)
        #print(self.rootpath)
    def selected(self,filename,*args):
            if (filename == True):
                global fp
                global loaded_type
                #store file path
                fp = args[0][0]
                with open('csvpathfile.txt', 'w') as f:
                    data = fp
                    head, tail = os.path.split(data)
                    f.write(head)
                coo = []
                csvtessellcoords =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
                with open(fp) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0:
                            #print(f'Column names are {", ".join(row)}')
                            line_count += 1
                        else:
                            loaded_type = row[0]
                            if (row[1] != "None"):
                                coo.append(float(row[1]))
                                coo.append(float(row[2]))

                            csvtessellcoords[0].append(float(row[3]))
                            csvtessellcoords[0].append(float(row[4]))
                            csvtessellcoords[1].append(float(row[5]))
                            csvtessellcoords[1].append(float(row[6]))
                            csvtessellcoords[2].append(float(row[7]))
                            csvtessellcoords[2].append(float(row[8]))
                            csvtessellcoords[3].append(float(row[9]))
                            csvtessellcoords[3].append(float(row[10]))
                            csvtessellcoords[4].append(float(row[11]))
                            csvtessellcoords[4].append(float(row[12]))
                            csvtessellcoords[5].append(float(row[13]))
                            csvtessellcoords[5].append(float(row[14]))
                            csvtessellcoords[6].append(float(row[15]))
                            csvtessellcoords[6].append(float(row[16]))
                            csvtessellcoords[7].append(float(row[17]))
                            csvtessellcoords[7].append(float(row[18]))
                            csvtessellcoords[8].append(float(row[19]))
                            csvtessellcoords[8].append(float(row[20])) 
                            csvtessellcoords[9].append(float(row[21]))
                            csvtessellcoords[9].append(float(row[22])) 
                            csvtessellcoords[10].append(float(row[23]))
                            csvtessellcoords[10].append(float(row[24]))
                            csvtessellcoords[11].append(float(row[25]))
                            csvtessellcoords[11].append(float(row[26])) 
                            csvtessellcoords[12].append(float(row[27]))
                            csvtessellcoords[12].append(float(row[28]))
                            csvtessellcoords[13].append(float(row[29]))
                            csvtessellcoords[13].append(float(row[30]))
                            csvtessellcoords[14].append(float(row[31]))
                            csvtessellcoords[14].append(float(row[32]))
                            csvtessellcoords[15].append(float(row[33]))
                            csvtessellcoords[15].append(float(row[34]))
                            csvtessellcoords[16].append(float(row[35]))
                            csvtessellcoords[16].append(float(row[36]))
                            csvtessellcoords[17].append(float(row[37]))
                            csvtessellcoords[17].append(float(row[38]))
                            csvtessellcoords[18].append(float(row[39]))
                            csvtessellcoords[18].append(float(row[40]))
                            csvtessellcoords[19].append(float(row[41]))
                            csvtessellcoords[19].append(float(row[42]))
                            csvtessellcoords[20].append(float(row[43]))
                            csvtessellcoords[20].append(float(row[44]))
                            csvtessellcoords[21].append(float(row[45]))
                            csvtessellcoords[21].append(float(row[46])) 
                            csvtessellcoords[22].append(float(row[47]))
                            csvtessellcoords[22].append(float(row[48])) 
                            csvtessellcoords[23].append(float(row[49]))
                            csvtessellcoords[23].append(float(row[50]))
                            csvtessellcoords[24].append(float(row[51]))
                            csvtessellcoords[24].append(float(row[52])) 
                            line_count += 1
                            #print(f'Processed {line_count} lines.')
                global f_coords
                points = list(zip(coo[::2],coo[1::2]))
                print(points)
                print(coo)
                poly = Polygon(points)
                f_coords = poly.exterior.coords
                #f_coords = sm.shape_model(coo)
                #print(f_coords)
                global loaded_csv_tessel
                #global is_load_csv
                global is_load_csv
                loaded_csv_tessel = csvtessellcoords
                #print(loaded_csv_tessel[0][0])
                is_load_csv = True
                b_grid = BoxGrid()
                self.parent.add_widget(b_grid)
                self.parent.remove_widget(self)




#gile chooser class
class FileChooser(FileChooserListView):
    def getpath(self):
        with open('imgpathfile.txt', 'r') as f:
            data = f.read()
        if (data != None):
            return data
        else:
            return ""
        #print(data)
        #print(self.rootpath)
    def selected(self,filename,*args):
            if (filename == True):

                global fp
                #store file path
                fp = args[0][0]
                with open('imgpathfile.txt', 'w') as f:
                    data = fp
                    head, tail = os.path.split(data)
                    f.write(head)

                #print(fp)
                #use file path to process as image in imageprocessing.py
                global f_coords
                global is_load_csv
                is_load_csv = False
                coo = ip.processImage(fp)
                #print(coo)
                f_coords = sm.shape_model(coo)
                #print(f_coords)
                b_grid = BoxGrid()
                self.parent.add_widget(b_grid)
                
                self.parent.remove_widget(self)
            else:
                self.ids.image.source = filename[0]


class ReccomendationButton(Button):
    def __init__(self, **kwargs):
        self.tooltip = Tooltip()
        self.tooltext=''
        self.tooltip.text = self.tooltext
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(Button, self).__init__(**kwargs)
        #self.size = 175, 145

        self.background_color = [.3, .3, 0.3, .75]
        self.pressed=False
        self.index = None
        if (the_poly != None):
            with self.canvas.after:
                Line(points = the_poly)
            with self.canvas.before:
                Line(points = the_poly)
    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        self.tooltip.pos = pos
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            Clock.schedule_once(self.display_tooltip,1)
    def close_tooltip(self,*args):
        Window.remove_widget(self.tooltip)
    def display_tooltip(self,*args):
        Window.add_widget(self.tooltip)

    def on_press(self, **kwargs):
        #print(self.index)
        #print(self.parent.parent.parent.children[1])
        #self.parent.parent.parent.children
        self.pressed=True
        self.parent.parent.parent.children[1].draw_recommendation(self.index)
        #self.button_normal =''
        self.background_color = [.3, .7, .4, .75]
        self.parent.parent.press_helper_func(self)

class ReccomendationButtons(FloatLayout):
    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        self.size_hint= None, None
        #self.saved_states = []

    def press_helper_func(self,eleref):
        #print(eleref)
        for btn in self.reccrows.children:
            if btn != eleref:
                print(self.btns_info[btn.index])
                tempsaveinfo = self.btns_info[btn.index]
                if len(tempsaveinfo) != 5:
                    btn.background_color = [.3, .3, 0.3, .75]
                else:
                    btn.background_color =[1, .3, .4, .85]
        #print(self.reccrows.children)

    def setup_btns(self, is_resize):


        #print(self.parent.main_shape_info)
        self.btns_info = self.parent.main_shape_info
        self.numreccs = len(self.btns_info)
        #print("shape info")
        #print(self.btns_info)
        #print(self.numreccs)
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
        u = self.numreccs
        for k in range(0, self.numreccs):

            u = u - 1
            if (k != 0):
                the_poly = self.make_positive(self.btns_info[k][0])
                btn_height = (Window.size[1] / self.numreccs)
                yoff = (Yoff ) + btn_height* k
                the_poly = affinity.translate(the_poly, xoff= xoff, yoff= yoff)
                if xscale > yscale:
                    the_poly = affinity.scale(the_poly, xfact= xscale, yfact= yscale)
                else:
                    the_poly = affinity.scale(the_poly, xfact= xscale, yfact= xscale)
                the_poly = self.shapely_to_kivy(the_poly)
            else:
                the_poly = None
            temp = ReccomendationButton()
            if str(self.btns_info[u][1]) == "regular":
                temp.tooltip.text = "Freeform"
            else:
                temp.tooltip.text = str(self.btns_info[u][1])
            the_poly = None

            temp.index = u

            colorcheck = self.btns_info[u]
            if len(colorcheck) == 5:
                if colorcheck[4] == "s":
                    temp.background_normal= ''
                    temp.background_color =[1, .3, .4, .85]
            self.reccrows.add_widget(temp)
            #temp.add_widget(Label(text="testt",valign='bottom'), index=0)
        self.add_widget(self.reccrows, index=1)
        # # for k in range(0, self.numreccs):
        #      label = Label(text="hello")
        #      self.add_widget(label)



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
        if is_load_csv == True:
            print("changing self.polygons")
            self.children[0].polygons = loaded_csv_tessel
            print("changing type of tessel")
            self.children[0].type = loaded_type
        tessel.display_initial_tiling(is_load_csv)
        tessel.change_rec_label_text()
        self.main_shape_info = tessel.shape_info
        self.btn = ReccomendationButtons()
        self.add_widget(self.btn)
        if (self.main_shape_info != None and len(self.main_shape_info) > 1):
            self.btn.setup_btns(False)

class Tooltip(Label):
    pass

class ToolBtn(Button):
    def __init__(self,**kwargs):
        self.tooltip = Tooltip()
        self.tooltext=''
        self.tooltip.text = self.tooltext
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(Button, self).__init__(**kwargs)
    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        self.tooltip.pos = pos
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            Clock.schedule_once(self.display_tooltip,1)
    def close_tooltip(self,*args):
        Window.remove_widget(self.tooltip)
    def display_tooltip(self,*args):
        Window.add_widget(self.tooltip)

#layout for baseunit and functions
class CustomLayout(BoxLayout):
    def __init__(self, **kwargs):

        super(CustomLayout, self).__init__(**kwargs)

        Window.bind(on_key_down=self.key_action) #Binds Keyboard for key detection
        Window.bind(on_resize=self.on_window_resize)
        self.saved_states= []
        self.back_button = ToolBtn(text = 'Back',
                                          background_color = (1,1,1,1),
                                          font_size = '12dp',
                                          size_hint = (.3,.07),
                                          pos_hint = {'bottom': 0.3})
        self.back_button.tooltip.text ="Go back to main menu"
        # Add change color button
        self.color_picker_button = Button(text = 'Choose Color',
                                          font_size = '12dp',
                                          background_color = (1,1,1,1),
                                          size_hint = (.35,.07),
                                          pos_hint = {'bottom': 0.3})
        self.color_picker_button.tooltip.text ="Find a color that suits your tessellation"

        #Add background color button
        self.background_color_picker_button = Button(text = 'Choose Background',
                                                     font_size = '12dp',
                                                     background_color = (1,1,1,1),
                                                     size_hint = (.45,.07),
                                                     pos_hint = {'bottom': 0.3})
        self.background_color_picker_button.tooltip.text = "Choose color for tessellation background"
        self.add_widget(self.back_button)
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.color_picker_button)
        self.color_picker_button.bind(on_press=self.change_color)
        self.add_widget(self.background_color_picker_button)
        self.color_picker_button.bind(on_press=self.change_color_background)

        #add help button for keyboard commands
        def open_help(self, *args):
            self.help.open()

        self.help_label = Label(text = " Click on edge/vertex to select\n To delete edge/vertex: Press 'delete'/'backspace\n To add a vertex: Press 'a'\n To reset: Press 'r'",
                                font_size = '20sp')
        self.help = Popup(title = 'Help',
                           content = self.help_label,
                           pos_hint={'center_x': .5, 'center_y': .5},
                           size_hint = (.4, .4),
                           auto_dismiss = True)
        self.help_button = ToolBtn(text = '?',
                                   size_hint = (.1, .04),
                                   background_color = (1,1,1,.3),
                                   pos_hint = {'top':1})
        self.help_button.tooltip.text = "Click for controls help and descriptions"
        self.help_button.bind(on_press = open_help)
        self.add_widget(self.help_button)

        self.shape = InstructionGroup()
        self.col = [1,1,1,1]
        self.col_background = [0,0,0,1]
        self.fill = [0,0,1,1]

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
        self.xscale = sizeX * .25 / xdistnace
        self.yscale = sizeY * .25 / ydistance
        center = (poly.centroid.coords[0])
        xoff = ((sizeX/5) + (Window.size[0]*.14)) - center[0]
        yoff = (sizeY/4) - center[1]

        poly = affinity.translate(poly, xoff= xoff, yoff= yoff)
        if self.xscale > self.yscale:
            poly = affinity.scale(poly, xfact= self.yscale, yfact= self.yscale)
        else:
            poly = affinity.scale(poly, xfact= self.xscale, yfact= self.xscale)
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

    def config_from_shapely_poly(self, shapely_poly_saved):
        poly = shapely_poly_saved
        self.c_coords = poly.exterior.coords
        sizeX = Window.size[0]
        sizeY = Window.size[1]
        xdistnace = (poly.bounds[2] - poly.bounds[0])
        ydistance = (poly.bounds[3] - poly.bounds[1])
        self.xscale = sizeX * .25 / xdistnace
        self.yscale = sizeY * .25 / ydistance
        center = (poly.centroid.coords[0])
        xoff = ((sizeX/5) + (Window.size[0]*.14)) - center[0]
        yoff = (sizeY/4) - center[1]

        poly = affinity.translate(poly, xoff= xoff, yoff= yoff)
        if self.xscale > self.yscale:
            poly = affinity.scale(poly, xfact= self.yscale, yfact= self.yscale)
        else:
            poly = affinity.scale(poly, xfact= self.xscale, yfact= self.xscale)
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
        #print(key_pressed)

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
            poly = []
            i = 0
            for xy in self.canvas_nodes:
                poly.append(self.canvas_nodes[i].pos)
                i = i + 1

            newply = Polygon(poly)
            newply = affinity.translate(newply, xoff= -size[0]/2.95, yoff= -size[1]/4)
            if self.xscale > self.yscale:
                newply = affinity.scale(newply, xfact= 1/self.yscale, yfact= 1/self.yscale)
            else:
                newply = affinity.scale(newply, xfact= 1/self.xscale, yfact= 1/self.xscale)
            self.parent.children[1].original_base_unit = newply
            self.parent.children[1].polygon = newply
            self.parent.children[1].reset(0)
            #self.parent.children[1].tile_regular_polygon()

            if (self.parent.children[0] != None):
                    new_shape_info = tr.identify_shape(newply)
                    self.parent.main_shape_info = new_shape_info
                    self.parent.children[1].shape_info = new_shape_info
                    for state in self.saved_states:
                        new_shape_info.append(state)
                    self.parent.remove_widget(self.parent.children[0])
                    btns = ReccomendationButtons()
                    self.parent.add_widget(btns)
                    if (new_shape_info != None and len(new_shape_info) >= 1):
                        btns.setup_btns(False)

        #Add when pressing a
        elif key_pressed[2] == 4 and self.pressed:
            try:
                self.canvas.children.remove(self.highlight)
                mid = midpoint(self.canvas_edge[self.index].points)
                #print(self.highlight.points)
                self.c_coords.insert((self.index+1)%len(self.canvas_nodes), tuple(mid))
                self.draw()

            except:
                print(' Point selected')
            self.pressed = False

            poly = []
            i = 0
            for xy in self.canvas_nodes:
                poly.append(self.canvas_nodes[i].pos)
                i = i + 1

            newply = Polygon(poly)
            newply = affinity.translate(newply, xoff= -size[0]/2.95, yoff= -size[1]/4)
            if self.xscale > self.yscale:
                newply = affinity.scale(newply, xfact= 1/self.yscale, yfact= 1/self.yscale)
            else:
                newply = affinity.scale(newply, xfact= 1/self.xscale, yfact= 1/self.xscale)
            self.parent.children[1].original_base_unit = newply
            self.parent.children[1].polygon = newply
            self.parent.children[1].reset(0)
            #self.parent.children[1].tile_regular_polygon()

            if (self.parent.children[0] != None):
                    new_shape_info = tr.identify_shape(newply)
                    self.parent.main_shape_info = new_shape_info
                    self.parent.children[1].shape_info = new_shape_info
                    for state in self.saved_states:
                        new_shape_info.append(state)
                    self.parent.remove_widget(self.parent.children[0])
                    btns = ReccomendationButtons()
                    self.parent.add_widget(btns)
                    if (new_shape_info != None and len(new_shape_info) >= 1):
                        btns.setup_btns(False)

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
            newply = affinity.translate(newply, xoff= -size[0]/2.95, yoff= -size[1]/4)
            if self.xscale > self.yscale:
                newply = affinity.scale(newply, xfact= 1/self.yscale, yfact= 1/self.yscale)
            else:
                newply = affinity.scale(newply, xfact= 1/self.xscale, yfact= 1/self.xscale)
            self.parent.children[1].original_base_unit = newply
            self.parent.children[1].polygon = newply
            self.parent.children[1].reset(0)
            #self.parent.children[1].tile_regular_polygon()

            if (self.parent.children[0] != None):
                    new_shape_info = tr.identify_shape(newply)
                    self.parent.main_shape_info = new_shape_info
                    self.parent.children[1].shape_info = new_shape_info
                    for state in self.saved_states:
                        new_shape_info.append(state)
                    self.parent.remove_widget(self.parent.children[0])
                    btns = ReccomendationButtons()
                    self.parent.add_widget(btns)
                    if (new_shape_info != None and len(new_shape_info) >= 1):
                        btns.setup_btns(False)

    def on_window_resize(self, window, width, height):
        self.canvas.remove_group('shape')
        self.canvas.remove(self.shape)
        self.configCoords()

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
        self.parent.remove_widget(self.parent.children[0])
        btns = ReccomendationButtons()
        self.parent.add_widget(btns)
        if (self.parent.main_shape_info != None and len(self.parent.main_shape_info) >= 1):
            btns.setup_btns(False)

    def draw(self):
        r,g,b,a = self.col[0], self.col[1], self.col[2], self.col[3]
        self.canvas.add(Color(r,g,b,a))
        self.canvas.remove_group('shape')
        self.canvas.remove(self.shape)
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
                group = 'shape',
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
                close = False,
                group = 'shape'
                )
            i = i + 1

    def on_touch_down(self, touch):
        i = 0
        if self.color_picker_button.collide_point(*touch.pos):
            self.change_color()
        if self.back_button.collide_point(*touch.pos):
            self.go_back()
        if self.background_color_picker_button.collide_point(*touch.pos):
            self.change_color_background()
        if self.help_button.collide_point(*touch.pos):
            self.help.open()
        else:
            for lines in self.canvas_edge:
                x,y = self.canvas_edge[i].points[0], self.canvas_edge[i].points[1]
                a = [x,y]
                x,y = self.canvas_edge[i].points[2], self.canvas_edge[i].points[3]
                b = [x,y]
                c = list(touch.pos)
                if angle(a,b,c) and not self.pressed:
                    points = [a,b]

                    self.shape.add(Color(1,0,0, .5))
                    self.canvas.add(self.shape)
                    self.highlight = Line(
                        points = points,
                        width = 5,
                        group = 'shape'
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
                        self.shape.add(Color(1,0,0, .5))
                        self.canvas.add(self.shape)
                        self.highlight = Ellipse(
                            size = self.nodesize,
                            pos =  self.canvas_nodes[key].pos,
                            group = 'shape'
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
            self.canvas.remove_group('shape')
            self.canvas.remove(self.shape)
            r,g,b,a = self.col[0], self.col[1], self.col[2], self.col[3]
            self.canvas.add(Color(r,g,b,a))
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
            newply = affinity.translate(newply, xoff= -size[0]/2.95, yoff= -size[1]/4)
            if self.xscale > self.yscale:
                newply = affinity.scale(newply, xfact= 1/self.yscale, yfact= 1/self.yscale)
            else:
                newply = affinity.scale(newply, xfact= 1/self.xscale, yfact= 1/self.xscale)
            #123 references to tessellation engine objects
            #self.parent.children[1].draw_polygons()
            self.parent.children[1].original_base_unit = newply
            self.parent.children[1].polygon = newply
            self.parent.children[1].reset(0)

        else:
            pass

    def on_touch_up(self, touch):
        temp = []
        i = 0
        for i in range(len(self.c_coords)):
            temp.append(self.canvas_nodes[i].pos)
            i = i + 1
        self.c_coords = temp
        print(self.c_coords)

        if touch.grab_current is self:
            touch.ungrab(self)
            poly = []
            i = 0
            for xy in self.canvas_nodes:
                poly.append(self.canvas_nodes[i].pos)
                i = i + 1

            #print(poly)
            newply = Polygon(poly)
            newply = affinity.translate(newply, xoff= -size[0]/2.95, yoff= -size[1]/4)
            if self.xscale > self.yscale:
                newply = affinity.scale(newply, xfact= 1/self.yscale, yfact= 1/self.yscale)
            else:
                newply = affinity.scale(newply, xfact= 1/self.xscale, yfact= 1/self.xscale)
            #print(self.parent.children[1].polygon)
            self.parent.children[1].reset(0)
            self.parent.children[1].polygon = newply
            self.parent.children[1].base_unit = newply
            #self.parent.children[1].get_new_recommendations()
            #print(self.parent.children[1].polygon)
            self.parent.children[1].tile_regular_polygon()
            #print("parker")
            #print(self.parent.children[0])
            if (self.parent.children[0] != None):
                #self.saved_states = self.parent.saved_states
                #print("fetching any saved states")
                #print(self.saved_states)
                #print("got saved states ...")
                new_shape_info = tr.identify_shape(newply)
                self.parent.main_shape_info = new_shape_info
                for state in self.saved_states:
                    new_shape_info.append(state)
                self.parent.children[1].shape_info = new_shape_info
                self.parent.remove_widget(self.parent.children[0])
                btns = ReccomendationButtons()
                self.parent.add_widget(btns)
                if (new_shape_info != None and len(new_shape_info) >= 1):
                    btns.setup_btns(False)



            # self.main_shape_info = tessel.shape_info
        #btn = ReccomendationButtons()
        #self.add_widget(btn)
        #if (self.main_shape_info != None and len(self.main_shape_info) > 1):
         #   btn.setup_btns()

        else:
            pass
    def add_saved_state(self, polygon, typet, tf, polygons):
        #print('adding')
        self.saved_states.append((polygon,typet, tf, polygons,"s"))
        #print('added')
        #print(self.saved_states)
        state = (polygon,typet, tf, polygons, "s")
        self.parent.main_shape_info.append(state)
        self.parent.remove_widget(self.parent.children[0])
        btns = ReccomendationButtons()
        self.parent.add_widget(btns)
        if (self.parent.main_shape_info != None and len(self.parent.main_shape_info) >= 1):
            btns.setup_btns(False)

    #handler for back button
    def go_back(self, *args):
        #print(self.parent.parent)
        self.parent.parent.back_to_start()

    def change_color(self,*args):

        r,g,b,a = self.col[0], self.col[1], self.col[2], self.col[3]
        self.picker = ColorPicker(pos_hint={'center_x': .5, 'center_y': .5},
                                color = [r,g,b,a],
                                size_hint = (1,1))

        self.picker.add_widget(Button(text = 'Select',
                                  pos_hint = {'center_x': .76, 'y': -.02},
                                  size_hint = (.08, .08),
                                #   size = (100, 35),
                                  on_press = self.selected))

        self.edge_toggle = ToggleButton(text = 'Edge',
                                       pos_hint = {'center_x': .55, 'y': -.02},
                                       size_hint = (.08, .08),
                                    #    size = (100, 35),
                                       group = 'color',
                                       state = 'down')
        self.edge_toggle.bind(on_press = self.pressed_toggle_edge)
        self.picker.add_widget(self.edge_toggle)

        self.fill_toggle = ToggleButton(text = 'Fill',
                                            pos_hint = {'center_x': .63, 'y': -.02},
                                            size_hint = (.08, .08),
                                            # size = (100, 35),
                                            group = 'color')
        self.fill_toggle.bind(on_press = self.pressed_toggle_fill)
        self.picker.add_widget(self.fill_toggle)

        self.match_toggle = ToggleButton(text = 'Match',
                                            pos_hint = {'x': .8, 'y': -.02},
                                            size_hint = (.08, .08),
                                            # size = (100, 35),
                                            group = 'match')
        self.picker.add_widget(self.match_toggle)


        self.ColPop = Popup(title = "Choose Color",
                        size_hint = (.50, .50),
                        content = self.picker,
                        # size = (1500, 750),
                        auto_dismiss = True)

        self.ColPop.open()

    def change_color_background(self,*args):

        r,g,b,a = self.col_background[0], self.col_background[1], self.col_background[2], self.col_background[3]
        self.picker_background = ColorPicker(pos_hint={'center_x': .5, 'center_y': .5},
                                color = [r,g,b,a],
                                size_hint = (1, 1))

        self.picker_background.add_widget(Button(text = 'Select',
                                  pos_hint = {'center_x': .76, 'y': -.02},
                                  size_hint = (.08, .08),
                                #   size = (100, 35),
                                  on_press = self.background_selected))
        self.ColPop_background = Popup(title = "Choose Background",
                        size_hint = (.5, .5),
                        content = self.picker_background,
                        # size = (1500, 750),
                        auto_dismiss = True)

        self.ColPop_background.open()

    def selected(self, *args):
        self.ColPop.dismiss()

        if self.match_toggle.state == 'down':
            self.col = self.picker.color
            self.fill = self.col
            r,g,b,a = self.col[0], self.col[1], self.col[2], self.col[3]
            self.parent.children[1].stroke_color = [r,g,b,a]
            self.parent.children[1].fill_color = [r,g,b,a]
        elif self.edge_toggle.state == 'down':
            self.col = self.picker.color
            r,g,b,a = self.col[0], self.col[1], self.col[2], self.col[3]
            self.parent.children[1].stroke_color = [r,g,b,a]
        elif self.fill_toggle.state == 'down':
            self.fill = self.picker.color
            r,g,b,a = self.fill[0], self.fill[1], self.fill[2], self.fill[3]
            self.parent.children[1].fill_color = [r,g,b,a]
        elif self.fill_toggle != 'down' and self.edge_toggle != 'down':
            self.col = self.picker.color
            r,g,b,a = self.col[0], self.col[1], self.col[2], self.col[3]
            self.parent.children[1].stroke_color = [r,g,b,a]


        self.parent.children[1].draw_polygons()
        self.draw()

    def background_selected(self, *args):
        self.ColPop_background.dismiss()
        self.col_background = self.picker_background.color
        r,g,b,a = self.col_background[0], self.col_background[1], self.col_background[2], self.col_background[3]
        Window.clearcolor = (r, g, b, a)

    def pressed_toggle_edge(self, *args):
        self.picker.color = self.col

    def pressed_toggle_fill(self, *args):
        self.picker.color = self.fill

#main app class to build the root widget on program start
class DatoApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    Window.fullscreen = False
    DatoApp().run()


