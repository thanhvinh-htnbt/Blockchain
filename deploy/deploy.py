from web3 import Web3
import json
from config import PRIVATE_KEY, GANACHE_URL, CONTRACT_ADDRESS, RECIPIENT_ADDRESS

# Kết nối Ganache
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
print("Connected:", w3.isConnected())

account = w3.eth.account.from_key(PRIVATE_KEY)

# Load ABI từ file (export từ Remix)
with open("contracts/MyNFT_contract.json", "r") as f:
    contract_data = json.load(f)

# Deploy contract
contract = w3.eth.contract(abi=contract_data["abi"], bytecode=contract_data["bytecode"])
tx = contract.constructor().buildTransaction({
    "from": account.address,
    "nonce": w3.eth.getTransactionCount(account.address),
    "gas": 2000000,
    "gasPrice": w3.toWei("50", "gwei")
})

signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"Contract deployed! TX Hash: {tx_hash.hex()}")

contract_address = w3.eth.get_transaction_receipt(tx_hash)["contractAddress"]
print(f"Deployed at: {contract_address}")
