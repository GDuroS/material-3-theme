from ._anvil_designer import Form1Template
from anvil import *


class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.dropdown_menu_1.selected_value = self.dropdown_menu_1.items[0]
        self.dropdown_menu_2.selected_value = self.dropdown_menu_2.items[0]
        self.dropdown_menu_3.selected_value = self.dropdown_menu_3.items[0]

        # Any code you write here will run before the form opens.

    def toggle_icon_button_1_click(self, **event_args):
        self.text_area_1.read_only = self.toggle_icon_button_1.selected
        self.text_box_1.read_only = self.toggle_icon_button_1.selected
        self.dropdown_menu_1.read_only = self.toggle_icon_button_1.selected
