from ._anvil_designer import ButtonTemplate
from anvil import *
import anvil.js
from ...Functions import color_property, style_property, underline_property, italic_property, enabled_property, bold_property, visible_property

import anvil.designer

class Button(ButtonTemplate):
  def __init__(self, **properties):
    self._text = properties.get('text', '')
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dom_nodes['anvil-m3-button'].addEventListener("click", self.handle_click)

  def handle_click(self, e):
    self.raise_event("click", keys={"meta": e.metaKey, "shift": e.shiftKey, "ctrl": e.ctrlKey, "alt": e.altKey})

  def _anvil_get_design_info_(self, as_layout=False):
    di = super()._anvil_get_design_info_(as_layout)
    di['interactions'] = [{
      "type": "whole_component",
      "title": "Edit text",
      "icon": "edit",
      "default": True,
      "callbacks": {
        "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-button-text'])
      }
    }]
    return di

  @property
  def material_icon(self):
    return self._material_icon

  @material_icon.setter
  def material_icon(self, value):
    button = self.dom_nodes['anvil-m3-button']
    button_icon = self.dom_nodes['anvil-m3-button-icon']
    self._material_icon = value
    if value:
      button_icon.innerText = value
      button_icon.style.display = "block"
      button.classList.add('anvil-m3-icon-padding')
    else: 
      button_icon.innerText = ""
      button_icon.style.display = "none"
      button.classList.remove('anvil-m3-icon-padding')

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self, value):
    self._text = value
    self.dom_nodes['anvil-m3-button-text'].innerHTML = value or ""

  @property
  def appearance(self):
    return self._appearance

  @appearance.setter
  def appearance(self, value):
    self._appearance = value
    button = self.dom_nodes['anvil-m3-button']
    button.classList.remove('anvil-m3-elevated')
    button.classList.remove('anvil-m3-filled')
    button.classList.remove('anvil-m3-tonal')
    button.classList.remove('anvil-m3-outlined')
    if value:
      button.classList.add(f"anvil-m3-{value}")

  def form_show(self, **event_args):
      """This method is called when the HTML panel is shown on the screen"""
      if not self.text:
        if anvil.designer.in_designer:
          self.text = anvil.designer.get_design_name(self)
        else:
          self.text = "Button"

  text_color = color_property('anvil-m3-button-text', 'color')
  icon_color = color_property('anvil-m3-button-icon', 'color')
  font = style_property('anvil-m3-button-text', 'fontFamily')
  font_size = style_property('anvil-m3-button-text', 'fontSize')
  icon_size = style_property('anvil-m3-button-icon', 'fontSize')
  bold = bold_property('anvil-m3-button-text')
  italic = italic_property('anvil-m3-button-text')
  underline = underline_property('anvil-m3-button-text')
  align = style_property('anvil-m3-button-container', 'justifyContent')
  enabled = enabled_property('anvil-m3-button')
  visible = visible_property('anvil-m3-button-container', 'flex')
  border = style_property('anvil-m3-button-container', 'border')
  # TODO: Add background color property



  
