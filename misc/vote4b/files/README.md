# vote4b

Welcome to the world of Web3!

For the basics of Web3 and Solidity, refer to resources like the [Solidity official documentation](https://soliditylang.org/).

## Testing Locally

There are several ways to test Solidity contracts locally.

Here, we'll explain using the standard framework [Foundry](https://book.getfoundry.sh/). If you haven't used Foundry before, follow the [installation guide](https://book.getfoundry.sh/getting-started/installation) to install it.

### Setting Up a Test Network

Testing on an open Ethereum network requires fees called Gas. Using a command called [anvil](https://book.getfoundry.sh/reference/anvil/) included with Foundry, you can create your own local network.

```
$ anvil
```

Running this command will display the addresses and private keys of 10 accounts. These are all owned by you, and each holds 10000 ETH initially (though they have no real value since this is a test network). Note that as specified in `deploy/config.yaml`, you only have 1 ETH on remote.

You'll need two accounts for Web3 challenges: a victim and an attacker. Note the addresses and private keys of two chosen accounts.

An RPC endpoint, used by Web3 clients to interact with the network, is created. This is shown at the end of `anvil`'s output, typically `http://localhost:8545/`.

```
Listening on 127.0.0.1:8545
```

### Initializing a Project

To deploy and test the Solidity file, [create a project](https://book.getfoundry.sh/reference/forge/forge-init). For example, the following command creates a project named `vote4b`.

```
$ forge init vote4b
```

By default, a sample contract called `Counter` is created, but we'll delete it since we won't be using it.

```
$ rm src/Counter.sol test/Counter.sol script/Counter.s.sol
```

### Installing Dependencies

Looking at the `src/Ballot.sol` file in the distribution, it installs some external libraries.

```sol
import { Ownable } from "@openzeppelin/contracts/access/Ownable.sol";
import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
```

These are from the [OpenZeppelin Contracts](https://github.com/OpenZeppelin/openzeppelin-contracts), a widely used library providing safe implementations of common features and standardized protocols in Web3.

[Install the library](https://book.getfoundry.sh/reference/forge/forge-install). (If there are changes to the project, commit them with `git commit` first.)

```
$ git commit -a
$ forge install openzeppelin/openzeppelin-contracts
```

### Deploying the Contract

Copy all `.sol` files from the `src` folder of the distribution to the `src` folder of the project you created. The `Setup.sol` file specifies the `Setup` contract, which serves as the starting point for this challenge. [Create the `Setup` contract](https://book.getfoundry.sh/reference/forge/forge-create) using the victim's account information you noted earlier.

```
$ forge create --rpc-url <RPC URL> --private-key <Victim's Private Key> src/Setup.sol:Setup
```

If the contract compiles and creates successfully, the output should include "Deployed to."

```
Deployed to: 0xXXXXXXXX....XXXXXXXX
```

Note this hexadecimal address, as it is the address of your deployed `Setup` contract.

### Challenge Overview

With the contract deployed, read the source code to understand its purpose. `Ballot.sol` uses the [ERC721](https://ethereum.org/en/developers/docs/standards/tokens/erc-721/) (NFT; Non-Fungible Token) standard to implement a voting mechanism. Understand how ownership of voting papers and prevention of multiple votes are achieved by reading the source code, [Solidity language specification](https://docs.soliditylang.org/en/v0.8.26/), and OpenZeppelin's [ERC721 specification](https://docs.openzeppelin.com/contracts/4.x/erc721).

As specified in `deploy/verifier.py`, the goal is to make the `isSolved` function of the `Setup` contract return true.

```
function isSolved() public view returns (bool) {
  return ballot.votes(address(this)) >= 10;
}
```

The objective is to cast 10 or more votes to the `Setup` contract.

### Creating the Exploit

An exploit template is provided in `template/Exploit.s.sol`. This is written for use with [`forge script`](https://book.getfoundry.sh/reference/forge/forge-script). Copy this code to the `script` folder of the `vote4b` project.

In the `Script`, the `setUp` function is called first. The template code only sets up the `Setup` contract and the attacker's account, so set the appropriate addresses and keys.

```sol
  function setUp() public {
    chall = Setup(/* Setup Contract's Address */);
    solver = vm.createWallet(/* Attacker's Private Key */);
  }
```

Next, the `run` function is called. The template code calls [`startBroadcast`](https://book.getfoundry.sh/cheatcodes/start-broadcast) to execute all subsequent operations using the attacker's account. As an example, it references the `ballot` held by the `Setup` contract and checks its `votes` variable. It finally requires `chall.isSolved()` to be true, so transactions will fail unless the challenge is solved.

```sol
  function run() public {
    vm.startBroadcast(solver.privateKey);

    // Your exploit goes here
    Ballot ballot = chall.ballot();
    uint256 n = ballot.votes(address(chall));

    require(chall.isSolved(), "Not solved");
  }
```

To test the exploit, use the [`forge script` command](https://book.getfoundry.sh/reference/forge/forge-script). For example, you can test the `Exploit` contract in `Exploit.s.sol` with the following command.

```
$ forge script --rpc-url <RPC URL> --private-key <Attacker's Private Key> --broadcast script/Exploit.s.sol:Exploit
```

Check Solidity language specifications and common vulnerabilities to complete your exploit to manipulates the voting results.

## Testing with Docker

To replicate the remote environment using Docker, use the following commands.

```
$ docker build . -t vote4b
$ docker run --rm -p 8000:8000 vote4b
```

Access http://localhost:8000/start in your web browser to get four endpoints, each containing a random hexadecimal ID. (If you lose this ID, you will need to rebuild the instance.)

1. `/(Your_ID)/rpc`
   RPC network endpoint
2. `/(Your_ID)/info`
   Endpoint to retrieve contract and account information
3. `/(Your_ID)/reset`
   Endpoint to reset the test network state
4. `/(Your_ID)/flag`
   Endpoint to display the flag if the challenge is solved

First, access http://localhost:8000/(Your_ID)/info to get the following three pieces of information:

1. `level_contract_address`
   Address of the Setup contract (`src/Setup.sol`) deployed on the Ethereum test network
2. `user_private_key`
   Your account's private key
3. `user_address`
   Your account's address

By changing the RPC URL passed to the forge command and incorporating the above information into your Exploit contract, you can solve the challenge on the test network. Once the `isSolved` function returns true, access `/(Your_ID)/flag` to confirm that you have obtained the flag.

## Solving on Remote

All contracts and transactions on the Ethereum network are public to all users. To prevent someone from stealing your Exploit contract, the actual challengeserver separates the Ethereum network for each user.

Access the challenge URL and click the "Spawn instance" button to create your own network valid for 10 minutes. The obtained URL (e.g., `http://NGwEtghVvYWJoUfm:ZrlngjpJoGcNzSAX@vote4b.beginners.seccon.games:63607`) functions the same as `localhost:8000`. Access the `/start` endpoint to create the test network, change the RPC and contract addresses for sending the Exploit, and obtain the flag.

