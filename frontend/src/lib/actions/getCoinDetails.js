/**
 * @param {string} coinId
 */
export default async function getCoinDetails(coinId){
    const url = `https://api.coingecko.com/api/v3/coins/${coinId}`;
    const response = await fetch(url);

    if (response.ok) {
        const coin  = await response.json();
        const platforms = Object.keys(coin.platforms);
        return coin.platforms[0];
    }

    throw new Error('Network response was not ok.');
};