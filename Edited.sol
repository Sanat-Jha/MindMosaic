// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DreamToken is ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;
    
    struct Dream {
        string description;
        string category;
        address dreamer;
    }
    
    mapping(uint256 => Dream) public dreams;
    mapping(string => bool) public validCategories;

    event DreamMinted(uint256 indexed tokenId, address indexed dreamer, string category);

    constructor() ERC721("DreamToken", "DREAM") {
        // Predefined categories
        validCategories["Lucid"] = true;
        validCategories["Nightmare"] = true;
        validCategories["Fantasy"] = true;
        validCategories["Prophetic"] = true;
        validCategories["Recurring"] = true;
    }

    function mintDream(string memory _description, string memory _category, string memory _tokenURI) external {
        require(validCategories[_category], "Invalid dream category");
        
        uint256 tokenId = _nextTokenId;
        _nextTokenId++;
        
        _mint(msg.sender, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        
        dreams[tokenId] = Dream(_description, _category, msg.sender);
        
        emit DreamMinted(tokenId, msg.sender, _category);
    }

    function addCategory(string memory _category) external onlyOwner {
        validCategories[_category] = true;
    }

    function removeCategory(string memory _category) external onlyOwner {
        validCategories[_category] = false;
    }

    function getDream(uint256 tokenId) external view returns (Dream memory) {
        require(_exists(tokenId), "Dream does not exist");
        return dreams[tokenId];
    }
}
