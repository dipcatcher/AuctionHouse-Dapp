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
    if app_tables.exclude.get(chain=self.item['chain'], cohort=self.start) is None:
      pass
    else:
      self.outlined_button_1.enabled=False
    
    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    event_args['sender'].enabled=False
    m=[]
    for n in range(self.start, self.end):
      try:
        a = self.contract.ownerOf(n)
        m.append(n)
        event_args['sender'].text = "{} | {}-{} {}".format(n, self.start, self.end, len(m))
      except Exception as e:
        print(e)
    app_tables.exclude.add_row(cohort=self.start, exclude=m,chain=self.item['chain'])
    event_args['sender'].icon='fa:check'
