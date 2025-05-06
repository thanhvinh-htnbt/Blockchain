// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GameToken {
    address public owner;
    mapping(address => uint256) public balances;
    mapping(address => string[]) public encryptedImages;

    event Transfer(address from, address to, uint256 amount, string reason);

    event ItemPurchased(address player, string encrypted_image);

    constructor() {
        owner = msg.sender;
        balances[owner] = 1_000_000 * 10**18;
    }

    function createUser(address user) public {
        require(msg.sender == owner, "Only server can create users");
        balances[user] = 0;
    }

    function reward(address user, uint256 amount) public {
        require(msg.sender == owner, "Only server can reward");
        require(balances[owner] >= amount, "Insufficient server balance");
        balances[owner] -= amount;
        balances[user] += amount;
        emit Transfer(owner, user, amount, "Game Win Reward");
    }

    function buyItem(address user, uint256 amount, string memory encrypted_image) public {
        require(msg.sender == user, "Only user can call this");
        require(balances[msg.sender] >= amount, "Not enough balance");
        balances[msg.sender] -= amount;
        balances[owner] += amount;

        encryptedImages[msg.sender].push(encrypted_image);
        emit Transfer(msg.sender, owner, amount, "Buy Item");
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
