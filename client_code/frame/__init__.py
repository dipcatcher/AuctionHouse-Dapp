from ._anvil_designer import frameTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
import anvil.js
from anvil.js.window import ethers
from ..nft_display import nft_display
class frame(frameTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  def refresh(self):
    if get_open_form().wc.address is None:
      alert('Connect your wallet!')
    else:
      
      
      self.gofurs_contract = ethers.Contract(get_open_form().gofurs_address, get_open_form().gofurs_abi, get_open_form().wc.provider)
      address = get_open_form().wc.address
      self.nft_ids = self.get_nft_ids(address)
      
      self.nft_data= []
      if len(self.nft_ids) == 0:
        self.column_panel_eligible.visible=True
      for id in self.nft_ids:
        _ = {"ID":id, "owner":address}
        
        #data_uri = self.gofurs_contract.tokenURI(id)
        
        #json_part = data_uri.split(",", 1)[1]
        #metadata_dict = json.loads(json_part)
        #_["Metadata"]=metadata_dict
        self.nft_data.append(_)
      
      r = 1
      per_row=3
      b = 0
      for n in self.nft_data:
        self.grid_panel.add_component(nft_display(data=n, is_clickable=True),
                  row=str(r), col_xs=b*12/per_row, width_xs=12/per_row)
        if b<per_row-1:
          b+=1
        else:
          b=0
          r+=1
        
      
  def event_query(self, event_name, args, from_block = 0, to_block = "latest"):
    
    event_filter = self.gofurs_contract.filters[event_name](*args)
    if get_open_form().wc.chainId==666666666:
      print("degen")
      from_block = 1239792 
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

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().wc.link_1_click(sender=get_open_form().wc.link_1)
