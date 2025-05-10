// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GameToken {
    address public server;

    mapping(address => uint256) public balances;
    mapping(address => string[]) public encryptedImages;
    mapping(address => bool) public isPlayer;

    event PlayerCreated(address indexed player);
    event ItemPurchased(address indexed player, string encrypted_image);

    event Transfer(address indexed from, address indexed to, uint256 amount, string reason);

    constructor(address _server) {
        server = _server;
        balances[server] = 1_000_000 ether;
    }


    function createPlayer() public {
        require(!isPlayer[msg.sender], "Player already exists");
        isPlayer[msg.sender] = true;
        balances[msg.sender] = 0;
        emit PlayerCreated(msg.sender);
    }

    function reward(address user, uint256 amount) public {
        uint256 price = amount;
        require(msg.sender == server, "Only server can reward");
        require(balances[server] >= price, "Insufficient server balance");
        balances[server] -= price;
        balances[user] += price;
        emit Transfer(server, user, price, "Game Win Reward");
    }

    function buyItem(address user, uint256 amount, string memory encrypted_image) public {
        uint256 price = amount;
        require(isPlayer[msg.sender], "Player not registered");
        require(balances[msg.sender] >= price, "Not enough balance");

        balances[msg.sender] -= price;
        balances[server] += price;

        encryptedImages[msg.sender].push(encrypted_image);
        emit Transfer(msg.sender, server, price, "Buy Item");
        emit ItemPurchased(msg.sender, encrypted_image);
    }

    function getImageCount(address user) public view returns (uint256) {
        return encryptedImages[user].length;
    }

    function getEncryptedImage(address user, uint index) public view returns (string memory) {
        require(index < encryptedImages[user].length, "Invalid index");
        return encryptedImages[user][index];
    }

    function getBalance(address addr) public view returns (uint256) {
        return balances[addr];
    }
}
