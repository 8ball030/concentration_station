import {BASE_URL} from '$lib/consts'

/**
 * @param {string} endpoinName
 */
async function getRequest(endpoinName) {
    const response = await fetch(`${BASE_URL}${endpoinName}`);

    if (response.ok) {
        const data  = await response.json();
        return data;
    }

    throw new Error(`${endpoinName} network response was not ok.`);
}
/**
 * @param {string} endpoinName
 * @param {any} body
 */
async function postRequest(endpoinName, body) {
    const response = await fetch(`${BASE_URL}${endpoinName}`, body);
    console.log("response", response)
    if (response.ok) {
        const data  = await response.json();
        return data;
    }

    throw new Error(`${endpoinName} network response was not ok.`);
}

export async function getCurrentCoin(){
    const COIN_ENDPOINT = `/current_coin`;
    const response = await getRequest(COIN_ENDPOINT);
    return response
};

export async function getTransactions(){
    const TRANSACTIONS_ENPOINT = `/transactions`;
    const response = await getRequest(TRANSACTIONS_ENPOINT);
    return response
};

export async function getLedgers(){
    const LEDGERS_ENPOINT = `/ledgers`;
    const response = await getRequest(LEDGERS_ENPOINT);
    return response.ledgers
};

/**
 * @param {string} coin_id
 * @param {string} direction
 */
export async function postSwap(coin_id, direction){
    const SWAP_ENDPOINT = `/swipe`;
    const body = {
        method: "POST",
        body: JSON.stringify({
            coin_id,
            direction
        }),
    };

    const response = await postRequest(SWAP_ENDPOINT, body);
    return response
};