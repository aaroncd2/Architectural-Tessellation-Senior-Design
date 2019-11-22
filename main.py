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
        self.recNum = 0;
        self.imageFile = None
        self.shapeCoords = None
        self.base_unit = None
        self.base_tiling = None
        self.root = tk.Tk()
        self.root.wm_title("DATO")
        self.fig = Figure(figsize=(5, 4), dpi=100)
        
        self.browsebutton = tk.Button(master=self.root, text="Select Image", command=self._browse_button)
        self.browsebutton.pack(side=tk.RIGHT)
       
        self.quitbutton = tk.Button(master=self.root, text="Quit", command=self._quit)
        self.quitbutton.pack(side=tk.LEFT)
        tk.mainloop()
    
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
        self.tilingbutton = tk.Button(master=self.root, text="base tiling", command=self._make_base_tiling)
        self.tilingbutton.pack(side=tk.RIGHT)
        self.quitbutton = tk.Button(master=self.root, text="Quit", command=self._quit)
        self.quitbutton.pack(side=tk.LEFT)
        
    #makes a base tiling (button handler)
    def _make_base_tiling(self):        
        te.tileRegularPolygon(self.base_unit, 5, 5, 1, self.subplot, self.canvas) 
        if self.reccbuttonExists == False:
            self.tilingbutton = tk.Button(master=self.root, text="Reccomendation", command=self._generateRecc)
            self.tilingbutton.pack(side=tk.RIGHT)
            self.reccbuttonExists = True
    #generates tiling reccomendations (button handler)
    def _generateRecc(self):
        if self.recNum > 2:
            self.recNum = 1
        else:
            self.recNum = self.recNum + 1
        rs.generateRecommendations(self.base_unit, 5, 5, self.subplot, self.canvas, self.recNum)
        
    #export to excel
    def export(self):
        base_tiling = self.base_tiling
        te.exportTiling(base_tiling)
        
    #quit button handler
    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
                            
if __name__ == "__main__":
    mainObj = Main()
    
    
    