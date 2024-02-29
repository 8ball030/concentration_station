# Concentration Station

Using the Open Autonomy Framework we have developed a thought controlled tinder inspired application for speculating on altcoins.


Find the documentation [here](https://docs.autonolas.network).

# Setup

```bash
git clone https://github.com/8ball030/concentration_station.git
cd concentration_station
poetry install
# create a ethereum key
aea generate-key ethereum
```

# Running the agent.

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
curl -X POST --header "Content-Type: application/json" localhost:5000/swipe --data "{\"coin_id\": \"test\", \"direction\": \"buy\"}"
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
