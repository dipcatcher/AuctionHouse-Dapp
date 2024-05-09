from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
  def refresh(self):
    self.label_address.text ="{}...{}".format(self.item['bidder'][0:4], self.item['bidder'][-4:])
    self.scan_url = "https://scan.9mm.pro/tx/{}".format(self.item['hash'])
    self.link_tx.url = self.scan_url
    self.label_1.text = "{:.4f} GOFURS".format( self.item['bid']/(10**18))
    tx_text = "1) {:.4f} GOFURS sent from Bidder to Contract\n2) {:.4f} GOFURS fee sent from Contract to Protocol\n3) {:.4f} GOFURS sent from Contract to Prior Bidder\n4) {:.4f} GOFURS sent from Contract to Auctioneer (burnt)".format(
      self.item['gofurs_transfers'][0]['amount']/(10**18), self.item['gofurs_transfers'][1]['amount']/(10**18), self.item['gofurs_transfers'][2]['amount']/(10**18), self.item['gofurs_transfers'][3]['amount']/(10**18)
    )
    
    
    self.label_transactions.text =tx_text
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    event_args['sender'].icon = 'fa:caret-down' if event_args['sender'].icon == 'fa:caret-up' else 'fa:caret-up'
    self.column_panel_1.visible = event_args['sender'].icon =='fa:caret-up'
    
