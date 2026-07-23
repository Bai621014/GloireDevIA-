// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title GloireCoin (GLC) - Jetons VIP GloirePay
 * @notice Contrat standard ERC-20 optimisé pour la sécurité et la rapidité sur Polygon.
 */
contract GloireCoin {
    string public name = "Gloire Coin";
    string public symbol = "GLC";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    address public owner;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event TokensMinted(address indexed to, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Accès refusé : Seul le propriétaire VIP peut émettre");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @notice Émission sécurisée de jetons GLC vers un coffre/portefeuille cible
     */
    function emettreJetons(address destinataire, uint256 montant) external onlyOwner {
        require(destinataire != address(0), "Adresse invalide");
        
        uint256 totalMontant = montant * (10 ** uint256(decimals));
        totalSupply += totalMontant;
        balanceOf[destinataire] += totalMontant;

        emit TokensMinted(destinataire, montant);
        emit Transfer(address(0), destinataire, totalMontant);
    }

    function transfer(address recipient, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Solde insuffisant");
        balanceOf[msg.sender] -= amount;
        balanceOf[recipient] += amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }
}
