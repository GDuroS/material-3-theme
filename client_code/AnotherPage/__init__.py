from ._anvil_designer import AnotherPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .._Components.Link import Link as M3_Link
from .._Components.Slider import Slider
from .._Components.NavigationLink import NavigationLink

class AnotherPage(AnotherPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    nav_link = NavigationLink(text="Test")
    self.layout.layout.add_to_nav_rail(nav_link)

  def text_field_3_pressed_enter(self, **event_args):
    """This method is called when the user presses enter in this component."""
    pass

 
    





