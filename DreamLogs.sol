// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract DreamLog {
    struct DreamEntry {
        string dreamText;
        uint256 timestamp;
    }

    mapping(address => DreamEntry[]) private userDreams;

    event DreamLogged(address indexed user, string dreamText, uint256 timestamp);

    function logDream(string memory _dreamText) public {
        require(bytes(_dreamText).length > 0, "Dream text cannot be empty");
        userDreams[msg.sender].push(DreamEntry(_dreamText, block.timestamp));
        emit DreamLogged(msg.sender, _dreamText, block.timestamp);
    }

    function getMyDreams() public view returns (DreamEntry[] memory) {
        return userDreams[msg.sender];
    }

    function getDreamCount(address user) public view returns (uint256) {
        return userDreams[user].length;
    }
}