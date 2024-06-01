import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import time
from web3 import Web3

# Initialize the web3 connection (replace with your provider)

web3 = Web3(Web3.HTTPProvider("https://0d91-2601-283-4c00-c7b0-1c4b-dec2-95db-6e51.ngrok-free.app/"))

# Function to load contract ABI and address from your data table
def get_contract_data(name):
    # Implement your method to retrieve the contract data
    # Example: app_tables.contracts.get(name=name)
    
    contract_data = app_tables.contract_data.get(name=name)
    return contract_data['abi'], contract_data['address']

# Function to create a contract object
def get_contract(name):
    abi, address = get_contract_data(name)
    return web3.eth.contract(address=address, abi=abi)


def run_nft_map():
  return anvil.server.launch_background_task('nft_map')
@anvil.server.background_task
def nft_map():
  frames_contract = get_contract("frames")
  
  
  max_id = int(frames_contract.functions.ID_DEADLINE().call())
  n = 0
  
  while n< max_id:
    
    t = anvil.server.launch_background_task('check_batch', n, n+500)
    app_tables.exclude.add_row(cohort=n, task_id = t.get_id())
    
    n+=500
  anvil.server.task_state = "DONE"
  
  
@anvil.server.background_task
def check_batch(a,b):
  m = []
  x = []
  gofurs_contract = get_contract("GOFURS")
  for n in range(a,b):
      try:
          owner = gofurs_contract.functions.ownerOf(n).call()
          print(owner)
          m.append(n)
      except Exception as e:
          x.append(n)
  app_tables.exclude.get(cohort=a).update(exclude=x)
  