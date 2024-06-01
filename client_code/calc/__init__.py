from ._anvil_designer import calcTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class calc(calcTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.contract = properties['contract']
    self.id_deadline = int(self.contract.minted().toString())
    self.label_1.text = properties['name']
    a=  app_tables.exclude.search(chain=properties['name'])
    ids = []
    for _ in a:
      ids+=_['exclude']
    print(sorted(ids))
    last = 0
    n = 0
    s = 500
    groups = []
    do_run = True
    is_last = False
    while do_run:
      start = n
      end = n + s
      if end > self.id_deadline:
        end = self.id_deadline
        is_last = True
      
      groups.append({"start":start, "end":end, "contract":self.contract, "chain":self.label_1.text})
      n = end
      start = end
      do_run = not is_last
    self.repeating_panel_1.items = groups

    # Any code you write here will run before the form opens.
