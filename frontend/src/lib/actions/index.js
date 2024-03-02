import { BASE_URL } from '$lib/consts'

/**
 * @param {string} endpoinName
 * @param {any} handleError
 */
async function getRequest(endpoinName, handleError) {
    try {
        const response = await fetch(`${BASE_URL}${endpoinName}`);
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error(`${endpoinName} network response was not ok.`);
        }
    } catch (err) {
        handleError(endpoinName, err)
        return { error: err }
    }
}
/**
 * @param {string} endpoinName
 * @param {any} body
 * @param {any} handleError
 */
async function postRequest(endpoinName, body, handleError) {
    try {
        const response = await fetch(`${BASE_URL}${endpoinName}`, body);

        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error(`${endpoinName} network response was not ok.`);
        }
    } catch (err) {
        handleError(endpoinName, err)
        return { error: err }
    }
}

/**
 * @param {any} handleApiError
 */
export async function getCurrentCoin(handleApiError) {
    const COIN_ENDPOINT = `/current_coin`;
    const response = await getRequest(COIN_ENDPOINT, handleApiError);

    console.log("response", response)
    return response
};

/**
 * @param {any} handleApiError
 */
export async function getTransactions(handleApiError) {
    const TRANSACTIONS_ENPOINT = `/transactions`;
    const response = await getRequest(TRANSACTIONS_ENPOINT, handleApiError);

    return response
};

/**
 * @param {any} handleApiError
 */
export async function getLedgers(handleApiError) {
    const LEDGERS_ENPOINT = `/ledgers`;
    const response = await getRequest(LEDGERS_ENPOINT, handleApiError);
    return response.ledgers
};

/**
 * @param {string} coin_id
 * @param {string} chain_id
 * @param {string} direction
 * @param {any} [handleApiError]
 */
export async function postSwap(coin_id, direction, chain_id, handleApiError) {
    const SWAP_ENDPOINT = `/swipe`;
    const body = {
        method: "POST",
        body: JSON.stringify({
            coin_id,
            direction,
            chain_id
        }),
    };

    const response = await postRequest(SWAP_ENDPOINT, body, handleApiError);
    return response
};

/**
 * @param {string} user_id
 */
export async function postUser(user_id) {
    const USER_ENDPOINT = `/users/${user_id}`;
    const body = {
        method: "POST",
        body: JSON.stringify({}),
    };

    const response = await postRequest(USER_ENDPOINT, body, () => { });
    return response
};