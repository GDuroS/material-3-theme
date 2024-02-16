from ._anvil_designer import RadioButtonTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import HtmlTemplate
from anvil.js.window import document
import anvil.designer
from ...Functions import checked_property, role_property, tooltip_property, name_property, innerText_property, enabled_property, style_property, underline_property, italic_property, border_property, bold_property, font_size_property, color_property, theme_color_to_css, value_property, property_with_callback, font_family_property, margin_property
from ...utils import gen_id

class RadioButton(RadioButtonTemplate):
  def __init__(self, **properties):
    self._props = properties
    self._tooltip_node = None
    self._design_name = "" 
    self.init_components(**properties)
    
    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)
    if not anvil.designer.in_designer:
        id = gen_id()
        self.dom_nodes["anvil-m3-radiobutton-input"].id = id
        self.dom_nodes["anvil-m3-radiobutton-label"].setAttribute("for", id)

  def _on_mount(self, **event_args):
    self.dom_nodes['anvil-m3-radiobutton-hover'].addEventListener("click", self._handle_click)

  def _on_cleanup(self, **event_args):
    self.dom_nodes['anvil-m3-radiobutton-hover'].removeEventListener("click", self._handle_click)
    
  # Properties 
  visible = HtmlTemplate.visible
  group_name = name_property('anvil-m3-radiobutton-input', "group_name")
  value = value_property('anvil-m3-radiobutton-input')
  enabled = enabled_property('anvil-m3-radiobutton-input')
  italic = italic_property('anvil-m3-radiobutton-label')
  bold = bold_property('anvil-m3-radiobutton-label')
  underline = underline_property('anvil-m3-radiobutton-label')
  font_size = font_size_property('anvil-m3-radiobutton-label')
  border = border_property('anvil-m3-radiobutton-container')
  font = font_family_property('anvil-m3-radiobutton-label', 'font')
  text_color = color_property('anvil-m3-radiobutton-label', 'color', 'text_color')
  background = color_property('anvil-m3-radiobutton-component', 'backgroundColor', 'background')
  align = style_property('anvil-m3-radiobutton-component', 'justifyContent', 'align')
  # selected = checked_property('anvil-m3-radiobutton-input')
  margin = margin_property('anvil-m3-radiobutton-component')
  tooltip = tooltip_property('anvil-m3-radiobutton-component')
  role = role_property('anvil-m3-radiobutton-container')
  
  @property
  def radio_color(self):
    return self._props.get('radio_color')

  @radio_color.setter
  def radio_color(self, value):
    if value: value = theme_color_to_css(value)
    self.dom_nodes['anvil-m3-radiobutton-checked'].style['color'] = value
    self.dom_nodes['anvil-m3-radiobutton-unchecked'].style['color'] = value
    self._props['radio_color'] = value

  @property
  def selected(self):
    return self.dom_nodes['anvil-m3-radiobutton-input'].checked

  @selected.setter
  def selected(self, value):
    self.dom_nodes['anvil-m3-radiobutton-input'].checked = value

  def _set_text(self, value):
    v = value
    self.dom_nodes['anvil-m3-radiobutton-label'].classList.toggle('anvil-m3-textlessComponentText', False)
    if anvil.designer.in_designer and not value:
      v = self._design_name
      self.dom_nodes['anvil-m3-radiobutton-label'].classList.toggle('anvil-m3-textlessComponentText', True)
    self.dom_nodes['anvil-m3-radiobutton-label'].innerText = v
    
  text = property_with_callback("text", _set_text)
  
  # Class Functions
  def _anvil_get_interactions_(self):
    return [
      {
        "type": "whole_component",
        "title": "Edit text",
        "icon": "edit",
        "default": True,
        "callbacks": {
          "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-radiobutton-label'])
        },   
      },
      {
        "type": "region",
        "bounds": self.dom_nodes['anvil-m3-radiobutton-hover'],
        "sensitivity": 0,
        "callbacks": {
          "execute": self._toggle_selected
        }
      }
    ]

  def _toggle_selected(self):
    self.selected = not self.selected
    anvil.designer.update_component_properties(self, {'selected': self.selected})
   
  def _handle_click(self, event):
    if self.enabled:
      self.dom_nodes['anvil-m3-radiobutton-input'].focus()
      self.selected = True 
      self.raise_event("change")

  def form_show(self, **event_args):
    if anvil.designer.in_designer:
      self._design_name = anvil.designer.get_design_name(self)
      if not self.text:
        self.dom_nodes['anvil-m3-radiobutton-label'].innerText = self._design_name

  def get_group_value(self):
    selected_item = document.querySelector(f".anvil-m3-radiobutton-input[name={self.group_name}]:checked")
    return selected_item.value
