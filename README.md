# Speculation Station

Speculation Station is a thought controlled tinder inspired application for speculating on altcoins.

Using the Open Autonomy Framework we have brought together a number of disparate technologies to invisage a perhaps distopia world where were can transact as fast as the speed of the thought.

We present a proof of concept of a thought controlled application that allows the user to buy and sell altcoins using their brainwaves, no need to touch a keyboard or mouse, just think and the application will do the rest, no need to worry or stress about the current price of the coin.

(We are not responsible for any financial loss incurred by using this application, please use responsibly. Again, this is a proof of concept and should not be used for any real trading. I cannot stress this enough, do not use this for real trading. This was built to have fun and play with the idea of a thought controlled application.)

## The Idea

What if i could buy shitcoins just by thinking about it? What if i could sell them just as fast? What if i could do it all without touching a keyboard or mouse? What if i could do it all without even looking at a screen?

This is the idea behind Speculation Station. We have built a proof of concept of a thought controlled application that allows the user to buy and sell altcoins using their brainwaves. No need to touch a keyboard or mouse, just think and the application will do the rest. No need to worry or stress about the current price of the coin.

The application is based on the idea of a future where we will be able to interface much more directly with the digital world. We used an EEG headset to read the brainwaves of the user and then use that to control the application.

We were able to accomplish this by effectively streaming the data from the EEG headset over bluetooth to a server which then processed the data and used it to create a dataset aligned with the users blinks. Using this data we were able to create a model that could predict the users blinks with a high degree of accuracy (around 90%).

We then used this model to control the application. The user would be shown a series of coins and they could swipe left or right to indicate if they wanted to buy or sell the coin. The application would then use the Open [Autonomy Framework](https://github.com/valory-xyz/open-autonomy) to route the transaction to the relevant chain and execute the trade.

This was a proof of concept and we were able to demonstrate the application working in a live demo, where we were able to control the application using the EEG headset, and execute trades on the Ethereum and Arbitrum chains.

Signficantly outprforming even the fastest traders, we were able to execute trades in under 1 second, and we were able to do it all without touching a keyboard or mouse.

We used the following technologies to build the application:
- [Open Autonomy Framework](https://docs.autonolas.network)
- [Muse EEG headset](https://choosemuse.com/)
- [0x Swap API](https://0x.org/docs/0x-swap-api/introduction)
- [CoinGecko API](https://www.coingecko.com/en/api)


Find the documentation [here](https://docs.autonolas.network).

## Coin API

We use the [CoinGecko API](https://www.coingecko.com/en/api) to get the current price of the coins.

## Price Routing

This is handled by [0x](https://0x.org/docs) who provide a [swap API](https://0x.org/products/swap) which we can use to route the swaps.

Docs for the swap API are [here](https://0x.org/docs/0x-swap-api/introduction).

We make use of the affiliate fees to generate revenue for the application. This is done by using the `feeRecipient` parameter in the swap API.

## Chains

A number of chains are supported out of the box for the agent, based on the sponsors of EthDenver, and the chains that are supported by the 0v swap API.

```json
{
    "ethereum": {
      "ledger_id": "ethereum",
      "chain_id": 1,
      "chain_name": "Ethereum",
      "explorer_url": "https://etherscan.io/",
      "native_currency": "ETH"
    },
    "arbitrum": {
      "ledger_id": "arbitrum",
      "chain_id": 42161,
      "chain_name": "Arbitrum",
      "explorer_url": "https://arbiscan.io/",
      "native_currency": "ETH"
    },
    "celo": {
      "ledger_id": "celo",
      "chain_id": 42220,
      "chain_name": "",
      "explorer_url": "https://celoscan.io/",
      "native_currency": "CELO"
    },
    "base": {
      "ledger_id": "base",
      "chain_id": 8453,
      "chain_name": "Base",
      "explorer_url": "https://basescan.org/",
      "native_currency": "ETH"
    },
    "matic": {
      "ledger_id": "matic",
      "chain_id": 137,
      "chain_name": "Matic",
      "explorer_url": "https://polygonscan.com/",
      "native_currency": "MATIC"
    }
}
```

## Setup

```bash
git clone https://github.com/8ball030/concentration_station.git
cd concentration_station
poetry install && poetry run autonomy packages sync
# create a ethereum key
poetry run aea generate-key ethereum
```

## Running the agent.

```bash
make run-agent
```

# Sample requests
The api for agent is available at `http://localhost:5555' and the following are the sample requests.

```bash
curl localhost:5000/current_coin
```

To see the available ledgers.
```bash
curl localhost:5555/ledgers
```

To see transactions by the agent
```bash
curl localhost:5555/transactions
```

To submit a swipe request;
```bash
curl -X POST --header "Content-Type: application/json" localhost:5553/swipe --data "{\"coin_id\": \"test\", \"direction\": \"LEFT\", \"ledger_id\": \"ethereum\"}"
```



## System requirements

- Python `>=3.8`
- [Tendermint](https://docs.tendermint.com/v0.34/introduction/install.html) `==0.34.19`
- [IPFS node](https://docs.ipfs.io/install/command-line/#official-distributions) `==0.6.0`
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Poetry](https://python-poetry.org/)
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Alternatively, you can fetch this docker image with the relevant requirements satisfied:

> **_NOTE:_**  Tendermint and IPFS dependencies are missing from the image at the moment.

```bash
docker pull valory/open-autonomy-user:latest
docker container run -it valory/open-autonomy-user:latest
```

## This repository contains:

- Empty directory `packages` which acts as the local registry

- .env file with Python path updated to include packages directory

## How to use

Create a virtual environment with all development dependencies:

```bash
poetry shell
poetry install
```

Get developing...

## Useful commands:

Check out the `Makefile` for useful commands, e.g. `make formatters`, `make generators`, `make code-checks`, as well
as `make common-checks-1`. To run tests use the `autonomy test` command. Run `autonomy test --help` for help about its usage.

