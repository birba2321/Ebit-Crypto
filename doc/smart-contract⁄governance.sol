// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EbitGovernance {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    Proposal[] public proposals;
    mapping(address => mapping(uint256 => bool)) public votes;

    event ProposalCreated(uint256 id, string description);
    event Voted(address indexed voter, uint256 proposalId);
    event Executed(uint256 proposalId);

    function createProposal(string memory _description) public {
        proposals.push(Proposal({
            description: _description,
            voteCount: 0,
            executed: false
        }));
        emit ProposalCreated(proposals.length - 1, _description);
    }

    function vote(uint256 proposalId) public {
        require(proposalId < proposals.length, "Proposta inesistente");
        require(!votes[msg.sender][proposalId], "Hai già votato");
        proposals[proposalId].voteCount += 1;
        votes[msg.sender][proposalId] = true;
        emit Voted(msg.sender, proposalId);
    }

    function executeProposal(uint256 proposalId) public {
        require(proposalId < proposals.length, "Proposta inesistente");
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Già eseguita");
        require(proposal.voteCount > 10, "Voti insufficienti");
        proposal.executed = true;
        emit Executed(proposalId);
    }

    function getProposal(uint256 proposalId) public view returns (string memory, uint256, bool) {
        Proposal memory p = proposals[proposalId];
        return (p.description, p.voteCount, p.executed);
    }
}
