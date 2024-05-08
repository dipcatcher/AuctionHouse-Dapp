from ._anvil_designer import auctionTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js.window import ethers

class auction(auctionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.address = get_open_form().wc.address
    if self.address is None:
      self.user_data = {"Balance":0, "Approved":0}
      self.contract_write = None
    else:
      self.user_data = get_open_form().get_user_data(self.address)
      self.contract_write = get_open_form().get_contract(False)
    self.refresh()
  def refresh(self):
    self.auction_data = get_open_form().get_auction_data("Saturday Morning")
    self.label_balance.text = "{:.3f} GOFURS".format( self.user_data['Balance']/(10**18))
    self.label_allowance.text = "{:.3f} GOFURS".format( self.user_data['Approved']/(10**18))
    self.label_latest_bid.text = "{:.3f} GOFURS".format( self.auction_data['bidAmount']/(10**18))
    self.label_minimum_bid.text = "{:.3f} GOFURS".format( self.auction_data['nextMinimumBid']/(10**18))
    

  def bid_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    is_approved = False
    is_balance = False
    is_valid = False
    is_enough = False
    self.input = event_args['sender'].text
    error = ""
    if self.input in [0, None, "", " "]:
      self.input =0
    try:
      self.input_value = ethers.utils.parseUnits(str(self.input), 18)
      event_args['sender'].role = "outlined"
      is_valid=True
    except Exception as e:
      print(dir(e))
      print(e.original_error.message)
      error+="Invalid number entry. "
    val = int(self.input_value.toString())
    if  val > self.user_data['Approved']:
      self.button_set_approval.role = 'filled-button'
      is_approved = False
      error +="You must approve the contract to interact with your GOFURS. "
    else:
      self.button_set_approval.role = None
      is_approved=True
    if val >self.user_data['Balance']:
      self.button_buy_gofurs.role = 'filled-button'
      error += "You do not have that many GOFURS. "
    else:
      self.button_buy_gofurs.role = None
      is_balance=True

    if val<self.auction_data['nextMinimumBid']:
      error += "Your bid must exceed the minimum bid. "
    else:
      is_enough=True
    self.button_place_bid.enabled = all([is_approved, is_balance, is_valid, is_enough])
    if self.button_place_bid.enabled:
      self.label_error.visible=False
    else:
      self.label_error.visible = True
      self.label_error.text = error
      self.label_error.foreground='red'
      self.label_error.font_size=9
      self.label_error.italic=True

  def button_set_approval_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.contract_write is None:
      alert('You must connect your wallet to the site first.')
      return False
    else:
      tb = TextBox(type='number', text=100, role ="outlined")
      cp = ColumnPanel()
      cp.add_component(Label(text="To prevent having to do an approval step numerous times if you bid more than once or get outbid right before your bid transaction is broadcast, it is recommended to approve a large number. This is safe to do, but for peace of mind after you are done bidding you can set the approval to zero."))
      cp.add_component(tb)
      _ = alert(cp, title="Approve Contract to Interact with GOFURS", buttons=[("Submit", True), ("Cancel", False)])
      if _:
        gofurs_address = "0x54f667dB585b7B10347429C72c36c8B59aB441cb"
        ercabi = app_tables.contract_data.get(name="erc20")['abi']
        self.gofurs_contract_write=  ethers.Contract(gofurs_address, ercabi, get_open_form().wc.signer)
        try:
          a = anvil.js.await_promise(self.gofurs_contract_write.approve(get_open_form().c['address'], ethers.utils.parseUnits(str(tb.text), 18)))
          print(dir(a))
          a.wait()
        except Exception as e:
          alert(e)
        self.form_show()

  def info_icon_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
        
