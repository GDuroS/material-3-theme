from ._anvil_designer import MenuItemTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Functions import innerText_property, enabled_property, underline_property, italic_property, bold_property, font_size_property, color_property, theme_color_to_css, font_family_property

import anvil.designer

class MenuItem(MenuItemTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self._props = properties
    self.init_components(**properties)
    self.dom_nodes['anvil-m3-menuItem-container'].addEventListener("click", self.handle_click)

  """ Properties """
  """
  
  text = innerText_property('anvil-m3-menuItem-labelText')
  """
  @property
  def leading_icon(self):
    return self._leading_icon
    
  @leading_icon.setter
  def leading_icon(self, value):
    self._leading_icon = value
    self.dom_nodes["anvil-m3-menuItem-leadingIcon"].innerHTML = value or " "
    
  text = innerText_property('anvil-m3-menuItem-labelText')
  italic = italic_property('anvil-m3-menuItem-labelText')
  bold = bold_property('anvil-m3-menuItem-labelText')
  underline = underline_property('anvil-m3-menuItem-labelText')
  font_size = font_size_property('anvil-m3-menuItem-labelText')
  font_family = font_family_property('anvil-m3-menuItem-labelText', 'font_family')
  text_color = color_property('anvil-m3-menuItem-labelText', 'color', 'text_color')
  background = color_property('anvil-m3-menuItem-container', 'backgroundColor', 'background')


  @property
  def trailing_icon(self):
    return self._trailing_icon
  @trailing_icon.setter
  def trailing_icon(self, value):
    self._trailing_icon = value
    self.dom_nodes["anvil-m3-menuItem-trailingIcon"].innerText = value 
    
  @property
  def trailing_text(self):
    return self._trailing_text
  @trailing_text.setter
  def trailing_text(self, value):
    self._trailing_text = value
    self.dom_nodes["anvil-m3-menuItem-trailingText"].innerText = value 

  #TODO: rename this
  @property 
  def hide_leading_icon(self):
    return self._hide_leading_icon
  @hide_leading_icon.setter
  def hide_leading_icon(self, value):
    self._hide_leading_icon = value
    self.dom_nodes["anvil-m3-menuItem-leadingIcon"].classList.toggle("anvil-m3-menuItem-hideLeadingIcon", value)
  # anvil-m3-menuItem-hideLeadingIcon

  @property
  def enabled(self):
    return self._enabled
  @enabled.setter
  def enabled(self, value):
    self._enabled = value
    self.dom_nodes["anvil-m3-menuItem-container"].classList.toggle("anvil-m3-menuItem-disabled", not value)

  """ Functions """
  def handle_click(self, event):
    event.preventDefault() #TODO: make sure this doesn't prevent the menu from closing
    self.raise_event("click")

  def _anvil_get_interactions_(self):
    return [{
      "type": "whole_component",
      "title": "Edit text",
      "icon": "edit",
      "default": True,
      "callbacks": {
        "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-menuItem-labelText'])
      }
    }]