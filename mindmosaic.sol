// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DreamMosaic is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _dreamIds;

    struct Dream {
        uint256 dreamId;
        address dreamer;
        string dreamContent;
        uint256 timestamp;
        string[] tags;
    }

    mapping(uint256 => Dream) public dreams;
    mapping(address => uint256[]) public dreamerToDreams;

    event DreamRecorded(uint256 indexed dreamId, address indexed dreamer);
    event DreamTagsUpdated(uint256 indexed dreamId, string[] tags);

    constructor() ERC721("DreamMosaic", "DREAM") {}

    function recordDream(string memory _dreamContent, string[] memory _tags) public {
        _dreamIds.increment();
        uint256 newDreamId = _dreamIds.current();

        dreams[newDreamId] = Dream({
            dreamId: newDreamId,
            dreamer: msg.sender,
            dreamContent: _dreamContent,
            timestamp: block.timestamp,
            tags: _tags
        });

        dreamerToDreams[msg.sender].push(newDreamId);
        _safeMint(msg.sender, newDreamId);

        emit DreamRecorded(newDreamId, msg.sender);
        emit DreamTagsUpdated(newDreamId, _tags);
    }

    function getDream(uint256 _dreamId) public view returns (
        uint256 dreamId,
        address dreamer,
        string memory dreamContent,
        uint256 timestamp,
        string[] memory tags
    ) {
        Dream memory dream = dreams[_dreamId];
        return (
            dream.dreamId,
            dream.dreamer,
            dream.dreamContent,
            dream.timestamp,
            dream.tags
        );
    }

    function getDreamerDreams(address _dreamer) public view returns (uint256[] memory) {
        return dreamerToDreams[_dreamer];
    }

    function getTotalDreams() public view returns (uint256) {
        return _dreamIds.current();
    }
}