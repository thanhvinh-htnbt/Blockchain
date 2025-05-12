# Ứng dụng của hàng NFTs và Blockchain
## 1. Set up môi trường và deploy contract
### Set up mạng lưới blockchain
- Sử dụng Ganache UI, tạo 1 workspace mới với 1 account với số dư lớn để làm server
- Chạy file `createNewUser.py` để tạo ra 5 user trong mạng lưới với các **address** và **private** key lưu trữ trong `accounts.json`
- Lưu ý là các tài khoản tạo mới sẽ có balance = 0;
### Deploy contract
- Cài đặt thư viện remixd:
```python
npm install -g @remix-project/remixd
```
- Chạy lệnh để kết nối với remixd IDE trên trình duyệt
```
remixd -s . --remix-ide https://remix.ethereum.org
```
- Mở trang web của remixd: https://remix.ethereum.org/ > **connect to local Filesystem**
- Chọn thư mục `contracts/GameToken.sol`
- Chọn tab `Solidity compiler` > chọn `EVM london` > `compile`
- Đổi sang tab `deploy & run transaction` > Enviroment: `Dev - Ganache Provider` > Đổi sang cổng `http://127.0.0.1:7545` > Deploy
- Contract sẽ được lưu và hiển thị thành 1 block trên Ganache UI
- Vào file config.py thay đổi giá trị của `CONTRACT_ADDRESS`