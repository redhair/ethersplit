// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract RandomSpell is ERC721 {
    uint256 public tokenCounter;

    enum Spell{HASTE, TIME_STOP, MAZE, EVENT_HORIZON, SINGULARITY}

    mapping(uint256 => Spell) public tokenIdToSpell;
    mapping(uint256 => uint256) public tokenIdToEdition;
    
    event Log(address owner, uint256 randomNumber);
    
    constructor()
    ERC721("RandomSpell", "RNGS")
    {
        tokenCounter = 0;
    }

    function createSpell(address owner, uint256 amount, uint256 randomNumber) 
        external {
            require(msg.sender == address(0x82a29BFDb765860FA50063607674493c53c44366), "Only authorized contracts can call this function");
            emit Log(owner, randomNumber);
            uint256 randomSeed = randomNumber;
            for (uint256 i = 0; i < amount; i++) {
                uint256 newItemId = tokenCounter;
                _safeMint(owner, newItemId);
                // _setTokenURI(newItemId, tokenURI);
                Spell spell = Spell(randomSeed % 5);
                uint256 edition = 1;
                tokenIdToSpell[newItemId] = spell;
                tokenIdToEdition[newItemId] = edition;
                tokenCounter = tokenCounter + 1;
                randomSeed = uint256(keccak256(abi.encodePacked(randomSeed, blockhash(block.number - 1))));
            }
    }
}
