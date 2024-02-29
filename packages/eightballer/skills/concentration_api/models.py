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

"""This module contains the db models for the 'faucet' skill."""

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BanList(Base):  # type: ignore
    """Represents a banned address."""

    __tablename__ = "BanList"

    id = Column(Numeric, primary_key=True)
    public_address = Column(Numeric)


class DripRequest(Base):  # type: ignore
    """Represents a claim from the faucet."""

    __tablename__ = "DripRequests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP)
    public_address = Column(String)
    valid_request = Column(Boolean)
    ledger_id = Column(String)

    def as_dict(self):
        datetime_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "id": self.id,
            "created_at": datetime_str,
            "public_address": self.public_address,
            "valid_request": self.valid_request,
            "ledger_id": self.ledger_id,
        }


class AllowList(Base):  # type: ignore
    """Represents a whitelisted address."""

    __tablename__ = "WhiteList"

    id = Column(Numeric, primary_key=True)
    public_address = Column(Numeric)
