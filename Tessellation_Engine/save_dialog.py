from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import pandas as pd

class SaveDialog(Popup):
    def __init__(self,my_widget,**kwargs):  # my_widget is now the object where popup was called from.
        super(SaveDialog,self).__init__(**kwargs)
        
        self.my_widget = my_widget
        self.data = self.my_widget.df

        self.title = 'Save Your Tiling'
        self.content = GridLayout(rows=3, cols=2)

        self.label = Label(text='Please enter name for output CSV file, do not include .csv extension')
        self.input_box = TextInput(text='', multiline=False, font_size=32)

        self.save_button = Button(text='Save')
        self.save_button.bind(on_press=self.save)

        self.cancel_button = Button(text='Cancel')
        self.cancel_button.bind(on_press=self.cancel)

        self.error_message = Label(text='', color=(1,0,0,1), font_size=32)

        self.content.add_widget(self.label)
        self.content.add_widget(self.input_box)
        self.content.add_widget(self.save_button)
        self.content.add_widget(self.cancel_button)
        self.content.add_widget(self.error_message)

    # saves data to csv file in Saved_Tilings folder
    def save(self,*args):
        if self.input_box.text != '':
            file_name = 'Saved_Tilings\\' + self.input_box.text + '.csv'
            self.data.to_csv(file_name, index=None)
            self.dismiss()
        else:
            self.error_message.text = 'PLEASE ENTER A NAME FOR YOUR FILE'

    # closes popup without saving anything
    def cancel(self,*args):
        self.dismiss()