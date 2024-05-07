from ._anvil_designer import _homeTemplate
from anvil import *
import anvil.server
from ..auction import auction
class _home(_homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.menu_click(sender=self.link_auction)
    # Any code you write here will run before the form opens.
  def menu_click(self, **event_args):
    self.content_panel.clear()
    self.target = event_args['sender']
    if self.target==self.link_auction:
      self.page = auction()
    self.content_panel.add_component(self.page)
    
  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('About')

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')
