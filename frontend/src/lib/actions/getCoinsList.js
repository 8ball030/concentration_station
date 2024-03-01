export default async function loadCoins(){
    const url = 'https://api.coingecko.com/api/v3/search/trending';
    const response = await fetch(url);

    if (response.ok) {
        const coins  = await response.json();
        return coins;
    }

    throw new Error('loadCoins Network response was not ok.');
};