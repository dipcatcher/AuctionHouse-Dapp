from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random

class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.start = self.item['start']
    self.end = self.item['end']
    self.contract = self.item['contract']
    self.outlined_button_1.text  = (self.start, self.end)
    self.candidates = app_tables.exclude.get(chain=self.item['chain'], cohort=self.start)
    if self.candidates is None:
      pass
    else:
      self.possible = self.candidates['exclude']
      #self.outlined_button_1.enabled=False
    
    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    event_args['sender'].enabled=False
    count = 0
    m=[]
    for n in range(self.start, self.end):
      if n in self.possible:
        try:
          a = self.contract.ownerOf(n)
          m.append(n)
          count = len(m)
          if self.item['chain']=='Ethereum':
            options = app_tables.frames.search(eth_id=None)
            selection = random.choice(list(options))
            #selection.update(eth_id=n)
          if self.item['chain']=='PulseChain':
            options = app_tables.frames.search(pls_id=None)
            selection = random.choice(list(options))
            #selection.update(pls_id=n)
          if self.item['chain']=='Degen Chain':
            options = app_tables.frames.search(degen_id=None)
            selection = random.choice(list(options))
            #selection.update(degen_id=n)
          print(selection['file_name'])
          
        except Exception as e:
          print(e)
      event_args['sender'].text = "{} | {}-{} {}".format(n, self.start, self.end, count)
    #app_tables.exclude.add_row(cohort=self.start, exclude=m,chain=self.item['chain'])
    event_args['sender'].icon='fa:check'
