# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains a scaffold of a behaviour."""

from datetime import datetime
from itertools import product
import json
from typing import Any, cast
from aea.skills.behaviours import TickerBehaviour

from enum import Enum
from packages.eightballer.protocols.http.message import HttpMessage
from packages.eightballer.connections.http_client.connection import PUBLIC_ID as HTTP_CLIENT_PUBLIC_ID
from packages.eightballer.skills.concentration_api.behaviours import TransactionBehaviour as BaseTransactionBehaviour

from packages.eightballer.skills.price_router.strategy import PriceRoutingStrategy

class SwapSide(Enum):
    """This class scaffolds a behaviour."""
    BUY = "buy"
    SELL = "sell"


TransactionBehaviour = BaseTransactionBehaviour

DEFAULT_BUY_AMOUNT = 100000
DEFAULT_SELL_AMOUNT = 100000


CHAIN_ID_TO_BASE_CURRENCY = {
    1: "0x6b175474e89094c44da98b954eedeac495271d0f",
    42161: "0x6b175474e89094c44da98b954eedeac495271d0f",
}

CHAIN_ID_TO_TOKENS = {
    1: {
    },
    42161: {
        "edu-coin": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "palm-ai": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "grape-2-2": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "decubate": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "botto": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "pepe": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "solana": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "dogwifcoin": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "bonk": "0x6b175474e89094c44da98b954eedeac495271d0f",
    },
}

CHAIN_NAME_TO_ID = {
    "ethereum": 1,
    "arbitrum": 42161,
}


class TransactionPreparationBehaviour(TickerBehaviour):
    """This class scaffolds a behaviour."""
    prepared_transactions = {}


    @property
    def strategy(self) -> PriceRoutingStrategy:
        """Get the strategy."""
        return cast(PriceRoutingStrategy, self.context.price_routing_strategy)

    def act(self) -> None:
        """Implement the act."""
        for ledger_id, token_id in product(self.strategy.ledger_ids, self.strategy.token_ids):
            chain_id = CHAIN_NAME_TO_ID[ledger_id]
            self.prepare_transaction(token_id=token_id, chain_id=chain_id, swap_side=SwapSide.BUY, chain_name=ledger_id)
            self.prepare_transaction(token_id=token_id, chain_id=chain_id, swap_side=SwapSide.SELL, chain_name=ledger_id)


    def setup(self) -> None:
        """Implement the setup."""

        for ledger_id in self.strategy.ledger_ids:
            self.strategy.prepared_transactions[ledger_id] = {}
            for token_id in self.strategy.token_ids:
                self.strategy.prepared_transactions[ledger_id][str(token_id)] = {}

    def teardown(self) -> None:
        """Implement the task teardown."""


    def prepare_transaction(self, chain_id, token_id, swap_side, chain_name):
        """
        Submit a http request to the router to prepare a transaction.
        we just submit a message to the router to prepare a transaction.
        """
        router_kwargs = self.strategy.api_routers[0]['api_request']
        # 
        # url: https://arbitrum.api.0x.org/swap/v1/quote?buyToken=0x064f8b858c2a603e1b106a2039f5446d32dc81c1&sellToken=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&sellAmount=100000&excludedSources=Kyber&takerAddress=0xBa95718a52b5a3DBa749a7641712Dc05a3550d4f

        url = "https://arbitrum.api.0x.org/swap/v1/quote"

        if swap_side == SwapSide.BUY:
            # we are buying the token
            sell_token, buy_token = CHAIN_ID_TO_BASE_CURRENCY[chain_id], CHAIN_ID_TO_TOKENS[chain_id][token_id]
        else:
            # we are selling the token
            sell_token, buy_token = CHAIN_ID_TO_TOKENS[chain_id][token_id], CHAIN_ID_TO_BASE_CURRENCY[chain_id]

        params = {
            "buyToken": buy_token,
            "sellToken": sell_token,
            "sellAmount":  DEFAULT_BUY_AMOUNT if swap_side == SwapSide.BUY else DEFAULT_SELL_AMOUNT,
            "excludedSources": "Kyber", # we exclude Kyber due to the hack.
            "takerAddress": self.context.agent_address,
        }

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{url}?{query_string}"
        http_msg, dialogue = self.context.http_dialogues.create(
            counterparty=str(HTTP_CLIENT_PUBLIC_ID),
            performative=HttpMessage.Performative.REQUEST,
            method=router_kwargs['method'],
            url=url,
            headers=json.dumps(router_kwargs['headers'])[1:-1].replace('"', ''),
            body=bytes(router_kwargs['body'], 'utf-8'),
            version=router_kwargs['version'],
        )
        dialogue.swap_side, dialogue.chain_id, dialogue.token_id = swap_side, chain_name, token_id
        self.context.outbox.put_message(message=http_msg)
        

    def __init__(self, tick_interval: float = 20, start_at: datetime | None = None, **kwargs: Any) -> None:
        super().__init__(tick_interval, start_at, **kwargs)