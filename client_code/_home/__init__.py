from ._anvil_designer import _homeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..auction import auction
from ..frame import frame
from anvil.js.window import ethers
import datetime
from datetime import timedelta, timezone
class _home(_homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    self.c =  app_tables.contract_data.get(name='series')
    url = app_tables.wallet_chains.get(chainId=8008135)['rpcUrl']
    self.provider = ethers.providers.JsonRpcProvider(url)
    self.contract = self.get_contract()
    gofurs_address = "0x54f667dB585b7B10347429C72c36c8B59aB441cb"
    ercabi = app_tables.contract_data.get(name="GOFURS")['abi']
    self.gofurs_abi = ercabi
    self.gofurs_contract=  ethers.Contract(gofurs_address, ercabi, self.provider)
    self.latest = self.link_auction
    self.elogs = []
    self.setup_event_listener()
    print("ok")
    self.refresh()
    print("yea")
  def refresh(self):
    try:
      self.auction_data = self.get_auction_data("test")
      self.menu_click(sender=self.latest)
    except:
      self.menu_click(sender=self.link_auction)
    
    # Any code you write here will run before the form opens.
  def menu_click(self, **event_args):
    self.content_panel.clear()
    self.target = event_args['sender']
    if self.target==self.link_auction:
      self.page = auction()
    if self.target == self.link_frame:
      self.page = frame()
    self.content_panel.add_component(self.page)
    self.latest = self.target
  
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
    data = []
    for log in logs:
      d = {}
      d['hash']=log['transactionHash']
      d['bidder']=log.args[1]
      d['bid']=int(log.args[2].toString())
      d['timestamp']=int(log.args[3].toString())
      d['datetime']=datetime.datetime.fromtimestamp(d['timestamp'])
      data.append(d)
      tx = get_open_form().provider.getTransaction(d['hash'])
      contractAbi = self.c['abi']
      iface = ethers.utils.Interface(contractAbi)
      parsedTx = iface.parseTransaction({"data": tx.data})
      giface = ethers.utils.Interface(self.gofurs_abi)
      txReceipt = self.provider.getTransactionReceipt(d['hash'])
      #print(txReceipt)
      events = txReceipt.logs
      transfers = []
      for e in events:
        try:
          ev = giface.parseLog(e)
          eventArgs = 1#giface.decodeEventLog(ev.name, ev.data, ev.topics)
        
          
        except:
          ev = iface.parseLog(e)
          eventArgs = 0#iface.decodeEventLog(ev.name, ev.data, ev.topics)
        
       
        if ev.name =='ERC20Transfer':
          txdata = {}
          txdata['from']=ev.args[0]
          txdata['to']=ev.args[1]
          txdata['amount']=int(ev.args[2].toString())
          transfers.append(txdata)
      d['gofurs_transfers']=transfers
          
            
      
    
      
      
      
    return data
  def get_remaining_auction_time(self, auction_name, refresh):
    # Retrieve auction data
    if refresh:
      
      auction_data = self.get_auction_data(auction_name)
      auction_end_timestamp = auction_data['auctionEndTimestamp']
    
    # Get the current block timestamp from the blockchain
      current_block = self.provider.getBlock("latest")
      current_timestamp = current_block['timestamp']
    else:
      auction_end_timestamp=self.auction_data['auctionEndTimestamp']
      now = datetime.datetime.now(timezone.utc)
  
      # Get the Unix timestamp
      unix_timestamp = int(now.timestamp())
      current_timestamp = unix_timestamp
    # Calculate remaining time in seconds
    remaining_seconds = auction_end_timestamp - current_timestamp
    
    if remaining_seconds <= 0:
        readable_time = "Auction has ended"
        remaining_seconds = 0
    else:
        # Convert remaining seconds to a readable format
        remaining_time = timedelta(seconds=remaining_seconds)
        
        # Split the remaining time into days, hours, minutes, and seconds
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Format readable time
        readable_time = f"{days}d {hours}h {minutes}m {seconds}s" if days > 0 else f"{hours}h {minutes}m {seconds}s"

    return remaining_seconds, readable_time
  def setup_event_listener(self):
    # Call ethers.js to set up event listener
 
    self.contract.on("Bid", self.handle_event)
    
    

  def handle_event(self, *eventData):
    # Handle the event data here
    self.elogs.append(eventData)
    print("Event data received: ", eventData)
    print(len(self.elogs))
    # You can update UI or trigger other actions based on the event data
  def wc_connect(self, **event_args):
    self.refresh()

      
