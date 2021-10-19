// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract Weapon is ERC721 {
    uint256 public tokenCounter;

    enum Grade{IRON, OBSIDIAN, MITHRIL, DIAMOND, MYSTICAL}
    enum Type{SWORD, BOW}

    mapping(uint256 => Grade) public tokenIdToGrade;
    mapping(uint256 => Type) public tokenIdToType;
    mapping(uint256 => uint256) public tokenIdToEdition;
    
    event Log(address owner, uint256 randomNumber);
    
    constructor()
    ERC721("EtherscapeWeapon", "ESW")
    {
        tokenCounter = 0;
    }

    function createWeapon(address owner, uint256 amount, uint256 randomNumber) 
        external {
            require(msg.sender == address(0x82a29BFDb765860FA50063607674493c53c44366), "Only authorized contracts can call this function");
            emit Log(owner, randomNumber);
            uint256 randomSeed = randomNumber;
            for (uint256 i = 0; i < amount; i++) {
                uint256 newItemId = tokenCounter;
                _safeMint(owner, newItemId);
                // _setTokenURI(newItemId, tokenURI);
                Grade grade = Grade(randomSeed % 5);
                Type t = Type(randomSeed % 2);
                uint256 edition = 1;
                tokenIdToGrade[newItemId] = grade;
                tokenIdToType[newItemId] = t;
                tokenIdToEdition[newItemId] = edition;
                tokenCounter = tokenCounter + 1;
                randomSeed = uint256(keccak256(abi.encodePacked(randomSeed, blockhash(block.number - 1))));
            }
    }
}
