// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
contract GameToken is ERC721URIStorage {
    uint256 public tokenCounter;

    event NFTMinted(address indexed owner, uint256 indexed tokenId);

    constructor () ERC721("GameToken", "GT") {
        tokenCounter = 0;
    }


    function mintNFT(string memory tokenURI) public payable returns (uint256) {

        uint256 newItemId = tokenCounter;
        _mint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);
        emit NFTMinted(msg.sender, newItemId);  
        tokenCounter++;
        return newItemId;
    }

    receive() external payable {}
}

