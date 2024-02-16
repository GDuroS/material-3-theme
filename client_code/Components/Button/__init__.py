from ._anvil_designer import ButtonTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from ...Functions import color_property, role_property, tooltip_property, custom_bold_property, font_family_property, font_size_property, style_property, property_with_callback, underline_property, bold_property, italic_property, margin_property 
from anvil import HtmlTemplate
import anvil.designer

class Button(ButtonTemplate):
  def __init__(self, **properties):
    self._props = properties
    self._text = properties.get('text', '')
    self._tooltip_node = None
    self.init_components(**properties)
    
    self._handle_click = self._handle_click
    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

  def _on_mount(self, **event_args):
    self.dom_nodes['anvil-m3-button'].addEventListener("click", self._handle_click)
  def _on_cleanup(self, **event_args):
    self.dom_nodes['anvil-m3-button'].removeEventListener("click", self._handle_click)

  def _set_align(self, value):
    self.dom_nodes['anvil-m3-button'].classList.toggle('full-width', False)
    if value is 'full':
      self.dom_nodes['anvil-m3-button'].classList.toggle('full-width', True)
    else:
      self.dom_nodes['anvil-m3-button-component'].style.justifyContent = value
      
  align = property_with_callback('align', _set_align)
  visible = HtmlTemplate.visible
  role = role_property('anvil-m3-button')

  def _handle_click(self, event):
    event.preventDefault()
    if self.enabled:
      self.raise_event("click")

  def _anvil_get_interactions_(self):
    return [{
      "type": "whole_component",
      "title": "Edit text",
      "icon": "edit",
      "default": True,
      "callbacks": {
        "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-button-text'])
      }
    }]

  def _set_icon(self):
    if self.icon:
      self.dom_nodes['anvil-m3-button-icon'].innerText = self.icon
      self.dom_nodes['anvil-m3-button-icon'].style.display = "flex"
      if self.text:
        self.dom_nodes['anvil-m3-button'].classList.add('anvil-m3-icon-padding')
      else:
        self.dom_nodes['anvil-m3-button'].classList.add('noText')
    else:
      self.dom_nodes['anvil-m3-button-icon'].innerText = ""
      self.dom_nodes['anvil-m3-button-icon'].style.display = "none"

  def _set_text(self):
    if self.text:
      self.dom_nodes['anvil-m3-button-text'].innerText = self.text
    else:
      if not self.icon:
        if anvil.designer.in_designer:
          self.dom_nodes['anvil-m3-button-text'].innerText = anvil.designer.get_design_name(self)
          self.dom_nodes['anvil-m3-button-text'].classList.add('anvil-m3-textlessComponentText')
        else: 
          self.dom_nodes['anvil-m3-button-text'].innerText = "Button"
      else:
        self.dom_nodes['anvil-m3-button-text'].innerText = ""
      
  def _update_button_look(self, value = None):
    buttonNode = self.dom_nodes['anvil-m3-button']
    iconNode = self.dom_nodes['anvil-m3-button-icon']
    textNode = self.dom_nodes['anvil-m3-button-text']

    buttonNode.classList.remove('anvil-m3-icon-padding')
    textNode.classList.remove('anvil-m3-textlessComponentText')
    buttonNode.classList.remove('noText')
    
    self._set_icon()
    self._set_text()
    
  icon = property_with_callback("icon", _update_button_look)
  text = property_with_callback("text", _update_button_look)

  def _set_enabled(self, value):
    if value:
      self.dom_nodes['anvil-m3-button'].removeAttribute("disabled")
    else:
      self.dom_nodes['anvil-m3-button'].setAttribute("disabled", " ")
      
  enabled = property_with_callback("enabled", _set_enabled)

  def _set_appearance(self, value):
    button = self.dom_nodes['anvil-m3-button']
    button.classList.remove('anvil-m3-elevated')
    button.classList.remove('anvil-m3-filled')
    button.classList.remove('anvil-m3-tonal')
    button.classList.remove('anvil-m3-outlined')
    if value:
      button.classList.add(f"anvil-m3-{value}")
      
  appearance = property_with_callback("appearance", _set_appearance)

  def form_show(self, **event_args):
    self._update_button_look()
    
  text_color = color_property('anvil-m3-button-text', 'color', 'text_color')
  font_family = font_family_property('anvil-m3-button-text')
  font_size = font_size_property('anvil-m3-button-text')
  underline = underline_property('anvil-m3-button-text')
  italic = italic_property('anvil-m3-button-text')
  bold = custom_bold_property('anvil-m3-button-text')
  icon_color = color_property('anvil-m3-button-icon', 'color', 'icon_color')
  icon_size = font_size_property('anvil-m3-button-icon', 'icon_size')
  background = color_property('anvil-m3-button', 'backgroundColor', 'background')
  margin = margin_property('anvil-m3-button-component')
  border = style_property('anvil-m3-button', 'border', 'border')
  tooltip = tooltip_property('anvil-m3-button')

  def _set_icon_align(self, value):
    self.dom_nodes['anvil-m3-button'].classList.toggle('anvil-m3-right-icon', value is 'right')
    
  icon_align = property_with_callback('icon_align', _set_icon_align)



  
