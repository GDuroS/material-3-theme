from ._anvil_designer import PeteTestPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class PeteTestPage(PeteTestPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def radio_group_panel_1_change(self, **event_args):
    """This method is called when the RadioButton selection changes"""
    print(self.radio_group_panel_1.selected_button.text)
    