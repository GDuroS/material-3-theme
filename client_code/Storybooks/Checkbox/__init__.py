from ._anvil_designer import CheckboxTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Checkbox(CheckboxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.checkbox_3.checked = None
    self.checkbox_5.checked = None

    # Any code you write here will run before the form opens.
