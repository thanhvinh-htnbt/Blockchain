import json
from web3 import Web3
import os
from solcx import compile_source, install_solc, compile_standard
from pathlib import Path

def deploy():
    # Cài đặt compiler
    install_solc("0.8.20")

    # Kết nối Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    private_key = "0xde9abfbfd3af8d5f14b76f4b01bc8d27dd44b717a58ba169b7e2052c9bf73fdf"
    account = w3.eth.account.from_key(private_key)
    
    if not w3.is_connected():
        print("Not connected to Ganache")
        return

    # Sử dụng Path để xử lý đường dẫn an toàn
    base_path = Path(__file__).parent.parent
    contracts_path = base_path / "contracts" / "GameToken.sol"
    node_modules_path = base_path / "node_modules"

    # Đọc contract
    with open(contracts_path, "r", encoding="utf-8") as file:
        contract_source = file.read()

    # Chuẩn bị remappings với raw string
    remappings = [
        f"@openzeppelin/={str(node_modules_path / '@openzeppelin').replace(' ', '_')}/"
    ]

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "GameToken.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "remappings": remappings,
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    }, solc_version="0.8.20")

    # Lấy bytecode và ABI
    bytecode = compiled_sol["contracts"]["GameToken.sol"]["GameToken"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["GameToken.sol"]["GameToken"]["abi"]

    # Deploy contract
    GameToken = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    construct_txn = GameToken.constructor(account.address).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 3000000,
        "gasPrice": w3.eth.gas_price,
        "chainId": 1337
    })
    
    try:
        signed_txn = account.sign_transaction(construct_txn)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")
        
        with open("contract_info.json", "w") as file:
            json.dump({
                "address": tx_receipt.contractAddress,
                "abi": abi
            }, file)
            
        return tx_receipt.contractAddress, abi
        
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        return None



def create_player(w3, contract, server):
    # Tạo user mới
    user = w3.eth.accounts[1]
    tx = contract.functions.createPlayer().transact({'from': user})
    w3.eth.wait_for_transaction_receipt(tx)

    return user

def reward(w3, contract, server, user, amount):
    # Server gửi coin cho user
    tx = contract.functions.reward(user, amount).transact({'from': server})
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt


def buy_item(w3, contract, user, amount, encrypted_image):
    # Player mua item
    tx = contract.functions.buyItem(user, amount, encrypted_image).transact({'from': user})
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt

def get_user_image_count(w3, contract, user):
    # Lấy số lượng ảnh của user
    count = contract.functions.getImageCount(user).call()
    return count

def get_image_cipher(w3, contract, user, index):
    # Lấy cipher của ảnh
    cipher = contract.functions.getEncryptedImage(user, index).call()
    return cipher
    
def get_user_balance(w3, contract, user):
    balance = contract.functions.getBalance(user).call()
    return balance 

deploy()

