import json
from web3 import Web3
from solcx import compile_source, install_solc

def deploy():

    # Cài đặt compiler (chạy 1 lần)
    install_solc("0.8.0")

    # Kết nối Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

    if w3.is_connected():
        print("Connected to Ganache")
    else:
        print("Not connected")

    server = w3.eth.accounts[0]

    # Load Smart Contract từ chuỗi
    with open("GameToken.sol", "r") as file:
        source_code = file.read()

    compiled = compile_source(source_code, solc_version="0.8.0")
    contract_id, contract_interface = compiled.popitem()

    abi = contract_interface['abi']
    bytecode = contract_interface['bin']

    # Deploy Contract
    GameToken = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = GameToken.constructor().transact({'from': server})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    print("Contract deployed at:", contract_address)

    # Tạo instance
    contract = w3.eth.contract(address=contract_address, abi=abi)

    return w3, contract, server


def create_player(w3, contract, server):
    # Tạo user mới
    user = w3.eth.accounts[1]
    tx = contract.functions.createUser(user).transact({'from': server})
    w3.eth.wait_for_transaction_receipt(tx)

    return user

def reward(w3, contract, server, user, amount):
    # Server gửi coin cho user
    tx = contract.functions.reward(user, amount * 10**18).transact({'from': server})
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt


def buy_item(w3, contract, user, amount, encrypted_image):
    # Player mua item
    tx = contract.functions.buyItem(user, amount, encrypted_image).transact({'from': user})
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt

def get_user_cipher(w3, contract, user):
    count = contract.functions.getImageCount(user).call()
    for i in range(count):
        cipher_str = contract.functions.getEncryptedImage(user, i).call()
        print(f"Item {i}: {cipher_str}")
        return cipher_str

# # Kiểm tra số dư
# balance_user = contract.functions.getBalance(user).call()
# balance_server = contract.functions.getBalance(server).call()
#
# print(f"User balance: {balance_user / 1e18}")
# print(f"Server balance: {balance_server / 1e18}")
