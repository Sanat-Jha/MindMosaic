// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract DreamPools {
    struct Pool {
        string category;
        address[] members;
        string nftCID; // IPFS CID of the AI-generated NFT image
    }

    mapping(string => Pool) public dreamPools;  // category => pool
    mapping(address => string) public userDreamCategory;  // User => Category

    event PoolCreated(string category);
    event UserJoined(address user, string category);

    function joinDreamPool(string memory category) public {
        require(bytes(userDreamCategory[msg.sender]).length == 0, "Already in a pool");

        // Add user to the category pool
        dreamPools[category].members.push(msg.sender);
        userDreamCategory[msg.sender] = category;

        // Emit events
        emit UserJoined(msg.sender, category);

        // If first user, create the pool
        if (dreamPools[category].members.length == 1) {
            emit PoolCreated(category);
        }
    }

    function getPoolMembers(string memory category) public view returns (address[] memory) {
        return dreamPools[category].members;
    }

    function assignNFTtoPool(string memory category, string memory nftCID) public {
        require(dreamPools[category].members.length > 0, "No users in pool");
        dreamPools[category].nftCID = nftCID;
    }
}