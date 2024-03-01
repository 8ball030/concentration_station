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

"""This package contains a scaffold of a handler."""

import json
from typing import Optional, cast

from aea.configurations.base import PublicId
from aea.protocols.base import Message
from aea.skills.base import Handler

from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.skills.concentration_api.behaviours import TransactionBehaviour
from packages.eightballer.skills.price_router.strategy import PriceRoutingStrategy
from packages.eightballer.protocols.http.message import HttpMessage
from packages.valory.protocols.ledger_api.dialogues import LedgerApiDialogues
from packages.valory.protocols.ledger_api.message import LedgerApiMessage
from packages.valory.connections.ledger.connection import (
    PUBLIC_ID as LEDGER_CONNECTION_PUBLIC_ID,
)
from packages.valory.protocols.ledger_api.message import LedgerApiMessage

from packages.eightballer.skills.concentration_api.handlers import LedgerApiHandler as BaseLedgerApiHandler
from packages.eightballer.skills.concentration_api.handlers import SigningHandler as BaseSigningHandler

LEDGER_API_ADDRESS = str(LEDGER_CONNECTION_PUBLIC_ID)


LedgerApiHandler = BaseLedgerApiHandler
SigningHandler = BaseSigningHandler



class HttpHandler(Handler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = HttpMessage.protocol_id

    @property
    def strategy(self) -> PriceRoutingStrategy:
        """Get the strategy."""
        return cast(PriceRoutingStrategy, self.context.price_routing_strategy)
    

    def setup(self) -> None:
        """Implement the setup."""

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        self.context.logger.debug("handling http message...")
        http_message = cast(HttpMessage, message)
        dialogue = self.context.http_dialogues.update(http_message)

        result = {}
        if http_message.performative == HttpMessage.Performative.RESPONSE:
            response = http_message.body
            data = json.loads(response)
            for key in self.strategy.api_routers[0]['api_request']['keys']:
                if key in data:
                    result[key] = data[key]
            
        self.context.logger.debug(f"result: {result}")
        self.context.price_routing_strategy.prepared_transactions[dialogue.chain_id][dialogue.swap_side.name] = result


    def teardown(self) -> None:
        """Implement the handler teardown."""




class OrdersHandler(Handler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = OrdersMessage.protocol_id

    @property
    def strategy(self) -> PriceRoutingStrategy:
        """Get the strategy."""
        return cast(PriceRoutingStrategy, self.context.strategy)
    

    def setup(self) -> None:
        """Implement the setup."""

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        orders_message = cast(OrdersMessage, message)
        order = orders_message.order
        self.context.logger.info(f"handling new orders message. Side: {order.side.name}, Exchange: {order.exchange_id}, Symbol: {order.symbol}")
        # note we are assuming that the prepared transactions are already available
        # we are also for simplicity assuming that there is no symbol
        try:
            raw_tx = self.context.price_routing_strategy.prepared_transactions[order.exchange_id][order.side.name]
        except KeyError:
            self.context.logger.error("No prepared transaction available for the given order!")
            return
        self.send_raw_tx(raw_tx, orders_message.order)


    def teardown(self) -> None:
        """Implement the handler teardown."""

    def send_raw_tx(self, raw_tx, order):
        """Send the raw transaction to the ledger."""
        self.context.logger.info(f"Sending raw tx!")
        self.context.logger.debug(f"{raw_tx}")
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        strategy = cast(PriceRoutingStrategy, self.context.price_routing_strategy)
        to_address = "0xdef1c0ded9bec7f1a1670819833240f027b25eff"

        terms = strategy.get_swap_terms(raw_tx, order.exchange_id)
        if terms is None:
            self.context.logger.error("Invalid terms!")
            return
        tx_behaviour = cast(TransactionBehaviour, self.context.behaviours.transaction)
        tx_behaviour.waiting.append(terms)
