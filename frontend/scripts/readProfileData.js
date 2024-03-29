// Import and Network Setup

import { ERC725 } from '@erc725/erc725.js';
import lsp3ProfileSchema from '@erc725/erc725.js/schemas/LSP3ProfileMetadata.json' assert { type: 'json' };
import { ethers, JsonRpcProvider } from "ethers";
// Our static variables
//const SAMPLE_PROFILE_ADDRESS2 = '0x6979474Ecb890a8EFE37daB2b9b66b32127237f7';
const SAMPLE_PROFILE_ADDRESS = "0x958508bf61756A17c3Cf4ad2968EF6E225091eB3";
const RPC_ENDPOINT = 'https://rpc.testnet.lukso.network';
const IPFS_GATEWAY = 'https://api.universalprofile.cloud/ipfs';

// Parameters for ERC725 Instance
const provider = new JsonRpcProvider(RPC_ENDPOINT);
//const provider = new Web3.providers.HttpProvider(RPC_ENDPOINT);
const config = { ipfsGateway: IPFS_GATEWAY };

async function fetchProfile(address) {
    try {
        const profile = new ERC725(lsp3ProfileSchema, address, provider, config);
        console.log(profile)
        return await profile.fetchData();
    } catch (error) {
        console.log(error)
        return console.log('This is not an ERC725 Contract');
    }
}

fetchProfile(SAMPLE_PROFILE_ADDRESS).then((profileData) =>
    console.log(JSON.stringify(profileData, undefined, 2)),
);