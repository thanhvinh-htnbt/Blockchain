from web3 import Web3
import json
from config.config import GANACHE_URL, CONTRACT_ADDRESS

def mint_nft(image_data, user_address, private_key, price_eth):

    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    print("Connected:", w3.is_connected())

    with open("contracts/GameToken_contract.json", "r") as f:
        contract_data = json.load(f)

    nft_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_data["abi"])


    tx = nft_contract.functions.mintNFT(image_data).build_transaction({
        "from": user_address,
        "nonce": w3.eth.get_transaction_count(user_address),
        "gasPrice": w3.to_wei(price_eth, "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Tìm sự kiện NFTMinted để lấy tokenId
    events = nft_contract.events.NFTMinted().process_receipt(tx_receipt)
    if events:
        token_id = events[0]["args"]["tokenId"]
        print(f"Mint thành công. Token ID: {token_id}")
        return token_id
    else:
        print("Không tìm thấy sự kiện NFTMinted.")
        return None
