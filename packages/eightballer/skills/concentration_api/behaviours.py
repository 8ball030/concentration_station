# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2020 Fetch.AI Limited
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

"""This package contains the behaviour for the erc-1155 client skill."""

from datetime import datetime
import json
import random
from typing import Any, List, Optional, Set, cast

from aea.skills.behaviours import TickerBehaviour

from packages.eightballer.protocols.fipa.dialogues import FipaDialogue
from packages.eightballer.protocols.websockets.message import WebsocketsMessage
from packages.eightballer.skills.concentration_api.dialogues import (
    LedgerApiDialogue,
    LedgerApiDialogues,
)
from packages.eightballer.skills.concentration_api.strategy import Strategy
from packages.valory.connections.ledger.connection import (
    PUBLIC_ID as LEDGER_CONNECTION_PUBLIC_ID,
)
from packages.valory.protocols.ledger_api.message import LedgerApiMessage

LEDGER_API_ADDRESS = str(LEDGER_CONNECTION_PUBLIC_ID)
DEFAULT_MAX_PROCESSING = 20.0
DEFAULT_TX_INTERVAL = 2.0


class TransactionBehaviour(TickerBehaviour):
    """A behaviour to sequentially submit transactions to the blockchain."""

    def __init__(self, **kwargs: Any):
        """Initialize the transaction behaviour."""
        tx_interval = cast(
            float, kwargs.pop("transaction_interval", DEFAULT_TX_INTERVAL)
        )
        self.max_processing = cast(
            float, kwargs.pop("max_processing", DEFAULT_MAX_PROCESSING)
        )
        self.processing_time = 0.0
        self.waiting: List[FipaDialogue] = []
        self.processing: Optional[LedgerApiDialogue] = None
        self.timedout: Set[Any] = set()
        super().__init__(tick_interval=tx_interval, **kwargs)

    def setup(self) -> None:
        """Setup behaviour."""

    def act(self) -> None:
        """Implement the act."""
        if self.processing is not None:
            if self.processing_time <= self.max_processing:
                # already processing
                self.processing_time += self.tick_interval
                self.check_processing()
                return
            self._timeout_processing()
        if len(self.waiting) == 0:
            # nothing to process
            return
        self._start_processing()

    def teardown(self) -> None:
        """Teardown behaviour."""

    def _timeout_processing(self) -> None:
        """Timeout processing."""
        if self.processing is None:
            return
        self.context.logger.warning(
            f"Transaction processing timeout assuming failed: {self.processing.dialogue_label}"
        )
        self.timedout.add(self.processing.dialogue_label)
        self.processing_time = 0.0
        self.processing = None

    def check_processing(self) -> None:
        """Check processing."""
        # we submit the ledger api message and check if it has been processed
        try:
            msg = getattr(self.context.price_routing_strategy, "current_tx")
            if msg is None:
                return
        except AttributeError:
            return
        self.context.send_to_skill(msg)


    def finish_processing(self, ledger_api_dialogue: LedgerApiDialogue) -> None:
        """
        Finish processing.

        :param ledger_api_dialogue: the ledger api dialogue
        """

        response = ledger_api_dialogue.initial_ledger_api_dialogue

        if self.processing == response:
            self.processing_time = 0.0
            self.processing = None
            return
        
        # we check if the dialogue is 
        
        if ledger_api_dialogue.dialogue_label not in self.timedout:
            return
        self.timedout.remove(ledger_api_dialogue.dialogue_label)
        self.context.logger.debug(
            f"Timeout dialogue in transaction processing: {ledger_api_dialogue}"
        )

    def _start_processing(self) -> None:
        """Process the next transaction."""
        terms, raw_tx = self.waiting.pop(0)
        self.context.logger.info(
            f"Processing transaction, {len(self.waiting)} transactions remaining"
        )
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        ledger_api_msg, ledger_api_dialogue = ledger_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=LedgerApiMessage.Performative.GET_RAW_TRANSACTION,
            terms=terms,

        )
        ledger_api_dialogue.raw_tx = raw_tx
        ledger_api_dialogue.terms = terms
        ledger_api_dialogue = cast(LedgerApiDialogue, ledger_api_dialogue)
        self.processing_time = 0.0
        self.processing = ledger_api_dialogue
        self.context.logger.info(
            f"requesting transfer transaction for address: {terms.counterparty_address}..."
        )
        self.context.outbox.put_message(message=ledger_api_msg)

    def failed_processing(self, ledger_api_dialogue: LedgerApiDialogue) -> None:
        """
        Failed processing. Currently, we retry processing indefinitely.

        :param ledger_api_dialogue: the ledger api dialogue
        """
        self.finish_processing(ledger_api_dialogue)


class BalanceCheckBehaviour(TickerBehaviour):
    """This class implements a search behaviour."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the search behaviour."""
        super().__init__(**kwargs)

    def setup(self) -> None:
        """Implement the setup for the behaviour."""
        strategy = cast(Strategy, self.context.strategy)
        address = cast(str, self.context.agent_addresses.get(strategy.ledger_id))
        self.context.logger.info(f"I am in control of {address}")
        self.request_balance(address)

    def request_balance(self, address):
        """Submit a balance request to the ledger api."""
        strategy = cast(Strategy, self.context.strategy)
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        ledger_api_msg, _ = ledger_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=LedgerApiMessage.Performative.GET_BALANCE,
            ledger_id=strategy.ledger_id,
            address=address,
        )
        self.context.outbox.put_message(message=ledger_api_msg)

    def act(self) -> None:
        """Implement the act."""

    def teardown(self) -> None:
        """Implement the task teardown."""

class TrendingApi(TickerBehaviour):
    """This class implements a search behaviour."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the search behaviour."""
        super().__init__(**kwargs)

    def setup(self) -> None:
        """Implement the setup for the behaviour."""
        strategy = cast(Strategy, self.context.strategy)
        address = cast(str, self.context.agent_addresses.get(strategy.ledger_id))
        self.context.logger.info(f"I am in control of {address}")
        self.request_balance(address)

    def request_balance(self, address):
        """Submit a balance request to the ledger api."""
        strategy = cast(Strategy, self.context.strategy)
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.http_dialogues
        )
        ledger_api_msg, _ = ledger_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=LedgerApiMessage.Performative.GET_BALANCE,
            ledger_id=strategy.ledger_id,
            address=address,
        )
        self.context.outbox.put_message(message=ledger_api_msg)

    def act(self) -> None:
        """Implement the act."""

    def teardown(self) -> None:
        """Implement the task teardown."""

class SignalBehaviour(TickerBehaviour):
    """This class implements a search behaviour."""

    def setup(self):
        """
        Implement the setup.
        """
        self.strategy = self.context.strategy
        self.client_to_lines = {}

    def act(self):
        """
        We read in the log file and send the new lines to the client.
        We do so in an efficent manner, only reading the new lines.
        we make sure to send a message to all clients.
        """

        msg = json.dumps({'intention': random.choice(['LEFT', 'RIGHT'])})


        for _, dialogue in self.strategy.clients.items():
            self.send_message(msg, dialogue)

    def teardown(self):
        """
        Implement the handler teardown.
        """

    def send_message(self, data, dialogue):
        """
        Send a message to the client.
        """
        msg = dialogue.reply(
            performative=WebsocketsMessage.Performative.SEND,
            data=data,
        )
        self.context.outbox.put_message(message=msg)

    def __init__(self, tick_interval: float = 5, start_at: datetime | None = None, **kwargs: Any) -> None:
        super().__init__(tick_interval, start_at, **kwargs)