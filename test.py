import subprocess
import time
from web3 import Web3
from eth_account import Account

# Khóa riêng (64 ký tự hex, KHÔNG có "0x")
PRIVATE_KEY_1 = "115369ac1f42677a844abaf8da731d29505a61dbb98aca7531ae6e5859fa75d1"  # Server
PRIVATE_KEY_2 = "fde4d5305079b75e5c00e46bb5f169d820cc4bf3e2015cd74063743217cc9d32"  # Player

from web3 import Web3

PRIVATE_KEY_1 = "115369ac1f42677a844abaf8da731d29505a61dbb98aca7531ae6e5859fa75d1"
account_1 = Web3().eth.account.from_key(PRIVATE_KEY_1)
print("📬 Address 1:", account_1.address)

# Chuyển sang địa chỉ
ADDR_1 = Account.from_key(PRIVATE_KEY_1).address
ADDR_2 = Account.from_key(PRIVATE_KEY_2).address

# In thông tin
print("🔑 Địa chỉ PRIVATE_KEY_1 (Server):", ADDR_1)
print("🔑 Địa chỉ PRIVATE_KEY_2 (Player):", ADDR_2)

# Số dư khởi tạo (1 triệu ETH)
balance_1 = 10**6 * 10**18  # 1 triệu ETH (server)
balance_2 = 0               # 0 ETH (player)

# Đường dẫn tới ganache-cli (thay đổi nếu cài ở nơi khác)
ganache_path = "C:\\Users\\Vinh\\AppData\\Roaming\\npm\\ganache-cli.cmd"

# Khởi động Ganache CLI
print("🚀 Đang khởi động Ganache CLI...")
ganache_proc = subprocess.Popen([
    ganache_path,
    "--accounts", "0",  # không tạo account ngẫu nhiên
    f"--account={PRIVATE_KEY_1},{balance_1}",
    f"--account={PRIVATE_KEY_2},{balance_2}",
    "--port", "7545"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)




# Chờ ganache khởi động
time.sleep(3)

# Kết nối Web3
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if web3.is_connected():
    print("✅ Ganache đã khởi động thành công!\n")

    accounts = web3.eth.accounts
    print("📋 Danh sách tài khoản trong Ganache:")
    for acc in accounts:
        balance = web3.eth.get_balance(acc)
        print(f"  🧾 {acc} có {web3.from_wei(balance, 'ether')} ETH")

    print("\n🔍 Kiểm tra tài khoản được cấp ETH:")
    bal1 = web3.eth.get_balance(ADDR_1)
    bal2 = web3.eth.get_balance(ADDR_2)

    print(f"✅ Server ({ADDR_1}) có {web3.from_wei(bal1, 'ether')} ETH")
    print(f"✅ Player ({ADDR_2}) có {web3.from_wei(bal2, 'ether')} ETH")

    if web3.from_wei(bal1, 'ether') != 1_000_000:
        print("❌ Server KHÔNG được cấp đúng 1 triệu ETH!")
else:
    print("❌ Không thể kết nối tới Ganache.")
