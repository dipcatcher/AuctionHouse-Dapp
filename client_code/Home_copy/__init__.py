from ._anvil_designer import Home_copyTemplate
from anvil import *
import anvil.server

class Home_copy(Home_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('About')

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')
