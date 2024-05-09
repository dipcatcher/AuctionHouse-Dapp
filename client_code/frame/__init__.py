from ._anvil_designer import frameTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class frame(frameTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  def event_query(self, event_name, chain,args, from_block = 0, to_block = "latest"):
    
    event_filter = self.cd['GOFURS']['contract_read'][chain].filters[event_name](*args)
    logs = self.cd['GOFURS']['contract_read'][chain].queryFilter(event_filter, from_block, to_block)
    processed_logs = [log.args for log in logs]  # Replace with your own logic if necessary
        
    return processed_logs
  def get_nft_ids(self, chain, address):
    mints = self.event_query("Transfer", chain, [zero_addr, address, None])
    burns = self.event_query("Transfer", chain, [address, zero_addr, None])
    minted_ids = set([int(i[2].toString()) for i in mints])
    burnt_ids = set([int(i[2].toString()) for i in burns])
    remaining = []
    for m in minted_ids:
      if m not in burnt_ids:
        remaining.append(m)    
    return remaining

    # Any code you write here will run before the form opens.
