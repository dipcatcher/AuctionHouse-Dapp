from ._anvil_designer import nft_displayTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.js

class nft_display(nft_displayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.data = properties['data']
    self.is_clickable = properties['is_clickable']
    self.role = ['elevated-card']
    self.contract_read = self.data['contract']
  def refresh(self):
    if get_open_form().wc.chainId==1:
      row = app_tables.frames.get(eth_id=self.data['ID'])
      
      #selection.update(eth_id=n)
    if get_open_form().wc.chainId==369:
      row = app_tables.frames.get(pls_id=self.data['ID'])
      
      #selection.update(pls_id=n)
    if get_open_form().wc.chainId==666666666:
      row = app_tables.frames.get(degen_id=self.data['ID'])
    
    self.image.source=row['file']#"_/theme/Frame%20NFT%20Placeholder.png"#self.data['Metadata']['image']
    self.label_name.text = "Frame NFT ID #{}".format(self.data['ID'])
    
    self.did_claim = self.contract_read.DID_CLAIM(self.data['ID'])
   
    self.button_claim.text = "Claim NFT" if  not self.did_claim else "✅ Claimed"
    

  def image_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    if self.is_clickable:
      c = nft_display(data= self.data, is_clickable=False)
      
      alert(c, large=True)

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.refresh()

    # Any code you write here will run before the form opens.

  def button_claim_click(self, **event_args):
    if  "Claimed" in self.button_claim.text :
      return False
    else:
      self.contract_write = get_open_form().get_contract('frames', False)
      try:
        a = anvil.js.await_promise(self.contract_write.claim(self.data['ID']))
        a.wait()
      except Exception as e:
        alert(e.original_error.reason)
      self.refresh()
    
    
