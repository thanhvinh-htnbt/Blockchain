// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
contract GameToken is ERC721URIStorage {
    uint256 public tokenCounter;

    mapping(address => string[]) public encryptedImages;
    mapping(address => bool) public isPlayer;


    event PlayerCreated(address indexed player);
    event NFTMinted(address indexed to, uint256 tokenId, string tokenURI);
    event ItemPurchased(address indexed to, string tokenURI);
    event RewardSent(address indexed to, uint256 amount);

    constructor () ERC721("GameToken", "GT") {
        tokenCounter = 0;
    }


    function reward(address player, uint256 amount) public {
        payable(player).transfer(amount);
        emit RewardSent(player, amount);
    }


    function getImageCount(address user) public view returns (uint256) {
        return encryptedImages[user].length;
    }

    function getEncryptedImage(address user, uint index) public view returns (string memory) {
        require(index < encryptedImages[user].length, "Invalid index");
        return encryptedImages[user][index];
    }

    function mintNFT(string memory tokenURI) public returns (uint256) {

        uint256 newItemId = tokenCounter;
        _mint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);

        tokenCounter++;

        emit NFTMinted(msg.sender, newItemId, tokenURI);
        emit ItemPurchased(msg.sender, tokenURI);
        return newItemId;
    }

    receive() external payable {}
}
