"""
Save dialog is displayed upon clicking the export button. 
Extends kivy's Popup widget
"""

from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window

import pandas as pd

class SaveDialog(Popup):
    def __init__(self,my_widget,**kwargs):  # my_widget is now the object where popup was called from (Tessellation Widget).
        super(SaveDialog,self).__init__(**kwargs)
        
        self.my_widget = my_widget
        self.data = self.my_widget.df # The pandas dataframe with metadata from TessellationWidget's export function
        self.raw_data = self.my_widget.raw_df # The pandas dataframe without metadata from TessellationWidget's export function

        self.title = 'Save Your Tiling'
        self.content = GridLayout(rows=4, cols=1)

        self.file_browser = FileChooserIconView(size_hint=(1,None), height=Window.size[1]/2)
        self.file_browser.path = 'Saved_Tilings\\'
        self.content.add_widget(self.file_browser)

        self.input_row = BoxLayout(orientation='horizontal', size_hint=(1,None), height=40)
        self.label = Label(text='Please enter name for output CSV file, do not include .csv extension.')
        self.input_box = TextInput(text='', multiline=False, font_size=24)
        self.input_row.add_widget(self.label)
        self.input_row.add_widget(self.input_box)
        self.content.add_widget(self.input_row)

        self.button_row = BoxLayout(orientation='horizontal', size_hint=(1,None), height=40)
        self.cancel_button = Button(text='Cancel')
        self.cancel_button.bind(on_press=self.cancel)
        self.button_row.add_widget(self.cancel_button)
        self.save_button = Button(text='Save')
        self.save_button.bind(on_press=self.save)
        self.button_row.add_widget(self.save_button)
        self.content.add_widget(self.button_row)

        self.error_message = Label(text='', color=(1,0,0,1), font_size=32)
        self.content.add_widget(self.error_message)

    # saves data to csv file
    def save(self,*args):
        if self.input_box.text != '':
            file_name = self.file_browser.path + '\\' + self.input_box.text + '.csv'
            self.data.to_csv(file_name, index=None)
            file_name = self.file_browser.path + '\\' + self.input_box.text + '_raw.csv'
            self.raw_data.to_csv(file_name, index=None)
            self.dismiss()
        else:
            self.error_message.text = 'PLEASE ENTER A NAME FOR YOUR FILE'

    # closes popup without saving anything
    def cancel(self,*args):
        self.dismiss()