# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
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

"""
Module contains the classes required for dialogue management.

- Dialogue: The dialogue class maintains state of a dialogue and manages it.
- Dialogues: The dialogues class keeps track of all dialogues.
"""

from typing import Any, Type

from aea.exceptions import enforce
from aea.helpers.transaction.base import Terms
from aea.protocols.base import Address, Message
from aea.protocols.dialogue.base import Dialogue as BaseDialogue
from aea.protocols.dialogue.base import DialogueLabel as BaseDialogueLabel
from aea.skills.base import Model

from packages.eightballer.protocols.http.dialogues import (
    HttpDialogue as BaseHttpDialogue,
)
from packages.eightballer.protocols.http.dialogues import (
    HttpDialogues as BaseHttpDialogues,
)
from packages.eightballer.protocols.orders.dialogues import (
    OrdersDialogue as BaseOrdersDialogue,
)
from packages.eightballer.protocols.orders.dialogues import (
    OrdersDialogues as BaseOrdersDialogues,
)
from packages.eightballer.skills.concentration_api.dialogues import (
    LedgerApiDialogue as BaseLedgerDialogue,
)
from packages.eightballer.skills.concentration_api.dialogues import (
    LedgerApiDialogues as BaseLedgerDialogues,
)
from packages.eightballer.skills.concentration_api.dialogues import (
    SigningDialogue as BaseSigningDialogue,
)
from packages.eightballer.skills.concentration_api.dialogues import (
    SigningDialogues as BaseSigningDialogues,
)



HttpDialogue = BaseHttpDialogue


OrdersDialogue = BaseOrdersDialogue
OrdersDialogues = BaseOrdersDialogues

LedgerApiDialogue = BaseLedgerDialogue
LedgerApiDialogues = BaseLedgerDialogues

SigningDialogue = BaseSigningDialogue
SigningDialogues = BaseSigningDialogues

class HttpDialogues(Model, BaseHttpDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.

        :param kwargs: keyword arguments
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            return BaseHttpDialogue.Role.SERVER

        BaseHttpDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
        )


