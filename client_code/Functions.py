from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import document
from anvil.property_utils import set_element_margin, set_element_padding, set_element_spacing
from .utils import noop, fui
from .Components.Tooltip import Tooltip
import anvil.designer

def theme_color_to_css(color:str):
  if color.startswith('theme:'):
    color = color.lstrip('theme:')
    return app.theme_colors[color]
  else:
    return color

#REUSABLE PROPERTIES
def property_with_callback(prop, cb):
  def getter(self):
    return self._props.get(prop)
  def setter(self, value):
    self._props[prop] = value
    cb(self, value)
  return property(getter, setter)
  
def property_without_callback(prop):
  def getter(self):
    return self._props.get(prop)
  def setter(self, value):
    self._props[prop] = value
  return property(getter, setter)

def color_property(dom_node_name, style_prop, prop_name):
  def set_color(self, value):
    if value: value = theme_color_to_css(value)
    self.dom_nodes[dom_node_name].style[style_prop] = value
  return property_with_callback(prop_name, set_color)
  # def getter(self):
  #   return self.dom_nodes[dom_node_name].style[style_prop]

  # def setter(self, value):
  #   if value: value = theme_color_to_css(value)
  #   self.dom_nodes[dom_node_name].style[style_prop] = value

  # return property(getter, setter)

def style_property(dom_node_name, style_prop, prop_name):
  def set_style(self, value):
    self.dom_nodes[dom_node_name].style[style_prop] = value
  return property_with_callback(prop_name, set_style)

def innerHTML_property(dom_node_name, prop_name="text"):
  def set_innterHTML(self, value):
    self.dom_nodes[dom_node_name].innerHTML = value
  return property_with_callback(prop_name, set_innterHTML)

def innerText_property(dom_node_name, prop_name="text"):
  def set_innerText(self, value):
    self.dom_nodes[dom_node_name].innerText = value
  return property_with_callback(prop_name, set_innerText)

def href_property(dom_node_name, prop_name="url"):
  def set_href(self, value):
    self.dom_nodes[dom_node_name].href = value
  return property_with_callback(prop_name, set_href)

def checked_property(dom_node_name, prop_name="selected"):
  def set_checked(self, value):
    self.dom_nodes[dom_node_name].checked = value
  return property_with_callback(prop_name, set_checked)

def enabled_property(dom_node_name, prop_name="enabled"):
  def set_enabled(self, value):
    if value:
      self.dom_nodes[dom_node_name].removeAttribute("disabled")
    else:
      self.dom_nodes[dom_node_name].setAttribute("disabled", " ")
  return property_with_callback(prop_name, set_enabled)

def name_property(dom_node_name, prop_name="name"):
  def set_name(self, value):
    self.dom_nodes[dom_node_name].name = value
  return property_with_callback(prop_name, set_name)

def value_property(dom_node_name, prop_name="value"):
  def set_value(self, value):
    self.dom_nodes[dom_node_name].value = value
  return property_with_callback(prop_name, set_value)

def underline_property(dom_node_name, prop_name="underline"):
  def set_underline(self, value):
    if value:
      self.dom_nodes[dom_node_name].style.textDecoration = 'underline'
    else:
      self.dom_nodes[dom_node_name].style.textDecoration = 'none'
  return property_with_callback(prop_name, set_underline)

def italic_property(dom_node_name, prop_name="italic"):
  def set_italic(self, value):
    if value:
      self.dom_nodes[dom_node_name].style.fontStyle = 'italic'
    else:
      self.dom_nodes[dom_node_name].style.fontStyle = 'normal'
  return property_with_callback(prop_name, set_italic)

def bold_property(dom_node_name, prop_name="bold"):
  return custom_bold_property(dom_node_name, prop_name, 'bold')

def custom_bold_property(dom_node_name, prop_name="bold", custom_bold=500):
  def set_bold(self, value):
    if value:
      self.dom_nodes[dom_node_name].style.fontWeight = custom_bold
    else:
      self.dom_nodes[dom_node_name].style.fontWeight = 'normal'
  return property_with_callback(prop_name, set_bold)
  

def font_size_property(dom_node_name, prop_name="font_size"):
  def set_font_size(self, value):
    self._font_size = value
    if value: value = f'{value}px'
    self.dom_nodes[dom_node_name].style.fontSize = value
  return property_with_callback(prop_name, set_font_size)
  
def font_family_property(dom_node_name, prop_name="font_family"):
  def set_font_family(self, value):
    self.dom_nodes[dom_node_name].style.fontFamily = value
  return property_with_callback(prop_name, set_font_family)
  
def border_property(dom_node_name, prop_name="border"):
  def set_border(self, value):
    self.dom_nodes[dom_node_name].style.border = value
  return property_with_callback(prop_name, set_border)

def margin_property(dom_node_name, prop_name="margin"):
  def set_margin(self, value):
    set_element_margin(self.dom_nodes[dom_node_name], value)
  return property_with_callback(prop_name, set_margin)

def spacing_property(dom_node_name, prop_name="spacing"):
  def set_spacing(self, value):
    set_element_spacing(self.dom_nodes[dom_node_name], value)
  return property_with_callback(prop_name, set_spacing)

def padding_property(dom_node_name, prop_name="padding"):
  def set_padding(self, value):
    set_element_padding(self.dom_nodes[dom_node_name], value)
  return property_with_callback(prop_name, set_padding)

def tooltip_property(dom_node_name, prop_name="tooltip"):
  #To use this property, add self.tooltip_node = None to the init of your component
  def set_tooltip(self, value):
    if anvil.designer.in_designer:
      return
      
    self._cleanup = noop
    reference_element = self.dom_nodes[dom_node_name]
    if value:
      tooltip_el = Tooltip(text=value)
      self.tooltip_node = tooltip_el.tooltip_node
      document.body.append(self.tooltip_node)

      tooltip_events = {
        'mouseenter': tooltip_el.show_tooltip,
        'mouseleave': tooltip_el.hide_tooltip,
        'focus': tooltip_el.show_tooltip,
        'blur': tooltip_el.hide_tooltip
        }
      for event, listener in tooltip_events.items():
        reference_element.addEventListener(event, listener)
      self._cleanup = fui.auto_update(reference_element, self.tooltip_node, placement="bottom-start")
    else:
      if self.tooltip_node:
        self.tooltip_node.remove()
        self._cleanup()
        self._cleanup = noop
  return property_with_callback(prop_name, set_tooltip)

  
  


