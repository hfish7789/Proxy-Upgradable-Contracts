// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Box {
    uint256 public value;

    event ValueChanged(uint256 newValue, uint256 timestamp);

    function setValue(uint256 _newValue) public {
        value = _newValue;

        emit ValueChanged(_newValue, block.timestamp);
    }

    function getValue() public view returns (uint256) {
        return value;
    }
}
