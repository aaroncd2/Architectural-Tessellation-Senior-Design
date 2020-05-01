"""
HelpDialog is a class that extends kivy's Popup class.
It displays information about the controls of the Tessellation Engine
"""

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class HelpDialog(Popup):
    def __init__(self,**kwargs):
        super(HelpDialog,self).__init__(**kwargs)

        self.title = 'Tessellation Engine Controls'

        
        layout = BoxLayout(orientation='vertical')
        title_label = Label(text='Tessellation Engine Controls', font_size='24dp')
        layout.add_widget(title_label)
        save_button_label = Label(text='Save State: Saves the current state of tiling. Adds button to recommendations on left side of screen to quickly return to saved state.', font_size = '14dp')
        layout.add_widget(save_button_label)
        export_button_label = Label(text='Export: Exports two CSV files with current status of tiling. The raw CSV just holds the coordinates of the tiling for use in other programs.\nThe other holds metadata to reload the tiling inside DATO.', font_size = '14dp')
        layout.add_widget(export_button_label)
        undo_button_label = Label(text='Undo: Undoes last performed action.', font_size = '14dp')
        layout.add_widget(undo_button_label)
        reset_button_label = Label(text='Reset: Resets the tiling to a freeform tiling using the editable base unit on the left side of the screen', font_size = '14dp')
        layout.add_widget(reset_button_label)
        alt_cols_label = Label(text='Alternate Columns: Flips each polygon in every other column across their center horizontally', font_size = '14dp')
        layout.add_widget(alt_cols_label)
        alt_rows_label = Label(text='Alternate Rows: Flips each polygon in every other row across their center vertically', font_size = '14dp')
        layout.add_widget(alt_rows_label)
        vflip_label = Label(text='Flip Vertical: Flips each polygon across its center vertically', font_size = '14dp')
        layout.add_widget(vflip_label)
        hflip_label = Label(text='Flip Horizontal: Flips each polygon across its center horizontally', font_size = '14dp')
        layout.add_widget(hflip_label)
        toggle_freeform_label = Label(text='Toggle Freeform: Switches the tiling type to freeform if tiling a recommendation as a parallelogram or hexagon.\nClicking this button again will switch back to the previous tiling mode.', font_size = '14dp')
        layout.add_widget(toggle_freeform_label)

        close_button = Button(text='Close', on_press=self.close)
        layout.add_widget(close_button)
        self.add_widget(layout)

    # closes popup 
    def close(self,*args):
        self.dismiss()