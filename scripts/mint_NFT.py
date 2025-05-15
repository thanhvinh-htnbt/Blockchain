from web3 import Web3
import json

def mint_nft(image_data, user_address, private_key, price_eth):

    # Đọc config
    with open("config/config.json", "r") as f:
        config = json.load(f)

    ganache_url = config["GANACHE_URL"]
    contract_address = config["CONTRACT_ADDRESS"]

    with open("../scripts/accounts.json", "r") as f:
        accounts = json.load(f)

    server = accounts[0]
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    print("Connected:", w3.is_connected())

    with open("../contracts/GameToken_contract.json", "r") as f:
        contract_data = json.load(f)

    nft_contract = w3.eth.contract(address=contract_address, abi=contract_data["abi"])


    tx = nft_contract.functions.mintNFT(image_data).build_transaction({
        "from": user_address,
        "to": server["address"],
        "nonce": w3.eth.get_transaction_count(user_address),
        "gasPrice": w3.to_wei(price_eth, "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print(f"NFT minted! TX Hash: {tx_hash.hex()}")

     # Đợi xác nhận giao dịch
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Lấy event NFTMinted để biết tokenId
    events = nft_contract.events.NFTMinted().process_receipt(receipt)
    if not events:
        raise Exception("Không tìm thấy sự kiện NFTMinted!")

    token_id = events[0]["args"]["tokenId"]
    print(f"Mint thành công. Token ID: {token_id}")

    # Lấy lại tokenURI
    token_uri = nft_contract.functions.tokenURI(token_id).call()
    print(f"TokenURI: {token_uri}")
     
    return token_uri

