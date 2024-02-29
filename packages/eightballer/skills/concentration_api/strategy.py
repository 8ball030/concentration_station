# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
#   Copyright 2018-2021 Fetch.AI Limited
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

"""This module contains the strategy for the 'faucet' skill."""

from datetime import datetime, timedelta
from typing import Any

from aea.crypto.ledger_apis import LedgerApis
from aea.helpers.transaction.base import Terms
from aea.skills.base import Model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from packages.eightballer.skills.concentration_api.models import (
    AllowList,
    BanList,
    Base,
    DripRequest,
)


class Strategy(Model):  # pylint: disable=too-many-instance-attributes
    """This class defines a strategy for the agent."""

    _balance: int
    clients = {}

    @property
    def balance(self) -> int:
        """Get the balance of the agent."""
        return self._balance

    @property
    def ledger_id(self) -> str:
        """Get the ledger id."""
        return self._ledger_id

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the strategy of the agent.

        :param kwargs: keyword arguments
        """
        self._service_id = "eeg"
        self._currency_id = "ETH"
        self._allow_list = kwargs.pop("allow_list", [])
        self._ban_list = kwargs.pop("ban_list", [])
        self.max_requests_per_day = kwargs.pop("max_requests_per_day", 1)
        self.gwei_per_request = kwargs.pop("gwei_per_request", 1)
        ledger_id = kwargs.pop("ledger_id", None)
        uri_string = kwargs.pop("database_uri_string", None)

        super().__init__(**kwargs)
        self._setup_database(uri_string)
        self._ledger_id = (
            ledger_id if ledger_id is not None else self.context.default_ledger_id
        )

    def _setup_database(self, uri_string) -> None:
        """Set up the database and ensure all tables are created."""
        self.engine = create_engine(uri_string)
        Base.metadata.create_all(self.engine)
        # create session
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def is_request_valid(self, address, ledger_id) -> bool:
        """Checks if a faucet request is valid."""
        if self.is_address_allowed(address):
            return True
        if all(
            [
                not self.is_address_banned(address),
                not self.has_address_over_claimed_within_timeframe(address, ledger_id),
            ]
        ):
            return True
        return False

    def is_address_allowed(self, address) -> bool:
        """Check whether the address is within the allowed list."""
        return address in self.allow_list

    def is_address_banned(self, address) -> bool:
        """Check whether the address is within the ban list."""
        return address in self.ban_list

    def has_address_over_claimed_within_timeframe(self, address, ledger_id) -> bool:
        """Cracked."""
        end = datetime.now()
        start = end - timedelta(days=1)
        results = (
            self.session.query(DripRequest)
            .filter(DripRequest.public_address == address)
            .filter(DripRequest.created_at.between(start, end))
            .filter(DripRequest.valid_request is True)
            .filter(DripRequest.ledger_id == ledger_id)
        )
        self.context.logger.info(f"Successfully claimed: {len(results.all())} today.")
        return len(results.all()) >= self.max_requests_per_day

    def add_drip_request(self, address: str, valid: bool, ledger_id: str) -> None:
        """Cracked."""
        request = DripRequest(
            created_at=datetime.now(),
            public_address=address,
            valid_request=valid,
            ledger_id=ledger_id,
        )
        self.session.add(request)
        self.session.commit()

    def get_drip_terms(self, address, ledger_id: str) -> Terms:
        """Get the terms of a drop"""
        tx_nonce = LedgerApis.generate_tx_nonce(
            identifier=self.ledger_id,
            seller=self.context.agent_address,
            client=address,
        )

        currency_id = self.context.shared_state['ledgers'][ledger_id].native_currency
        terms = Terms(
            ledger_id=ledger_id,
            sender_address=self.context.agent_address,
            counterparty_address=address,
            amount_by_currency_id={currency_id: -self.gwei_per_request},
            fee_by_currency_id={currency_id: 210000},
            quantities_by_good_id={currency_id: self.gwei_per_request},
            is_sender_payable_tx_fee=True,
            nonce=tx_nonce,
        )
        return terms

    @property
    def allow_list(self) -> list:
        """Get the allow list from the strategy and the database."""
        return self._allow_list + [
            i.public_address for i in self.session.query(AllowList).all()
        ]

    @property
    def ban_list(self) -> list:
        """Get the ban list from the strategy and the database."""
        return self._ban_list + [
            i.public_address for i in self.session.query(BanList).all()
        ]

    def get_txs(self):
        """Get the transactions from the database."""
        return self.session.query(DripRequest).all()