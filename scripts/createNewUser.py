from web3 import Web3
from eth_account import Account

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Kiểm tra kết nối
print("Kết nối thành công:", w3.is_connected())

server_account = w3.eth.accounts[0]
print("Server account:", server_account)
print("Server account balance:", w3.eth.get_balance(server_account))

#write to file
with open("accounts.txt", "w") as f:
    f.write(server_account + "\n")
    f.write("add server private key" + "\n")

for i in range(5):
    # Tạo tài khoản mới
    new_account = w3.eth.account.create()
    print("New account address:", new_account.address)
    print("New account private key:", new_account.key.hex())

    # Ghi thông tin tài khoản vào file
    with open("accounts.txt", "a") as f:
        f.write(new_account.address + "\n")
        f.write(new_account.key.hex() + "\n")


#Dùng ganache UI để tạo trước network với 1 tài khoản gồm 10000 ether
#sau đó chạy file này để thêm tài khoản vào mạng, lưu lại address và private key
# Những tài khoản này sẽ không hiển thị trên ganache UI nên cần đọc file accounts.txt để lấy

# address = "0xD735097671EcbA0ECEf5F11F4Ce44adDa5bAc6Ec"
# print ("Address:", address)
# print ("Balance:", w3.eth.get_balance(address))