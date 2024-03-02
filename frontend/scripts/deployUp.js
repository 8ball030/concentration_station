// You might need to use node v16.0.0 (nvm use 16.0.0) when running this
// This is because node made a change and a flag is required in the fetch command, and the ipfs-http-client hasn't made an update
// So only older versions of node will work.
// You can do this with `nvm use 16.0.0`

import { LSPFactory } from '@lukso/lsp-factory.js';
import dotenv from 'dotenv/config';
import { ethers } from "ethers";


const PRIVATE_KEY = process.env.MY_PRIVATE_KEY;
const myEOA = new ethers.Wallet(PRIVATE_KEY);

const lspFactory = new LSPFactory('rpc.testnet.lukso.network/', {
    deployKey: PRIVATE_KEY,
    chainId: 4201, // LUKSO Testnet
});

async function createUniversalProfile() {
    const deployedContracts = await lspFactory.UniversalProfile.deploy({
        controllerAddresses: [myEOA.address],
        lsp3Profile: {
            name: 'My Universal Profile',
            description: 'My Cool Universal Profile',
            tags: ['Public Profile'],
            links: [],
        },
    });

    const myUPAddress = deployedContracts.LSP0ERC725Account.address;
    console.log('my Universal Profile address: ', myUPAddress);

    // Now we can add this UP address to our .env file
    return deployedContracts;
}
createUniversalProfile();

