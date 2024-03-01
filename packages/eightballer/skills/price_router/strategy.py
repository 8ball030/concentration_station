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

"""This package contains a scaffold of a model."""

from typing import Any, Dict
from aea.skills.base import Model
from aea_ledger_ethereum import LedgerApi
from aea.crypto.ledger_apis import LedgerApis
from packages.eightballer.protocols.orders.custom_types import Order

from packages.open_aea.protocols.signing.custom_types import Terms


class PriceRoutingStrategy(Model):
    """This class scaffolds a model."""

    ledger_ids = []
    token_ids = []
    api_routers = []
    base_currency: str = "USD"

    prepared_transactions = {}



    def __init__(self, **kwargs):
        """Initialize the strategy."""
        super().__init__(**kwargs)
        self.token_ids = kwargs.pop("token_ids", [])
        self.ledger_ids = kwargs.pop("ledger_ids", [])
        self.api_routers = kwargs.pop("api_routers", [])
        self.base_currency = kwargs.pop("base_currency", "USD")


    def get_swap_terms(self, raw_tx: Dict, ledger_id: str) -> Terms:
        """Get the terms of a drop"""
        ledger = LedgerApis.get_api("ethereum")
        currency_id = self.context.shared_state['ledgers'][ledger_id].native_currency
        fee, amount, address = int(raw_tx.get("gas", 0)), int(raw_tx.get("value", 0)), raw_tx.get("to")
        try:
            tx_nonce = ledger.generate_tx_nonce( seller=self.context.agent_address, client=address,)
        except AttributeError:
            self.context.logger.error(f"Invalid transaction: {raw_tx}")
            return

        if not all([fee, amount]):
            self.context.logger.error(f"Invalid transaction: {raw_tx}")
            return 

        terms = Terms(
            ledger_id=ledger_id,
            sender_address=self.context.agent_address,
            counterparty_address=address,
            amount_by_currency_id={currency_id: int(f"-{amount}")},
            fee_by_currency_id={currency_id: int(fee)},
            quantities_by_good_id={currency_id: int(amount)},
            is_sender_payable_tx_fee=True,
            nonce=str(tx_nonce),
        )
        return terms