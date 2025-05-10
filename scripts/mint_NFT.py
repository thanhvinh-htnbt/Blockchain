from web3 import Web3
import base64
from solcx import compile_source, install_solc
import json
from config.config import PRIVATE_KEY, GANACHE_URL, CONTRACT_ADDRESS, RECIPIENT_ADDRESS

def mint_nft(image_path):
    # Kết nối Ganache
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    print("Connected:", w3.is_connected())
    
    # Load Smart Contract từ chuỗi
    with open("contracts/GameToken.sol", "r") as file:
        source_code = file.read()

    # Đọc ABI contract
    compiled = compile_source(source_code, solc_version="0.8.0")
    contract_id, contract_interface = compiled.popitem()

    abi = contract_interface['abi']

    nft_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

    # Đọc và mã hóa ảnh
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        image_data_uri = f"data:image/jpeg;base64,{encoded_string}"

    # Tạo giao dịch mint NFT
    tx = nft_contract.functions.mintNFT(RECIPIENT_ADDRESS, image_data_uri).build_transaction({
        "from": RECIPIENT_ADDRESS,
        "nonce": w3.eth.get_transaction_count(RECIPIENT_ADDRESS),
        "gas": 2000000,
        "gasPrice": w3.to_wei("50", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"NFT minted! TX Hash: {tx_hash.hex()}")