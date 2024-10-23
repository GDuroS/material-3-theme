from ._anvil_designer import RadioGroupPanelTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RadioGroup:
  def __init__(self):
    super().__init__()
    self._buttons = []
    self._selected_button = None

  @property
  def buttons(self):
    return self._buttons

  def _add_button(self, button):
    self._buttons.append(button)

  def _remove_button(self, button):
    self._buttons.remove(button)

  def _handle_change(self):
    pass  # Override when used in a component
  
  @property
  def selected_button(self):
    for button in self._buttons:
      if button.selected:
        return button
    return None

  @selected_button.setter
  def selected_button(self, button):
    if button is None:
      # Deselect the currently selected button
      selected_button = self.selected_button
      if selected_button:
        selected_button.selected = False
    else:
      if button not in self._buttons:
        raise ValueError("RadioButton is not in this group")
      button.selected = True

  @property
  def selected_value(self):
    button = self.selected_button
    if button is None:
      return None
    else:
      return button.value

  @selected_value.setter
  def selected_value(self, requested_value):
    for button in self._buttons:
      if button.value == requested_value:
        self.selected_button = button
        return
    self.selected_button = None
  
  @classmethod
  def enclosing(cls, component):
    while component:
      component = component.parent
      if isinstance(component, cls):
        return component

    # No enclosing RadioGroup container, return a global one
    global global_radio_group
    return global_radio_group


global_radio_group = RadioGroup()


class RadioGroupPanel(RadioGroup, RadioGroupPanelTemplate):
  def __init__(self, **properties):
    super().__init__()
    self.init_components(**properties)

  def _handle_change(self):
    self.raise_event("change")
