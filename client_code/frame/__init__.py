from ._anvil_designer import frameTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.js
from anvil.js.window import ethers
class frame(frameTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  def refresh(self):
    if get_open_form().wc.signer is None:
      pass
    else:
      self.gofurs_contract = ethers.Contract(get_open_form().gofurs_address, get_open_form().gofurs_abi, get_open_form().wc.provider)
      self.nft_ids = self.get_nft_ids(get_open_form().wc.address)
      for id in self.nft_ids:
        self.add_component(Label(text=id))
  def event_query(self, event_name, args, from_block = 0, to_block = "latest"):
    
    event_filter = self.gofurs_contract.filters[event_name](*args)
    logs = self.gofurs_contract.queryFilter(event_filter, from_block, to_block)
    processed_logs = [log.args for log in logs]  # Replace with your own logic if necessary
        
    return processed_logs
  def get_nft_ids(self, address):
    zero_addr ='0x0000000000000000000000000000000000000000'
    mints = self.event_query("Transfer",  [zero_addr, address, None])
    burns = self.event_query("Transfer", [address, zero_addr, None])
    minted_ids = set([int(i[2].toString()) for i in mints])
    burnt_ids = set([int(i[2].toString()) for i in burns])
    remaining = []
    for m in minted_ids:
      if m not in burnt_ids:
        remaining.append(m)    
    return remaining

    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    
    self.refresh()
