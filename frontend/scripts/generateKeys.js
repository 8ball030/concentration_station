import { ethers } from "ethers";

const provider = new ethers.JsonRpcProvider("https://rpc.testnet.lukso.network/");

let account = ethers.Wallet.createRandom(provider);
console.log("My private key is: " + account.privateKey);
console.log("My address is: " + account.address);

// Now we can add this key and address to our .env file

async function getBalance() {
    let balance = await provider.getBalance(account.address);
    console.log("My balance: " + ethers.formatEther(balance) + "ether LYXt");
    
}

getBalance();