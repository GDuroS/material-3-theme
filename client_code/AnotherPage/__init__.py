from ._anvil_designer import AnotherPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AnotherPage(AnotherPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.button_menu_1.add_component(Link(text="hello"))
  

    # Any code you write here will run before the form opens.
