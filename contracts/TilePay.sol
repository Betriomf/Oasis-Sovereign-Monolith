// SPDX-License-Identifier: AGPL-3.0
pragma solidity ^0.8.20;

/**
 * @title TilePay
 * @notice Canales de pago off-chain (Pay-per-tick) para Oasis Play SDK (GPU Assist).
 */
contract TilePay {
    struct Channel {
        address gamer;
        address provider;
        uint256 deposit;
        uint256 nonce;
        bool active;
    }

    mapping(bytes32 => Channel) public channels;
    address public daoTreasury;

    event ChannelOpened(bytes32 indexed channelId, address gamer, address provider, uint256 deposit);
    event ChannelSettled(bytes32 indexed channelId, uint256 payoutProvider, uint256 refundGamer);

    constructor(address _daoTreasury) {
        daoTreasury = _daoTreasury;
    }

    function openChannel(address provider, bytes32 channelId) external payable {
        require(msg.value > 0, "Deposito requerido");
        require(!channels[channelId].active, "Canal ya activo");

        channels[channelId] = Channel({
            gamer: msg.sender,
            provider: provider,
            deposit: msg.value,
            nonce: 0,
            active: true
        });

        emit ChannelOpened(channelId, msg.sender, provider, msg.value);
    }

    function settleChannel(
        bytes32 channelId,
        uint256 finalNonce,
        uint256 providerShare
    ) external {
        Channel memory ch = channels[channelId];
        require(ch.active, "Canal inactivo");
        require(finalNonce > ch.nonce, "Nonce invalido");
        require(providerShare <= ch.deposit, "Fondos insuficientes");

        channels[channelId].active = false;

        uint256 fee = (providerShare * 5) / 100;
        uint256 netProvider = providerShare - fee;
        uint256 refundGamer = ch.deposit - providerShare;

        payable(daoTreasury).transfer(fee);
        payable(ch.provider).transfer(netProvider);
        if (refundGamer > 0) {
            payable(ch.gamer).transfer(refundGamer);
        }

        emit ChannelSettled(channelId, netProvider, refundGamer);
    }
}
