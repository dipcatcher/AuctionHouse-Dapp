from ._anvil_designer import nft_displayTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class nft_display(nft_displayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.data = properties['data']
    self.is_clickable = properties['is_clickable']
    self.role = ['elevated-card']
  def refresh(self):
    self.image.source=self.data['Metadata']['image']
    self.label_attributes_name.text = self.data['Metadata']['attributes'][0]['value']
    self.label_name.text = self.data['Metadata']['name']
    self.label_owner.text = "{}...{}".format( self.data['owner'][0:4], self.data['owner'][-4:])
    
    # Any code you write here will run before the form opens.

  def image_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    if self.is_clickable:
      c = nft_display(data= self.data, is_clickable=False)
      
      alert(c, large=True)

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.refresh()

    # Any code you write here will run before the form opens.
