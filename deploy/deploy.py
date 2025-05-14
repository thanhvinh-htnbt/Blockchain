import json
from web3 import Web3
from solcx import compile_source, install_solc

def deploy():

    with open("../config/config.json", "r") as f:
        config = json.load(f)

    ganache_url = config["GANACHE_URL"]

    # Cài đặt compiler (chạy 1 lần)
    install_solc("0.8.1")

    # Kết nối Ganache
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    if w3.is_connected():
        print("Connected to Ganache")
    else:
        print("Not connected")

    server = w3.eth.accounts[0]

    # Load ABI và bytecode từ file JSON (do Remix hoặc solc CLI tạo ra)
    with open("../contracts/GameToken_contract.json", "r") as f:
        contract_data = json.load(f)

    abi = contract_data["abi"]
    bytecode = contract_data["bytecode"]

    # Triển khai contract
    GameToken = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = GameToken.constructor().transact({"from": server})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    print("Contract đã được triển khai tại:", contract_address)

    config["CONTRACT_ADDRESS"] = contract_address

    with open("../config/config.json", "w") as f:
        json.dump(config, f, indent=4)


    # Trả về các đối tượng cần thiết
    contract = w3.eth.contract(address=contract_address, abi=abi)
    return w3, contract, server

