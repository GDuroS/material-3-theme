from ._anvil_designer import RadioButtonTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import HtmlTemplate
from anvil.js.window import document
import anvil.designer
from ...components import RadioGroup
from ...Functions import role_property, tooltip_property, enabled_property, style_property, underline_property, italic_property, border_property, bold_property, font_size_property, color_property, theme_color_to_css, font_family_property, spacing_property
from ...Functions import property_with_callback, property_without_callback
from ...utils import gen_id

class RadioButton(RadioButtonTemplate):
  def __init__(self, **properties):
    self.tag = ComponentTag()
    self._props = properties
    self._tooltip_node = None
    self._design_name = ""
    self.group = None
    self.init_components(**properties)

    if not anvil.designer.in_designer and self._props["value"] == "":
      self._props["value"] = self._props["text"]
    
    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)
    if not anvil.designer.in_designer:
        id = gen_id()
        self.dom_nodes["anvil-m3-radiobutton-input"].id = id
        self.dom_nodes["anvil-m3-radiobutton-input"].value = id
        self.dom_nodes["anvil-m3-radiobutton-label"].setAttribute("for", id)

  def _on_mount(self, **event_args):
    self.dom_nodes['anvil-m3-radiobutton-hover'].addEventListener("click", self._handle_click)
    self.dom_nodes['anvil-m3-radiobutton-input'].addEventListener("change", self._handle_change)
    self.group = RadioGroup.enclosing(self)
    self.group._add_button(self)
    self.dom_nodes["anvil-m3-radiobutton-input"].name = id(self.group)

  def _on_cleanup(self, **event_args):
    self.dom_nodes['anvil-m3-radiobutton-hover'].removeEventListener("click", self._handle_click)
    self.dom_nodes['anvil-m3-radiobutton-input'].removeEventListener("change", self._handle_change)
  
  #!componentEvent(material_3.RadioButton)!1: {name: "change", description: "When the Radio Button is selected or unselected."}
  #!componentEvent(material_3.RadioButton)!1: {name: "show", description: "When the Radio Button is shown on the screen."}
  #!componentEvent(material_3.RadioButton)!1: {name: "hide", description: "When the Raio Button is removed from the screen."}

  #!componentProp(material_3.RadioButton)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(material_3.RadioButton)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."} 
  #!componentProp(material_3.RadioButton)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(material_3.RadioButton)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(material_3.RadioButton)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(material_3.RadioButton)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!componentProp(material_3.RadioButton)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
  #!componentProp(material_3.RadioButton)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(material_3.RadioButton)!1: {name:"text_color",type:"color",description:"The color of the text on the component."} 
  #!componentProp(material_3.RadioButton)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}
  #!componentProp(material_3.RadioButton)!1: {name:"align",type:"enum",description:"The position of this component in the available space."} 
  #!componentProp(material_3.RadioButton)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(material_3.RadioButton)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(material_3.RadioButton)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"} 
  #!componentProp(material_3.RadioButton)!1: {name:"text",type:"string",description:"The text displayed on this component"}
  #!componentProp(material_3.RadioButton)!1: {name:"radio_color",type:"color",description:"The color of the radio button."}
  #!componentProp(material_3.RadioButton)!1: {name:"selected",type:"boolean",description:"If True, the radio button is selected."}
  #!componentProp(material_3.RadioButton)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  # Properties 
  enabled = enabled_property('anvil-m3-radiobutton-input')
  visible = HtmlTemplate.visible
  value = property_without_callback('value')
  underline = underline_property('anvil-m3-radiobutton-label')
  italic = italic_property('anvil-m3-radiobutton-label')
  bold = bold_property('anvil-m3-radiobutton-label')
  font_size = font_size_property('anvil-m3-radiobutton-label')
  border = border_property('anvil-m3-radiobutton-container')
  font_family = font_family_property('anvil-m3-radiobutton-label', 'font_family')
  text_color = color_property('anvil-m3-radiobutton-label', 'color', 'text_color')
  background_color = color_property('anvil-m3-radiobutton-component', 'backgroundColor', 'background')
  align = style_property('anvil-m3-radiobutton-component', 'justifyContent', 'align')
  spacing = spacing_property('anvil-m3-radiobutton-component')
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
      self._handle_change(self)

  def _handle_change(self, event):
    self.group._handle_change()
    self.raise_event("change")

  def form_show(self, **event_args):
    if anvil.designer.in_designer:
      self._design_name = anvil.designer.get_design_name(self)
      if not self.text:
        self.dom_nodes['anvil-m3-radiobutton-label'].innerText = self._design_name

#!defClass(material_3, RadioButton, anvil.Component)!:
