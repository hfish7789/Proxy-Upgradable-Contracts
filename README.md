## Proxy Upgradable Contracts
This is an implementation of upgradable smart contract using proxies

## Overview:
   
   Everyone in the blockchain world knows that smart contracts are immutable, meaning that once they are deployed on chain their core logic can't be changed. So developers must perform all the tests and verify every line of code in order to avoid mistakes or bugs which may lead to vulnerabilities inside the protocol. 
   <br/>
   But what if a major breakthrough happens in DEFI ecosystem for example, what if there is a new way to use automated market makers, a protocol like AAVE will need to create a new set of smart contracts and thus change the previous addresses, which means that other protocols that rely on AAVE would have to update their dapps and this could create a big mess.
   <br/>
   For this purpose, developers have created a way to upgrade a smart contract - not realy upgrade but almost - using something called PROXY, a proxy is contract that holds all the deployements of a given protocol (versions of the protocol), and when a user make a call the proxy automatically redirect the call to the latest implementation. So in order to "Upgrade" a smart contract the admin (or the DAO) need to deploy the new version and then add it to the proxy, ET VOILA the smart contract has been upgraded.
   
   In this repo, i created a simple pattern for upgrading smart contract using OpenZeppelin and i tested it on Box.sol and BoxV2.sol

## How to Use:

### Installation & Setup:

1. Installing Brownie: Brownie is a python framework for smart contracts development,testing and deployments. It's quit like [HardHat](https://hardhat.org) but it uses python for writing test and deployements scripts instead of javascript.
   Here is a simple way to install brownie.
   ```
    pip install --user pipx
    pipx ensurepath
    # restart your terminal
    pipx install eth-brownie
   ```
   Or if you can't get pipx to work, via pip (it's recommended to use pipx)
    ```
    pip install eth-brownie
    ```
   Install [ganache-cli](https://www.npmjs.com/package/ganache-cli): 
   ```sh
    npm install -g ganache-cli
    ```
    
3. Clone the repo:
   ```sh
   git clone https://github.com/Aymen1001/proxy-upgradable-contracts.git
   cd proxy-upgradable-contracts
   ```

4. Set your environment variables:

   To be able to deploy to real testnets you need to add your PRIVATE_KEY (You can find your PRIVATE_KEY from your ethereum wallet like metamask) and the infura project Id (just create an infura account it's free) to the .env file:
   ```
   PRIVATE_KEY=<PRIVATE_KEY>
   WEB3_INFURA_PROJECT_ID=<< YOUR INFURA PROJECT ID >>
   ```
### How to run:

To upgrade the Box contract to BoxV2 on development network, run the command :
   ```sh
   brownie run scripts/upgrade_box_contract.py
   ```
To use upgrade on real testnets (kovan, rinkbey,...), run the command :
   ```sh
   brownie run scripts/upgrade_box_contract.py --network=<testnet name>
   ```
### Testing:

The tests for the upgrade functionnalities can be found in the tests folder. 

You can run all the tests by :
   ```sh
   brownie test
   ```
Or you can test each function individualy:
   ```sh
   brownie test -k <function name>
   ```
