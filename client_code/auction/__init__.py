from ._anvil_designer import auctionTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js.window import ethers
import anvil.server
from ..gainful_auction import gainful_auction
class auction(auctionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.gofurs_abi = app_tables.contract_data.get(name="GOFURS")['abi']
    self.auction_name = "test"
    self.n = 0
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
    self.button_place_bid.enabled=True
    self.label_bid_history.text = "Loading Bid History..."
    self.label_bid_history.icon="_/theme/33Ho.gif"
    self.timer_1_tick()
    self.auction_data = get_open_form().get_auction_data(self.auction_name)
    self.label_balance.text = "{:.3f} GOFURS".format( self.user_data['Balance']/(10**18))
    self.label_allowance.text = "{:.3f} GOFURS".format( self.user_data['Approved']/(10**18))
    self.label_latest_bid.text = "{:.3f} GOFURS".format( self.auction_data['bidAmount']/(10**18))
    self.label_minimum_bid.text = "{:.3f} GOFURS".format( self.auction_data['nextMinimumBid']/(10**18))
    self.column_panel_error.clear()
    if self.auction_data['auctionEnded']:
      self.button_place_bid.text = "Auction Over"
      self.button_place_bid.enabled = False
    with anvil.server.no_loading_indicator:
      events = get_open_form().events_catalog("Bid")
      events.reverse()
      self.repeating_panel_2.items= events
      self.label_bid_history.text = "Bid History"
      self.label_bid_history.icon = ""
    

  def bid_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    is_approved = False
    is_balance = False
    is_valid = False
    is_enough = False
    self.is_good=False
    is_pls = False
    self.input = event_args['sender'].text
    error = ""
    e = ColumnPanel()
    if self.input in [0, None, "", " "]:
      self.input =0
    try:
      self.input_value = ethers.utils.parseUnits(str(self.input), 18)
      event_args['sender'].role = "outlined"
      is_valid=True
    except Exception as ee:
      print(dir(ee))
      print(ee.original_error.message)
      
      e.add_component(Label(text="Invalid number entry. ", font_size=10, foreground='red', role='body'))
    val = int(self.input_value.toString())
    if  val > self.user_data['Approved']:
      self.button_set_approval.role = 'outlined-button'
      is_approved = False
      t="You must approve the contract to interact with your GOFURS. "
      e.add_component(Label(text=t, font_size=10, foreground='red', role='body'))
      self.button_set_approval_click(sender=self.button_set_approval)
    else:
      self.button_set_approval.role = None
      is_approved=True
    if val >self.user_data['Balance']:
      self.button_buy_gofurs.role = 'outlined-button'
      t= "You do not have that many GOFURS. "
      e.add_component(Label(text=t, font_size=10, foreground='red', role='body'))
    else:
      self.button_buy_gofurs.role = None
      is_balance=True

    if val<self.auction_data['nextMinimumBid']:
      t= "Your bid must exceed the minimum bid. "
      e.add_component(Label(text=t, font_size=10, foreground='red', role='body'))
    else:
      is_enough=True
    if get_open_form().wc.chainId not in [8008135, 369]:
      t = "You must be connected to G Chain Testnet."
      e.add_component(Label(text=t, font_size=10, foreground='red', role='body'))
    else:
      is_pls = True
    self.column_panel_error.clear()
    self.column_panel_error.add_component(e)
    self.is_good = all([is_approved, is_balance, is_valid, is_enough, is_pls])
    print(self.is_good, 'isgood')
    

  def button_set_approval_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.contract_write is None:
      alert('You must connect your wallet to the site first.')
      return False
    else:
      tb = TextBox(type='number', text=10, role ="outlined")
      cp = ColumnPanel()
      cp.add_component(Label(text="Before you can submit your bid, you must approve at least that many GOFURS to be used by the auction contract. \n\nPro Tip: To prevent having to do an approval step numerous times if you bid more than once or get outbid right before your bid transaction is broadcast, it is recommended to approve a number larger than your bid amount. This is safe to do, but for peace of mind after you are done bidding you can set the approval to zero."))
      cp.add_component(tb)
      _ = alert(cp, title="Approve Contract to Interact with GOFURS", buttons=[("Submit", True), ("Cancel", False)])
      if _:
        gofurs_address = "0x54f667dB585b7B10347429C72c36c8B59aB441cb"
        ercabi = self.gofurs_abi
       
        self.gofurs_contract_write=  ethers.Contract(gofurs_address, ercabi, get_open_form().wc.signer)
        try:
          a = anvil.js.await_promise(self.gofurs_contract_write.approve(get_open_form().c['address'], ethers.utils.parseUnits(str(tb.text), 18)))
          print(dir(a))
          a.wait()
        except Exception as e:
          alert(e)
        self.form_show()

  def info_icon_click(self, **event_args):
    alert(gainful_auction(), large=True)

  def button_place_bid_click(self, **event_args):
    """This method is called when the button is clicked"""
    if event_args['sender'].text == 'Finalize Auction':
      if self.contract_write is None:
        alert('You must connect your wallet to the site first.')
        return False
      else:
        try:
          event_args['sender'].enabled = False
          a = anvil.js.await_promise(self.contract_write.endAuction(self.auction_name))
          a.wait()
          
        except Exception as e:
          alert(e)
          event_args['sender'].enabled=True
      
        self.form_show()
    else:
      
      self.bid_input_change(sender=self.bid_input)
      print(self.is_good)
      if not self.is_good:
        return False
      if self.contract_write is None:
        alert('You must connect your wallet to the site first.')
        return False
      else:
        try:
          event_args['sender'].enabled = False
          a = anvil.js.await_promise(self.contract_write.bid(self.auction_name,self.input_value))
          a.wait()
          self.bid_input.text = None
        except Exception as e:
          alert(e)
          event_args['sender'].enabled=True
      
        self.form_show()

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    refresh = self.n>12
    a,b = get_open_form().get_remaining_auction_time(self.auction_name,refresh)
   
    self.label_time_remaining.text = b
    if a == 0:
      self.timer_1.interval=0
      self.button_place_bid.text = "Finalize Auction"
      self.bid_input.enabled=False
    self.n +=1
    if refresh:
      self.n=0
        
        
