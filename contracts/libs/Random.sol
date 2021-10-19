pragma solidity ^0.8.0;

contract Random {
  uint256 _seed;

  function random256() public returns (uint256) {
    _seed = uint256(keccak256(abi.encodePacked(_seed, blockhash(block.number - 1))));
    return _seed;
  }

  function random(uint256 upperBound) public returns (uint256) {
    return random256() % upperBound;
  }
}