// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
contract GameToken is ERC721URIStorage {
    address public server;

    mapping(address => string[]) public encryptedImages;
    mapping(address => bool) public isPlayer;

    uint256 public tokenCounter;

    event PlayerCreated(address indexed player);
    event ItemPurchased(address indexed player, string encrypted_image);

    
    event Transfer(address indexed from, address indexed to, uint256 amount, string reason);
    event NFTMinted(address indexed player, uint256 tokenId, string tokenURI);

    constructor () ERC721("GameToken", "GT") {
        tokenCounter = 0;
    }


    function createPlayer() public {
        require(!isPlayer[msg.sender], "Player already exists");
        isPlayer[msg.sender] = true;
        emit PlayerCreated(msg.sender);
    }

    function reward(address user, uint256 amount) public {
        uint256 price = amount;
        require(msg.sender == server, "Only server can reward");
        emit Transfer(server, user, price, "Game Win Reward");
    }

    function buyItem(address user, uint256 amount, string memory encrypted_image) public {
        uint256 price = amount;
        require(isPlayer[msg.sender], "Player not registered");


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

    function mintNFT(string memory tokenURI) public returns (uint256) {
        require(isPlayer[msg.sender], "Player not registered");

        uint256 newItemId = tokenCounter;
        _mint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);

        tokenCounter++;

        emit NFTMinted(msg.sender, newItemId, tokenURI);
        return newItemId;
    }
}
