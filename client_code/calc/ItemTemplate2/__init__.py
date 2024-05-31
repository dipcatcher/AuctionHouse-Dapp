from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.start = self.item['start']
    self.end = self.item['end']
    self.contract = self.item['contract']
    self.outlined_button_1.text  = (self.start, self.end)

    # Any code you write here will run before the form opens.
