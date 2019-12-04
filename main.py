import tkinter as tk
from tkinter import filedialog
from Image_Processing import image_processing as ip
from Shape_Modeling import shape_modeling as sm
from Tessellation_Engine import tessellation_engine as te
from Tessellation_Engine import recommendation_system as rs
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import sys
class Main:
    #starts program, creates figure and subplot
    def __init__(self):
        self.reccbuttonExists = False
        self.reccbuttonPressed = False
        self.recNum = 0
        self.imageFile = None
        self.shapeCoords = None
        self.base_unit = None
        self.base_tiling = None
        self.polygons = None
        self.tesselbtns_exist = False
        self.root = tk.Tk()
        self.root.wm_title("DATO")
        self.fig = Figure(figsize=(5, 4), dpi=100)
        
        self.browsebutton = tk.Button(master=self.root, text="Select Image", command=self._browse_button)
        self.browsebutton.pack(side=tk.RIGHT)
       
        self.quitbutton = tk.Button(master=self.root, text="Quit", command=self._quit)
        self.quitbutton.pack(side=tk.LEFT)
        tk.mainloop()
    
    def _new_image(self):
        self._browse_button()
        self.basebutton.pack_forget()
        if self.tesselbtns_exist:
            self.exportbutton.pack_forget()
            self.verticalbutton.pack_forget()
            self.horizontalbutton.pack_forget()
            self.rotationscale.pack_forget()
            self.tesselbtns_exist = False
        self.subplot.clear()
        self.shapeCoords = ip.processImage(self.root.filename)
        self.base_unit = sm.shape_model(self.shapeCoords)
        x,y = self.base_unit.exterior.xy
        self.subplot.plot(x,y)
        self.canvas.draw()
    
    
    #browse for pictures
    def _browse_button(self):
        self.browsebutton.pack_forget()
        global folder_path
        self.root.filename = filedialog.askopenfilename(initialdir = "/Image_Processing/Images/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png")))
        print(self.root.filename)
        self.basebutton = tk.Button(master=self.root, text="Make Base Unit", command=self._make_base_unit)
        self.basebutton.pack(side=tk.BOTTOM)
    
    #processes image using cv
    def _process_image(self):
        #imageDirectory = "Image_Processing/Images/"
        #coords = ip.processImage(imageDirectory + sys.argv[1])
        self.shapeCoords = ip.processImage(self.root.filename)
        
    
    def _make_base_unit(self):
        self.quitbutton.pack_forget()
        self.basebutton.pack_forget()
        self._process_image()
        self.base_unit = sm.shape_model(self.shapeCoords)
        x,y = self.base_unit.exterior.xy        
        self.subplot = self.fig.add_subplot(111)
        self.subplot.plot(x,y)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.tilingbutton = tk.Button(master=self.root, text="Base Tiling", command=self._make_base_tiling)
        self.tilingbutton.pack(side=tk.RIGHT)
        self.quitbutton = tk.Button(master=self.root, text="Quit", command=self._quit)
        self.quitbutton.pack(side=tk.LEFT)
        self.newimgbtn = tk.Button(master=self.root, text="New Base Unit", command=self._new_image)
        self.newimgbtn.pack(side=tk.LEFT)
        
    #makes a base tiling (button handler)
    def _make_base_tiling(self):        
        self.polygons = te.tileRegularPolygon(self.base_unit, 5, 5, 1, self.subplot, self.canvas) 
        
        #self.tilingbutton = tk.Button(master=self.root, text="Reccomendation", command=self._generateRecc)
        #self.tilingbutton.pack(side=tk.RIGHT)
        self.verticalbutton = tk.Button(master=self.root, text="Flip Vertical", command=self._flipVertical)
        self.verticalbutton.pack(side=tk.RIGHT)
        self.horizontalbutton = tk.Button(master=self.root, text="Flip Horizontal", command=self._flipHorizontal)
        self.horizontalbutton.pack(side=tk.RIGHT)
        self.rotationscale = tk.Scale(orient='horizontal', from_=0, to=360, label='Rotate', command=self._rotateTiling)
        self.rotationscale.pack(side=tk.RIGHT)
        self.exportbutton = tk.Button(master=self.root, text="Export", command=self._export)
        self.exportbutton.pack(side=tk.LEFT)
        self.reccbuttonExists = True
        self.tesselbtns_exist = True

    #generates tiling reccomendations (button handler)
    def _generateRecc(self):
        if self.recNum > 2:
            self.recNum = 1
        else:
            self.recNum = self.recNum + 1
        rs.generateRecommendations(self.base_unit, 5, 5, self.subplot, self.canvas, self.recNum)

    # flips alternating rows of polygons vertically
    def _flipVertical(self):
        self.polygons = te.tileRegularPolygon(self.base_unit, 5, 5, 2, self.subplot, self.canvas)
        self.rotationscale.set(0)

    # flips alternating rows of polygons horizontally 
    def _flipHorizontal(self):
        self.rotationscale.set(0)
        self.polygons = te.tileRegularPolygon(self.base_unit, 5, 5, 3, self.subplot, self.canvas)    

    # rotates each polygon by the value in the rotation slider
    def _rotateTiling(self, scale):
        polygon = te.rotatePolygon(self.base_unit, self.rotationscale.get())
        self.polygons = te.tileRegularPolygon(polygon, 5, 5, 1, self.subplot, self.canvas)

    #export to excel
    def _export(self):
        te.exportTiling(self.polygons)
        
    #quit button handler
    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
                            
if __name__ == "__main__":
    mainObj = Main()
    
    
    