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
from packages.valory.protocols.contract_api.message import ContractApiMessage

class SwapSide(Enum):
    """This class scaffolds a behaviour."""
    BUY = "buy"
    SELL = "sell"


TransactionBehaviour = BaseTransactionBehaviour

DEFAULT_BUY_AMOUNT = 100
DEFAULT_SELL_AMOUNT = 100
DEFAULT_FEE_RECIPIENT = "0x5151c6929aBf8bBB75e336C13fe565c02AbcAc23"

BACK_OFF_TIME = 60

CHAIN_ID_TO_BASE_CURRENCY = {
    1: "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    42161: "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
}

CHAIN_ID_TO_TOKENS = {
    1: {
        "solana": "0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a",
        "bonk": "0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a",
        "pepe": "0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a",
    },
    42161: {
        # "edu-coin": "0x6b175474e89094c44da98b954eedeac495271d0f",
        # "palm-ai": "0x6b175474e89094c44da98b954eedeac495271d0f",
        # "grape-2-2": "0x6b175474e89094c44da98b954eedeac495271d0f",
        # "decubate": "0x6b175474e89094c44da98b954eedeac495271d0f",
        # "botto": "0x6b175474e89094c44da98b954eedeac495271d0f",
        # "pepe": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "solana": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
        "bonk": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
        "pepe": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
        # "dogwifcoin": "0x6b175474e89094c44da98b954eedeac495271d0f",
        # "bonk": "0x6b175474e89094c44da98b954eedeac495271d0f",
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
        if self.strategy.rate_limited:
            if (datetime.now() - self.strategy.rate_limited_time).seconds > BACK_OFF_TIME:
                self.strategy.rate_limited, self.strategy.rate_limited_time = False, None
                self.context.logger.info("Rate limit expired.")
            self.context.logger.info("Rate limited, waiting...")
            return
        for ledger_id, token_id in product(self.strategy.ledger_ids, self.strategy.token_ids):
            chain_id = CHAIN_NAME_TO_ID[ledger_id]
            self.prepare_transaction(token_id=token_id, chain_id=chain_id, swap_side=SwapSide.BUY, chain_name=ledger_id)
            # self.prepare_transaction(token_id=token_id, chain_id=chain_id, swap_side=SwapSide.SELL, chain_name=ledger_id)


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

        url = "https://arbitrum.api.0x.org/swap/v1/quote"

        if swap_side == SwapSide.BUY:
            sell_token, buy_token = CHAIN_ID_TO_BASE_CURRENCY[chain_id], CHAIN_ID_TO_TOKENS[chain_id][token_id]
        else:
            sell_token, buy_token = CHAIN_ID_TO_TOKENS[chain_id][token_id], CHAIN_ID_TO_BASE_CURRENCY[chain_id]

        params = {
            "buyToken": buy_token,
            "sellToken": sell_token,
            "sellAmount":  DEFAULT_BUY_AMOUNT if swap_side == SwapSide.BUY else DEFAULT_SELL_AMOUNT,
            "excludedSources": "Kyber", # we exclude Kyber due to the hack.
            "takerAddress": self.context.agent_address,
            "feeRecipient": DEFAULT_FEE_RECIPIENT,
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


class ApprovalPreparationBehaviour(TickerBehaviour):
    """This class scaffolds a behaviour."""

    @property
    def strategy(self) -> PriceRoutingStrategy:
        """Get the strategy."""
        return cast(PriceRoutingStrategy, self.context.price_routing_strategy)
    
    def act(self) -> None:
        """Implement the act."""
        for ledger_id, token_id in product(self.strategy.ledger_ids, self.strategy.token_ids):
            chain_id = CHAIN_NAME_TO_ID[ledger_id]
            self.prepare_approval(token_id=token_id, chain_id=chain_id, chain_name=ledger_id)

    def successful_check_approval_callback(self, contract_api_msg, contract_api_dialogue):
        """Callback for the approval."""
        if contract_api_msg.performative is not ContractApiMessage.Performative.ERROR:
            self.context.logger.info(f"Error in approval: {contract_api_msg.error_code} - {contract_api_msg.error_msg}")
            return
        # we can now check if we have enough allowance
        allowance = contract_api_msg.body.get("allowance")
        if allowance > self.strategy.min_amount:
            self.context.logger.info(f"Allowance is {allowance}, enough to proceed.")
            return
        # we can now proceed to generating the approval transaction.
    
    def prepare_approval(self, chain_id, token_id, chain_name):
        """
        We create the 
        """


    