# Concentration Station

Using the Open Autonomy Framework we have developed a thought controlled tinder inspired application for speculating on altcoins.


Find the documentation [here](https://docs.autonolas.network).

# Coin API
We use the [CoinGecko API](https://www.coingecko.com/en/api) to get the current price of the coins.

# Price Routing

This is handled by [0x](https://0x.org/docs) who provide a [swap API](https://0x.org/products/swap) which we can use to route the swaps.

Docs for the swap API are [here](https://0x.org/docs/0x-swap-api/introduction).

# Chains

A number of chains are supported out of the box for the agent, based on the sponsors of EthDenver
```
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

# Running the agent.

```bash
make run-agent
```

# Setup

```bash
git clone https://github.com/8ball030/concentration_station.git
cd concentration_station
poetry install
# create a ethereum key
poetry run aea generate-key ethereum
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
curl -X POST --header "Content-Type: application/json" 192.168.222.31:5555/swipe --data "{\"coin_id\": \"test\", \"direction\": \"buy\", \"chain_id\": \"arbitrum\"}"
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
