from ._anvil_designer import LinkTemplate
from anvil import *
import anvil.designer
from ...Functions import visible_property, underline_property, italic_property, style_property, color_property, innerText_property, bold_property, font_size_property, href_property


class Link(LinkTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    if anvil.designer.in_designer and not self.text:
      self.text = anvil.designer.get_design_name(self)
      self.dom_nodes['anvil-m3-link'].addEventListener("click", self.handle_click)

    def handle_click(self, event):
      self.raise_event("click")

  def _anvil_get_design_info_(self, as_layout=False):
    di = super()._anvil_get_design_info_(as_layout)
    di['interactions'] = [{
      "type": "whole_component",
      "title": "Edit text",
      "icon": "edit",
      "default": True,
      "callbacks": {
        "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-link'])
      }
    }]
    return di

  text = innerText_property('anvil-m3-link')
  url = href_property('anvil-m3-link')
  align = style_property('anvil-m3-link-container', 'justifyContent')
  italic = italic_property('anvil-m3-link')
  bold = bold_property('anvil-m3-link')
  font = style_property('anvil-m3-link', 'fontFamily')
  font_size = font_size_property('anvil-m3-link')
  material_icon = innerText_property('anvil-m3-link-icon')
  underline = underline_property('anvil-m3-link')
  visible = visible_property('anvil-m3-link-container', 'flex')
  