from ._anvil_designer import SliderTemplate
from anvil import *
from anvil.js.window import document, ResizeObserver
import anvil.js
from anvil import HtmlTemplate
from ...Functions import enabled_property, value_property, color_property, property_with_callback, theme_color_to_css, margin_property, tooltip_property

class Slider(SliderTemplate):
  def __init__(self, **properties):
    self.label_container = document.createElement('div')
    self.label_container.classList.add('anvil-m3-slider-label-container')
    self.label = document.createElement('div')
    self.label.classList.add('anvil-m3-slider-label')
    self.label_container.appendChild(self.label)
    self._props = properties
    self.tooltip_node = None
    self.init_components(**properties)
    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

  def _on_mount(self, **event_args):
    self.dom_nodes["anvil-m3-slider-input"].addEventListener("input", self.on_input)
    self.dom_nodes["anvil-m3-slider-input"].addEventListener("mousedown", self.on_mouse_down)
    self.dom_nodes['anvil-m3-slider-input'].addEventListener("change", self.on_change)
    self.resize_observer = ResizeObserver(self._on_window_resize)
    self.resize_observer.observe(self.dom_nodes['anvil-m3-slider'])
  
  def _on_cleanup(self, **event_args):
    self.dom_nodes['anvil-m3-slider-input'].removeEventListener('input', self.on_input)
    self.dom_nodes['anvil-m3-slider-input'].removeEventListener('mousedown', self.on_mouse_down)
    self.dom_nodes['anvil-m3-slider-input'].removeEventListener("change", self.on_change)
    self.resize_observer.unobserve(self.dom_nodes['anvil-m3-slider'])

  def on_change(self, event):
    self.raise_event("change")
  
  def on_input(self, event):
    self._update_progress()

  def on_mouse_down(self, event):
    self._do_show_label()
    document.addEventListener("mouseup", self.on_mouse_up)

  def on_mouse_up(self, event):
    self._do_hide_label()
    document.removeEventListener("mouseup", self.on_mouse_up)

  def _on_window_resize(self, *args):
    self.dom_nodes['anvil-m3-slider-track-container'].style.width = self._get_track_width()
    
  def _update_progress(self):
    slider = self.dom_nodes["anvil-m3-slider-input"]
    progress = self.dom_nodes["anvil-m3-slider-progress"]
    range = float(slider.max) - float(slider.min)
    abs_value = float(slider.value) - float(slider.min)
    percent = (abs_value / range) * 100;
    progress.style.width = str(percent) + "%"
    progress_right, progress_top = self._check_position()
    self.label.textContent = slider.value
    self.label_container.style.left = str(progress_right) + "px"
    self.label_container.style.top = str(progress_top) + "px"

  def _get_track_width(self):
    input = self.dom_nodes["anvil-m3-slider-input"]
    input_width = input.getBoundingClientRect().width
    return str(input_width - 20) + "px"

  def _check_position(self):
    progress_rect = self.dom_nodes["anvil-m3-slider-progress"].getBoundingClientRect()
    progress_right = progress_rect.right
    progress_top = progress_rect.top
    return progress_right, progress_top

  def _do_show_label(self):
    if self.show_label:
      self.label_container.remove()
      document.body.appendChild(self.label_container)
      self._update_progress()

  def _do_hide_label(self):
    self.label_container.remove()

  def _set_thumb_color(self, value=None):
    if self.thumb_color:
      self.dom_nodes['anvil-m3-slider-input'].style.setProperty('--anvil-m3-slider-thumb-color', theme_color_to_css(self.thumb_color))
    else:
      self.dom_nodes['anvil-m3-slider-input'].style.setProperty('--anvil-m3-slider-thumb-color', 'var(--anvil-m3-primary)')
      
  thumb_color = property_with_callback('thumb_color', _set_thumb_color)
  progress_color = color_property("anvil-m3-slider-progress", 'background', 'progress_color')
  track_color = color_property("anvil-m3-slider-background", 'background', 'track_color')
  margin = margin_property("anvil-m3-slider")
  tooltip = tooltip_property('anvil-m3-slider')
  visible = HtmlTemplate.visible

  @property
  def label_color(self):
    return self._props.get('label_color')

  @label_color.setter
  def label_color(self, value):
    self._props['label_color'] = value
    self.label_container.style.background = theme_color_to_css(value)

  @property
  def label_text_color(self):
    return self._props.get('label_text_color')

  @label_text_color.setter
  def label_text_color(self, value):
    self._props['label_text_color'] = value
    self.label_container.style.color = theme_color_to_css(value)

  @property
  def value(self):
    return self._props.get('value')

  @value.setter
  def value(self, value):
    if value > self.max:
      raise ValueError("Value cannot be more than max")
    self._props['value'] = value
    self.dom_nodes["anvil-m3-slider-input"].value = value
    if not value:
      value = 0
    self._update_progress()

  @property
  def min(self):
    return self._props.get('min')

  @min.setter
  def min(self, value):
    self._props['min'] = value
    self.dom_nodes["anvil-m3-slider-input"].min = value
    self._update_progress()

  @property
  def max(self):
    return self._props.get('max')

  @max.setter
  def max(self, value):
    self._props['max'] = value
    self.dom_nodes["anvil-m3-slider-input"].max = value
    self._update_progress()

  @property
  def step(self):
    return self._props.get('step')

  @step.setter
  def step(self, value):
    if not value:
      value = 1
    self._props['step'] = value
    self.dom_nodes["anvil-m3-slider-input"].step = value
    self._update_progress()
  
  @property
  def show_label(self):
    return self._props.get('show_label')

  @show_label.setter
  def show_label(self, value):
    self._props['show_label'] = value

  @property
  def enabled(self):
    return self._enabled

  @enabled.setter
  def enabled(self, value):
    self._enabled = value
    full_slider = self.dom_nodes['anvil-m3-slider']
    input = self.dom_nodes['anvil-m3-slider-input']
    if value:
      input.removeAttribute("disabled")
      full_slider.classList.remove("anvil-m3-slider-disabled")
    else:
      input.setAttribute("disabled", " ")
      full_slider.classList.add("anvil-m3-slider-disabled")

  def _set_markers(self):
    markers_container = self.dom_nodes["anvil-m3-slider-markers-container"]
    slider_range = self.max - self.min
    if self.step:
      marker_count = int(slider_range / self.step)
    else:
      marker_count = slider_range
    for i in range(marker_count + 1):
      marker = document.createElement('span')
      marker.classList.add('anvil-m3-slider-marker')
      markers_container.appendChild(marker)
  
  @property
  def show_markers(self):
    return self._props.get('show_markers')

  @show_markers.setter
  def show_markers(self, value):
    self._props['show_markers'] = value
    if value:
      self._set_markers()
    else:
      self.dom_nodes["anvil-m3-slider-markers-container"].innerHTML = ''

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    self.dom_nodes['anvil-m3-slider-track-container'].style.width = self._get_track_width()