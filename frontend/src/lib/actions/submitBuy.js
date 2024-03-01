import getCoinDetails from "./getCoinDetails";

/**
 * @param {string} coinId
 */
export default async function submitBuy(coinId){
    const tokenAddress = await getCoinDetails(coinId);

    const submitURL = 'https://';
    const response = await fetch(
        `url`,
        {
         method: "POST",
         mode: "no-cors",
         headers: {
          "Content-Type": "application/json",
         },
         body: JSON.stringify({
            tokenAddress,
         }),
        }
       );
      
       const json = await response.json();
       console.log("json ", json);
       return json;
};
