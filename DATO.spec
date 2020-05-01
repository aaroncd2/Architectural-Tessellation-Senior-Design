# -*- mode: python ; coding: utf-8 -*-

import os
from os.path import join


from kivy.tools.packaging import pyinstaller_hooks as hooks
from kivy import kivy_data_dir
from kivy_deps import sdl2, glew
import win32serviceutil
import win32service
import win32event
import win32timezone
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.graphics.vertex_instructions import Mesh

block_cipher = None
kivy_deps_all = hooks.get_deps_all()
kivy_factory_modules = hooks.get_factory_modules()


datas = [
    ('Image_Processing\\image_processing.py', 'Image_Processing'),
    ('Tessellation_Engine\\tessellation_engine.py', 'Tessellation_Engine'),
    ('Tessellation_Engine\\tessellation_utilities.py', 'Tessellation_Engine'),
    ('Tessellation_Engine\\save_dialog.py', 'Tessellation_Engine'),
    ('Tessellation_Engine\\help_dialog.py', 'Tessellation_Engine'),
    ('Tessellation_Engine\\custom_slider.py', 'Tessellation_Engine'),
    ('Shape_Identification\\tiling_rules.py', 'Shape_Identification'),
    ('Shape_Modeling\\shape_modeling.py', 'Shape_Modeling'),
    ('Shape_Modeling\\anomaly.py', 'Shape_Modeling'),
    ('Dato.kv', 'Dato'),
    ('imgpathfile.txt', 'imgpathfile'),
    ('csvpathfile.txt', 'csvpathfile')
]

# list of modules to exclude from analysis
excludes_a = ['Tkinter', '_tkinter', 'twisted', 'docutils', 'pygments']

# list of hiddenimports
hiddenimports = kivy_deps_all['hiddenimports'] + kivy_factory_modules + ['win32timezone']

# binary data
sdl2_bin_tocs = [Tree(p) for p in sdl2.dep_bins]
glew_bin_tocs = [Tree(p) for p in glew.dep_bins]
bin_tocs = sdl2_bin_tocs + glew_bin_tocs

# assets
kivy_assets_toc = Tree(kivy_data_dir, prefix=join('kivy_install', 'data'))

assets_toc = [kivy_assets_toc]

tocs = bin_tocs

a = Analysis(['main.py'],
             pathex=['C:\\Users\\pmoos\\Architectural-Tessellation-Senior-Design'],
             binaries=None,
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=hooks.runtime_hooks(),
             excludes=excludes_a,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='DATO',
          debug=True,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe, Tree('C:\\Users\\pmoos\\Architectural-Tessellation-Senior-Design'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *tocs,
               strip=False,
               upx=True,
               name='DATO')
