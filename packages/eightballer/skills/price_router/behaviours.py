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


CHAIN_ID_TO_BASE_CURRENCY = {
    1: "0x6b175474e89094c44da98b954eedeac495271d0f",
}
TransactionBehaviour = BaseTransactionBehaviour

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
            self.prepare_transaction(ledger_id, token_id, SwapSide.BUY)
            self.prepare_transaction(ledger_id, token_id, SwapSide.SELL)


    def setup(self) -> None:
        """Implement the setup."""

        for ledger_id in self.strategy.ledger_ids:
            self.strategy.prepared_transactions[ledger_id] = {}
            for token_id in self.strategy.token_ids:
                self.strategy.prepared_transactions[ledger_id][str(token_id)] = {}

    
    def teardown(self) -> None:
        """Implement the task teardown."""


    def prepare_transaction(self, chain_id, token_id, swap_side):
        """
        Submit a http request to the router to prepare a transaction.
        we just submit a message to the router to prepare a transaction.
        """
        router_kwargs = self.strategy.api_routers[0]['api_request']
        http_msg, dialogue = self.context.http_dialogues.create(
            counterparty=str(HTTP_CLIENT_PUBLIC_ID),
            performative=HttpMessage.Performative.REQUEST,
            method=router_kwargs['method'],
            url=router_kwargs['url'],
            headers=json.dumps(router_kwargs['headers'])[1:-1].replace('"', ''),
            body=bytes(router_kwargs['body'], 'utf-8'),
            version=router_kwargs['version'],
        )
        dialogue.swap_side, dialogue.chain_id, dialogue.token_id = swap_side, chain_id, token_id
        self.context.outbox.put_message(message=http_msg)

        

    def __init__(self, tick_interval: float = 20, start_at: datetime | None = None, **kwargs: Any) -> None:
        super().__init__(tick_interval, start_at, **kwargs)