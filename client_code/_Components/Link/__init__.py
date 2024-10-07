from ._anvil_designer import LinkTemplate
from anvil import *
import anvil.designer
from ...Functions import tooltip_property, role_property, underline_property, italic_property, style_property, color_property, innerText_property, bold_property, font_size_property, href_property, font_family_property, spacing_property

from anvil import HtmlTemplate

class Link(LinkTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.temp_url = None
    self._props = properties
    self._tooltip_node = None
    self.init_components(**properties)
    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)
    

  def _on_mount(self, **event_args):
    self.dom_nodes['anvil-m3-link'].addEventListener("click", self._handle_click)
    
  def _on_cleanup(self, **event_args):
    self.dom_nodes['anvil-m3-link'].removeEventListener("click", self._handle_click)
    self.revoke_tmp_url()
    
  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    if anvil.designer.in_designer and not self.text and not self.material_icon and not self.get_components():
      self.dom_nodes['anvil-m3-link-text'].innerText = anvil.designer.get_design_name(self)
      self.dom_nodes['anvil-m3-link-text'].style.display = 'block'
    
  def _handle_click(self, event):
    keys = {'shift': event.shiftKey, 'alt': event.altKey, 'ctrl': event.ctrlKey, 'meta': event.metaKey}
    self.raise_event("click", keys=keys, event=event)

  def _anvil_get_interactions_(self):
    return [{
      "type": "whole_component",
      "title": "Edit text",
      "icon": "edit",
      "default": True,
      "callbacks": {
        "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-link-text'])
      }
    }]

  #!componentEvent(material_3.Link)!1: {name: "click", description: "When the Link is clicked."}
  #!componentEvent(material_3.Link)!1: {name: "show", description: "When the Link is shown on the screen."}
  #!componentEvent(material_3.Link)!1: {name: "hide", description: "When the Link is removed from the screen."}

  #!componentProp(material_3.Link)!1: {name:"text",type:"string",description:"The text displayed on this component."}
  #!componentProp(material_3.Link)!1: {name:"align",type:"enum", options:["left", "center", "right"],description:"The position of this component in the available space."} 
  #!componentProp(material_3.Link)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(material_3.Link)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(material_3.Link)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(material_3.Link)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(material_3.Link)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!componentProp(material_3.Link)!1: {name:"material_icon",type:"enum",description:"The icon to display on this component."} 
  #!componentProp(material_3.Link)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."} 
  #!componentProp(material_3.Link)!1: {name:"text_color",type:"color",description:"The color of the text on the component."} 
  #!componentProp(material_3.Link)!1: {name:"icon_color",type:"color",description:"The color of the icon displayed on this component."}
  #!componentProp(material_3.Link)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
  #!componentProp(material_3.Link)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(material_3.Link)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(material_3.Link)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."} 
  #!componentProp(material_3.Link)!1: {name:"url",type:"string",description:"TThe target URL of the link. Can be set to a URL string or to a Media object."}
  #!componentProp(material_3.Link)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(material_3.Link)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}
  #!componentProp(material_3.Link)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}

  # text = innerText_property('anvil-m3-link-text')
  align = style_property('anvil-m3-link-container', 'justifyContent', 'align')
  italic = italic_property('anvil-m3-link-text')
  bold = bold_property('anvil-m3-link')
  font_family = font_family_property('anvil-m3-link', 'font_family')
  font_size = font_size_property('anvil-m3-link')
  underline = underline_property('anvil-m3-link-text')
  visible = HtmlTemplate.visible
  text_color = color_property('anvil-m3-link', 'color', 'text_color')
  icon_color = color_property('anvil-m3-link-icon', 'color', 'icon_color')
  border = style_property('anvil-m3-link', 'border', 'border')
  spacing = spacing_property('anvil-m3-link-container')
  tooltip = tooltip_property('anvil-m3-link')
  role = role_property('anvil-m3-link')
  background_color = color_property('anvil-m3-link-container', 'backgroundColor', 'background_color')

  @property
  def url(self):
    return self._props.get('url')

  @url.setter
  def url(self, value):
    self._props['url'] = value
    self.dom_nodes['anvil-m3-link'].removeAttribute("download")
    self.dom_nodes['anvil-m3-link'].removeAttribute("target")
    self.revoke_tmp_url()
    if value: 
      if isinstance(value, Media):
        if value.name:
          self.dom_nodes['anvil-m3-link'].setAttribute("download", value.name)
        self.temp_url = anvil.media.TempUrl(value)
        self.dom_nodes['anvil-m3-link'].href = self.temp_url.url
        # self.dom_nodes['anvil-m3-link'].href = value.get_url()
      else:
        self.dom_nodes['anvil-m3-link'].href = value
        self.dom_nodes['anvil-m3-link'].setAttribute("target", "_blank")
    else:
      self.dom_nodes['anvil-m3-link'].href = 'javascript:void(0)'

  def revoke_tmp_url(self):
    if self.temp_url:
      self.temp_url.revoke()

  @property
  def icon_size(self):
    return self._icon_size

  @icon_size.setter
  def icon_size(self, value):
    self._icon_size = value
    if value: value = f'{value}px'
    self.dom_nodes['anvil-m3-link-icon'].style.fontSize = value

  @property
  def material_icon(self):
    return self.dom_nodes['anvil-m3-link-icon'].innerText

  @material_icon.setter
  def material_icon(self, value):
    if value and self.text:
      self.dom_nodes['anvil-m3-link-icon'].style.marginRight = "8px"
    else:
      self.dom_nodes['anvil-m3-link-icon'].style.marginRight = ""
    self.dom_nodes['anvil-m3-link-icon'].innerText = value

  @property
  def text(self):
    return self._props.get('text')

  @text.setter
  def text(self, value):
    self._props['text'] = value
    self.dom_nodes['anvil-m3-link-text'].innerText = value
    if value:
      self.dom_nodes['anvil-m3-link-text'].style.display = 'block'
    else:
      self.dom_nodes['anvil-m3-link-text'].style.display = 'none'



#!defClass(material_3, Link, anvil.Component)!:
