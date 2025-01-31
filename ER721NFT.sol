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

    event DreamMinted(uint256 indexed tokenId, address indexed dreamer, string category);

    constructor() ERC721("DreamToken", "DREAM") {}

    function mintDream(string memory _description, string memory _category, string memory _tokenURI) external {
        uint256 tokenId = _nextTokenId;
        _nextTokenId++;
        
        _mint(msg.sender, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        
        dreams[tokenId] = Dream(_description, _category, msg.sender);
        
        emit DreamMinted(tokenId, msg.sender, _category);
    }

    function getDream(uint256 tokenId) external view returns (Dream memory) {
        require(_exists(tokenId), "Dream does not exist");
        return dreams[tokenId];
    }
}
