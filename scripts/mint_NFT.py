from web3 import Web3
import json
from config.config import GANACHE_URL, CONTRACT_ADDRESS

def mint_nft(image_data, recipient_address, private_key):

    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    print("Connected:", w3.is_connected())

    with open("contracts/GameToken_contract.json", "r") as f:
        contract_data = json.load(f)

    nft_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_data["abi"])


    tx = nft_contract.functions.mintNFT(image_data).build_transaction({
        "from": recipient_address,
        "nonce": w3.eth.get_transaction_count(recipient_address),
        "gasPrice": w3.to_wei("50", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"NFT minted! TX Hash: {tx_hash.hex()}")
