// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DreamChain {
    struct Dream {
        address dreamer;
        string ipfsHash;
        uint256 timestamp;
    }

    Dream[] public dreams;
    mapping(address => uint256[]) public userDreams;

    event DreamLogged(address indexed dreamer, string ipfsHash, uint256 timestamp);

    function submitDream(string memory _ipfsHash) public {
        dreams.push(Dream(msg.sender, _ipfsHash, block.timestamp));
        userDreams[msg.sender].push(dreams.length - 1);
        emit DreamLogged(msg.sender, _ipfsHash, block.timestamp);
    }

    
    function getDreamsByUser(address user) public view returns (Dream[] memory) {
        uint256 count = userDreams[user].length;
        Dream[] memory userDreamList = new Dream[](count);

        for (uint256 i = 0; i < count; i++) {
            userDreamList[i] = dreams[userDreams[user][i]];
        }

        return userDreamList;
    }

    function getAllDreams() public view returns (Dream[] memory) {
        return dreams;
    }
}