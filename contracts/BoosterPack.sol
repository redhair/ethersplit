// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./Character.sol";
import "./Weapon.sol";
import "./Spell.sol";
import "./libs/Random.sol";

contract BoosterPack is ERC721, Random {
    uint256 public tokenCounter;
    uint256 public edition;

    mapping(bytes32 => uint256) public requestIdToRandomNumber;
    mapping(uint256 => address) public tokenIdToSender;
    
    constructor()
    ERC721("EtherscapeStarterPack", "ESSP")
    {
        tokenCounter = 0;
    }

    function createStarterPack() 
        public {
            require(tokenCounter < 10, "No more than 10 starter packs can be minted.");
            address owner = msg.sender;
            uint256 newItemId = tokenCounter;
            _safeMint(owner, newItemId);
            tokenIdToSender[newItemId] = msg.sender;
            tokenCounter = tokenCounter + 1;
    }

    function open(uint256 tokenId, address charAddress, address weaponAddress, address spellAddress) public {
        require(tokenId < tokenCounter && tokenId >= 0, "tokenId not valid");
        require(tokenIdToSender[tokenId] != address(0x0), "Starterpack has already been opened");
        require(tokenIdToSender[tokenId] == msg.sender, "You don't own this starterpack");
        
        // generate the random number here
        uint256 randomNumber = random(777);
        
        // create the characters downstream with the random seed as a param
        // TODO seems to be a bug with creation. sometimes it fails othertimes it doesnt. No specified error
        RandomCharacter char = RandomCharacter(charAddress);
        char.createCharacter(msg.sender, 3, randomNumber);
        RandomWeapon weapon = RandomWeapon(weaponAddress);
        weapon.createWeapon(msg.sender, 3, randomNumber);
        RandomSpell spell = RandomSpell(spellAddress);
        spell.createSpell(msg.sender, 2, randomNumber);
        
        //then burn the starter pack
        _burn(tokenId);
        tokenIdToSender[tokenId] = address(0x0);
    }
}
