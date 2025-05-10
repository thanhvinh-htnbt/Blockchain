from web3 import Web3
import json
from config.config import PRIVATE_KEY, GANACHE_URL, CONTRACT_ADDRESS, RECIPIENT_ADDRESS

def mint_nft(image_data):

    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    print("Connected:", w3.is_connected())

    with open("contracts/GameToken_contract.json", "r") as f:
        contract_data = json.load(f)

    nft_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_data["abi"])


    tx = nft_contract.functions.mintNFT(RECIPIENT_ADDRESS, image_data).build_transaction({
        "from": RECIPIENT_ADDRESS,
        "nonce": w3.eth.get_transaction_count(RECIPIENT_ADDRESS),
        "gas": 200000,
        "gasPrice": w3.to_wei("50", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"NFT minted! TX Hash: {tx_hash.hex()}")