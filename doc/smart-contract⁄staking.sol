// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EbitStaking {
    mapping(address => uint256) public balances;
    mapping(address => uint256) public stakingStart;
    uint256 public rewardRate = 5; // 5% annuale

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount, uint256 reward);

    function stake() external payable {
        require(msg.value > 0, "Importo nullo");
        balances[msg.sender] += msg.value;
        stakingStart[msg.sender] = block.timestamp;
        emit Staked(msg.sender, msg.value);
    }

    function unstake() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Nessun saldo");
        uint256 duration = block.timestamp - stakingStart[msg.sender];
        uint256 reward = (amount * rewardRate * duration) / (365 days * 100);
        balances[msg.sender] = 0;
        stakingStart[msg.sender] = 0;
        payable(msg.sender).transfer(amount + reward);
        emit Unstaked(msg.sender, amount, reward);
    }

    function getStake(address user) external view returns (uint256) {
        return balances[user];
    }
}
