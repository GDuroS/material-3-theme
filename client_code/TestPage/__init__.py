from ._anvil_designer import TestPageTemplate
from anvil import *
import plotly.graph_objects as go

class TestPage(TestPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.indeterminate_checkbox_1.checked = None
    self.indeterminate_checkbox_2.checked = None
    self.indeterminate_checkbox_3.checked = None
    self.indeterminate_checkbox_4.checked = None

    print(self.button_1.tag)

    # Any code you write here will run before the form opens.

  def radio_button_2_click(self, **event_args):
    pass

  def checkbox_2_click(self, **event_args):
    """This method is called when the component is checked or unchecked"""
    pass


  



    




