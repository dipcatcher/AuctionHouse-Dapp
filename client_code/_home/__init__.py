from ._anvil_designer import _homeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..auction import auction
from anvil.js.window import ethers
class _home(_homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    self.c =  app_tables.contract_data.get(name='series')
    url = "http://127.0.0.1:8545/"
    self.provider = ethers.providers.JsonRpcProvider(url)
    self.contract = self.get_contract()
    gofurs_address = "0x54f667dB585b7B10347429C72c36c8B59aB441cb"
    ercabi = app_tables.contract_data.get(name="GOFURS")['abi']
    self.gofurs_contract=  ethers.Contract(gofurs_address, ercabi, self.provider)
    self.menu_click(sender=self.link_auction)
    
    
    # Any code you write here will run before the form opens.
  def menu_click(self, **event_args):
    self.content_panel.clear()
    self.target = event_args['sender']
    if self.target==self.link_auction:
      self.page = auction()
    self.content_panel.add_component(self.page)
  
  def get_contract(self, is_read=True):
    c = self.c
    address = c['address']
    abi = c['abi']
    if is_read:
      return ethers.Contract(address, abi, self.provider)
    else:
      return ethers.Contract(address, abi, self.wc.signer)
  def get_auction_data(self, name):
    auction_data = self.contract.AUCTION_DATABASE(name)
    data = {}
    f = [
        "lastBidTimestamp",
        "firstBidTimestamp",
        "auctionEndTimestamp",
        "latestBidder",
        "bidAmount",
        "bidDifferenceSplit",
        "auctionStarted",
        "auctionEnded",
        "uriPath",
        "startingPrice",
        "auctionDurationHours",
        "extensionPeriodHours",
        "minimumBidIncrement",
        "bidToken"
    ]
    n = 0
    for i in auction_data:
      c = str(i.__class__)
      if 'umber' in c:
        v = int(i.toString())
      else:
        v = i
    
      data[f[n]] = v
      n+=1
    data['nextMinimumBid'] = data['startingPrice'] if data['bidAmount']==0 else int(data['bidAmount']*data['minimumBidIncrement']/(10000000))
    print(data)
    
    return data
  def get_user_data(self, address):
    data = {}
    data['Balance'] = int(self.gofurs_contract.balanceOf(self.wc.address).toString())
    data['Approved'] =int(self.gofurs_contract.allowance(self.wc.address, self.c['address']).toString())
    return data
  def events_catalog(self, event_name, from_block = 0, to_block = "latest"):
    abi = app_tables.contract_data.get(name='series')['abi']
    
    # TODO: return event query results of the input event_name. The event_name should be in the available events from the party_abi.
    event_names = [event['name'] for event in abi if event['type'] == 'event']
    
    if event_name not in event_names:
        raise ValueError(f"The event {event_name} is not in the ABI.")
    
    # Query the event logs
    event_filter = self.contract.filters[event_name]()
    
    logs = self.contract.queryFilter(event_filter)
    
    # Process the logs to extract useful information (if needed)
    
    processed_logs = [log.args for log in logs]  # Replace with your own logic if necessary
    iface = ethers.utils.Interface(abi)
    eventInterface = iface.getEvent(event_name)
    
    for log in processed_logs:
      print(log)
      print(log[0].hash)
      print(dir(log[0]))
      print("_____")
      
      
    return processed_logs
      
class AuctionData:
    def __init__(self, last_bid_timestamp, first_bid_timestamp, auction_end_timestamp, latest_bidder, bid_amount, bid_difference_split, auction_started, auction_ended, uri_path, starting_price, auction_duration_hours, extension_period_hours, minimum_bid_increment, bid_token):
        self.last_bid_timestamp = last_bid_timestamp
        self.first_bid_timestamp = first_bid_timestamp
        self.auction_end_timestamp = auction_end_timestamp
        self.latest_bidder = latest_bidder
        self.bid_amount = bid_amount
        self.bid_difference_split = bid_difference_split
        self.auction_started = auction_started
        self.auction_ended = auction_ended
        self.uri_path = uri_path
        self.starting_price = starting_price
        self.auction_duration_hours = auction_duration_hours
        self.extension_period_hours = extension_period_hours
        self.minimum_bid_increment = minimum_bid_increment
        self.bid_token = bid_token

    
    