from ._anvil_designer import Form1Template
from anvil import *


class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def text_box_1_change(self, **event_args):
        """This method is called when the text in this component is edited."""
        value = event_args['sender'].text
        if isinstance(value, float) and value < 0:
            event_args['sender'].text = 
