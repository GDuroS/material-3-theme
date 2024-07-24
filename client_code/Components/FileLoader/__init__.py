from ._anvil_designer import FileLoaderTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Functions import property_with_callback, underline_property, role_property, tooltip_property, italic_property, style_property, color_property, innerText_property, bold_property, font_size_property, enabled_property, font_family_property, margin_property
from anvil.js.window import FileReader, Uint8Array
from ...utils import gen_id

#todo: fix focus state within column panel

class FileLoader(FileLoaderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self._props = properties
    self._tooltip_node = None
    self.init_components(**properties)

    self._handle_change = self._handle_change
    self._handle_focus = self._handle_focus
    self._handle_lost_focus = self._handle_lost_focus

    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)
    
    if not anvil.designer.in_designer:
      id = gen_id()
      self.dom_nodes["anvil-m3-fileloader-input"].id = id
      self.dom_nodes["anvil-m3-fileloader-label"].setAttribute("for", id)

  def _anvil_get_interactions_(self):
    return [{
      "type": "whole_component",
      "title": "Edit text",
      "icon": "edit",
      "default": True,
      "callbacks": {
        "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-fileloader-label'])
      }
    }]

  #!defMethod(_)!2: "Clear any selected files from this FileLoader." ["clear"]
  def clear(self):
    self.dom_nodes['anvil-m3-fileloader-input'].value = ''
    self.file = None
    self.dom_nodes['anvil-m3-fileloader-label'].innerText = self.text
    #update show_state text if present

  #!defMethod(_)!2: "Set the keyboard focus to this FileLoader." ["focus"]
  def focus(self):
    self.dom_nodes['anvil-m3-fileloader-container'].focus()

  #!defMethod(_)!2: "Open the file selector from code, this should be called within a click event handler for another component." ["open_file_selector"]
  def open_file_selector(self):
    self.dom_nodes['anvil-m3-fileloader-input'].click()

  def _on_mount(self, **event_args):
    self.dom_nodes['anvil-m3-fileloader-input'].addEventListener("change", self._handle_change)
    self.dom_nodes['anvil-m3-fileloader-container'].addEventListener("focus", self._handle_focus)
    self.dom_nodes['anvil-m3-fileloader-container'].addEventListener("blur", self._handle_lost_focus)
    
  def _on_cleanup(self, **event_args):
    self.dom_nodes['anvil-m3-fileloader-input'].removeEventListener("change", self._handle_change)
    self.dom_nodes['anvil-m3-fileloader-container'].removeEventListener("focus", self._handle_focus)
    self.dom_nodes['anvil-m3-fileloader-container'].removeEventListener("blur", self._handle_lost_focus)

  def _handle_change(self, event, **event_args):
    files = self.dom_nodes['anvil-m3-fileloader-input'].files
    file_list = [anvil.js.to_media(file) for file in files]
    self.file = file_list[0]
    self.raise_event('change', file=file_list[0], files=file_list)
    if self.show_state:
      num_files = len(files)
      self.dom_nodes['anvil-m3-fileloader-label'].innerText = "1 file selected" if num_files == 1 else f"{num_files} files selected"

  def _handle_focus(self, event, **event_args):
    self.raise_event("focus")

  def _handle_lost_focus(self, event, **event_args):
    self.raise_event("lost_focus")

  def _set_appearance(self, value):
    file_loader = self.dom_nodes['anvil-m3-fileloader-container']
    file_loader.classList.remove('anvil-m3-elevated')
    file_loader.classList.remove('anvil-m3-filled')
    file_loader.classList.remove('anvil-m3-tonal')
    file_loader.classList.remove('anvil-m3-outlined')
    if value:
      file_loader.classList.add(f"anvil-m3-{value}")

  #!defAttr()!1: {name:"text",type:"string",description:"The text displayed on this component"}
  #!defAttr()!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."} 
  #!defAttr()!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!defAttr()!1: {name:"text_color",type:"color",description:"The color of the text on the component."} 
  #!defAttr()!1: {name:"icon_color",type:"color",description:"The color of the icon displayed on this component."}
  #!defAttr()!1: {name:"background_color",type:"color",description:"The color of the background of this component."}
  #!defAttr()!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!defAttr()!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!defAttr()!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!defAttr()!1: {name:"font",type:"string",description:"The font family to use for this component."}
  #!defAttr()!1: {name:"icon_size",type:"number",description:"Size (pixels) of the icon displayed on this component."}
  #!defAttr()!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!defAttr()!1: {name:"align",type:"enum", options:["left", "center", "right"],description:"The position of this component in the available space."} 
  #!defAttr()!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
  #!defAttr()!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
  #!defAttr()!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!defAttr()!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"} 
  #!defAttr()!1: {name:"appearance",type:"enum",options:["elevated", "filled", "tonal", "outlined"],description:"A predefined style for this component."}
  #!defAttr()!1: {name:"show_state",type:"boolean",description:"If True, display a message describing selected files."}
  #!defAttr()!1: {name:"material_icon",type:"enum",description:"The icon to display on this component."} 
  #!defAttr()!1: {name:"file_types",type:"string",description:"Specify what type of file to upload. Can accept a MIME type (eg 'image/png' or 'image/*'), or an extension (eg '.png'), or a comma-separated set of them (eg '.png,.jpg,.jpeg')."} 
  #!defAttr()!1: {name:"multiple",type:"boolean",description:"If True, this FileLoader can load multiple files at the same time."} 
  #!defAttr()!1: {name:"file",type:"object",description:"The currently selected file (or the first, if multiple files are selected). This is a Media object."} 
  
  text = innerText_property('anvil-m3-fileloader-label')
  visible = HtmlTemplate.visible
  enabled = enabled_property('anvil-m3-fileloader-input')
  text_color = color_property('anvil-m3-fileloader-label', 'color', 'text_color')
  icon_color = color_property('anvil-m3-fileloader-icon', 'color', 'icon_color')
  background_color = color_property('anvil-m3-fileloader-form', 'backgroundColor', 'background_color')
  underline = underline_property('anvil-m3-fileloader-label')
  italic = italic_property('anvil-m3-fileloader-label')
  bold = bold_property('anvil-m3-fileloader-label')
  font = font_family_property('anvil-m3-fileloader-label', 'font')
  icon_size = font_size_property('anvil-m3-fileloader-icon', 'icon_size')
  font_size = font_size_property('anvil-m3-fileloader-label', 'font_size')
  align = style_property('anvil-m3-fileloader-form', 'justifyContent', 'align')
  border = style_property('anvil-m3-fileloader-container', 'border', 'border')
  margin = margin_property('anvil-m3-fileloader-form')
  tooltip = tooltip_property('anvil-m3-fileloader-container')
  role = role_property('anvil-m3-fileloader-container')
  appearance = property_with_callback("appearance", _set_appearance)

  @property
  def show_state(self):
    return self._props.get('show_state')

  @show_state.setter
  def show_state(self, value):
    self._props['show_state'] = value

  @property
  def material_icon(self):
    return self._material_icon

  @material_icon.setter
  def material_icon(self, value):
    self._material_icon = value
    if value:
      self.dom_nodes['anvil-m3-fileloader-icon'].style.marginRight = "8px"
    else:
      self.dom_nodes['anvil-m3-fileloader-icon'].style.marginRight = ""
    self.dom_nodes['anvil-m3-fileloader-icon'].innerText = value

  @property
  def file_types(self):
    return self._props.get("file_types")

  @file_types.setter
  def file_types(self, value):
    self._props["file_types"] = value
    self.dom_nodes['anvil-m3-fileloader-input'].accept = value

  @property
  def multiple(self):
    return self._props.get("multiple")

  @multiple.setter
  def multiple(self, value):
    self._props["multiple"] = value
    self.dom_nodes['anvil-m3-fileloader-input'].multiple = value

  #TODO: file should be media object
  @property
  def file(self):
    return self._props.get("file")

  @file.setter
  def file(self, value):
    self._props["file"] = value

#!defClass(material_3,FileLoader)!:
