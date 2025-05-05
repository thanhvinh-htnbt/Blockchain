from web3 import Web3
import json
from config import PRIVATE_KEY, GANACHE_URL, CONTRACT_ADDRESS, RECIPIENT_ADDRESS

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))


with open("contracts/MyNFT_abi.json", "r") as f:
    abi = json.load(f)

nft_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)


tx = nft_contract.functions.mintNFT(RECIPIENT_ADDRESS).buildTransaction({
    "from": RECIPIENT_ADDRESS,
    "nonce": w3.eth.getTransactionCount(RECIPIENT_ADDRESS),
    "gas": 200000,
    "gasPrice": w3.toWei("50", "gwei")
})

signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"NFT minted! TX Hash: {tx_hash.hex()}")