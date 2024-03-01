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

"""This module contains the handler for the 'faucet' skill."""
# pylint: disable=W0212,C0209

from dataclasses import asdict
import json
from typing import Dict, Optional, Union, cast

from aea.crypto.ledger_apis import LedgerApis
from aea.protocols.base import Message
from aea.skills.base import Handler

from packages.eightballer.protocols.default import DefaultMessage
from packages.eightballer.protocols.http.message import HttpMessage
from packages.eightballer.protocols.websockets.dialogues import WebsocketsDialogue, WebsocketsDialogues
from packages.eightballer.protocols.websockets.message import WebsocketsMessage
from packages.eightballer.skills.balance_metrics.strategy import Balance
from packages.eightballer.skills.concentration_api.behaviours import TransactionBehaviour
from packages.eightballer.skills.concentration_api.dialogues import (
    DefaultDialogues,
    HttpDialogue,
    HttpDialogues,
    LedgerApiDialogue,
    LedgerApiDialogues,
    SigningDialogue,
    SigningDialogues,
)
from packages.eightballer.skills.concentration_api.strategy import Strategy
from packages.open_aea.protocols.signing.message import SigningMessage
from packages.valory.connections.ledger.base import EVM_LEDGERS
from packages.valory.connections.ledger.tests.conftest import make_ledger_api_connection
from packages.valory.protocols.ledger_api.message import LedgerApiMessage


class EvmLedgerApis(LedgerApis):
    """Store all the ledger apis we initialise."""
    ledger_api_configs: Dict[str, Dict[str, Union[str, int]]] = EVM_LEDGERS

    @classmethod
    def get_api(cls, identifier: str):
        """Get the ledger API."""
        api = make_ledger_api_connection(identifier, **cls.ledger_api_configs[identifier])
        return api

class HttpHandler(Handler):
    """This implements the echo handler."""

    SUPPORTED_PROTOCOL = HttpMessage.protocol_id

    def setup(self) -> None:
        """Implement the setup."""
        self.context.logger.info(f"HttpHandler: setup method called. to procol_id={HttpMessage.protocol_id}")
        super().setup()

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        http_msg = cast(HttpMessage, message)

        # recover dialogue
        http_dialogues = cast(HttpDialogues, self.context.http_dialogues)
        http_dialogue = cast(HttpDialogue, http_dialogues.update(http_msg))
        if http_dialogue is None:
            self._handle_unidentified_dialogue(http_msg)
            return

        # handle message
        if http_msg.performative == HttpMessage.Performative.REQUEST:
            self._handle_request(http_msg, http_dialogue)
        else:
            self._handle_invalid(http_msg, http_dialogue)

    def _handle_unidentified_dialogue(self, http_msg: HttpMessage) -> None:
        """
        Handle an unidentified dialogue.

        :param http_msg: the message
        """
        self.context.logger.info(
            "received invalid http message={}, unidentified dialogue.".format(http_msg)
        )
        default_dialogues = cast(DefaultDialogues, self.context.default_dialogues)
        default_msg, _ = default_dialogues.create(
            counterparty=http_msg.sender,
            performative=DefaultMessage.Performative.ERROR,
            error_code=DefaultMessage.ErrorCode.INVALID_DIALOGUE,
            error_msg="Invalid dialogue.",
            error_data={"http_message": http_msg.encode()},
        )
        self.context.outbox.put_message(message=default_msg)

    def _handle_request(
        self, http_msg: HttpMessage, http_dialogue: HttpDialogue
    ) -> None:
        """
        Handle a Http request.

        :param http_msg: the http message
        :param http_dialogue: the http dialogue
        """
        self.context.logger.info(
            "received http request with method={}, url={} and body={!r}".format(
                http_msg.method,
                http_msg.url,
                http_msg.body,
            )
        )

        if "Upgrade: websocket" in http_msg.headers:
            self.context.strategy.clients[
                http_dialogue.incomplete_dialogue_label.get_incomplete_version().dialogue_reference[
                    0
                ] 
            ] = http_dialogue
            
            self.context.logger.debug(f"Total clients: {len(self.context.strategy.clients)}")
            return

        if http_msg.method == "post":
            self._handle_swipe(http_msg, http_dialogue)
        elif http_msg.method == "options":
            self._handle_pre_flight(http_msg, http_dialogue)
        elif http_msg.url.find("ledgers") >= 0 and http_msg.method == "get":
            self._return_ledgers(http_msg, http_dialogue)
        elif http_msg.url.find("transactions") >= 0 and http_msg.method == "get":
            self._return_txs(http_msg, http_dialogue)
        elif http_msg.url.find("current_coin") >= 0 and http_msg.method == "get":
            self._return_current_coin(http_msg, http_dialogue)
        else:
            self._handle_invalid(http_msg, http_dialogue)

    def _return_ledgers(
        self, http_msg: HttpMessage, http_dialogue: HttpDialogue
    ) -> None:
        """
        Handle a Http request of verb GET.

        :param http_msg: the http message
        :param http_dialogue: the http dialogue
        """
        shared_state = cast(Strategy, self.context.shared_state)
        ledgers = shared_state.get("ledgers")
        http_response = http_dialogue.reply(
            performative=HttpMessage.Performative.RESPONSE,
            target_message=http_msg,
            version=http_msg.version,
            status_code=200,
            status_text="",
            headers=self._get_cors_headers(http_msg),
            body=json.dumps({"ledgers": {i: asdict(k) for i, k in ledgers.items()}}).encode("utf-8"),
        )
        self.context.outbox.put_message(message=http_response)
    
    def _return_txs(
        self, http_msg: HttpMessage, http_dialogue: HttpDialogue
    ) -> None:
        """
        Handle a Http request of verb GET.

        :param http_msg: the http message
        :param http_dialogue: the http dialogue
        """
        txs = self.context.strategy.get_txs()
        txs = [{
            "chain_id": "1",
            "tx_hash": "0x1234567890",
            "block_explorer_url": "https://etherscan.io/txs/0x1234567890",
        }]
        http_response = http_dialogue.reply(
            performative=HttpMessage.Performative.RESPONSE,
            target_message=http_msg,
            version=http_msg.version,
            status_code=200,
            status_text="",
            headers=self._get_cors_headers(http_msg),
            body=json.dumps([f for f in txs]).encode("utf-8"),
        )
        self.context.outbox.put_message(message=http_response)

    def _return_current_coin(
        self, http_msg: HttpMessage, http_dialogue: HttpDialogue
    ) -> None:
        """
        Handle a Http request of verb GET.

        :param http_msg: the http message
        :param http_dialogue: the http dialogue
        """
        whitelist = self.context.strategy.allow_list
        http_response = http_dialogue.reply(
            performative=HttpMessage.Performative.RESPONSE,
            target_message=http_msg,
            version=http_msg.version,
            status_code=200,
            status_text="",
            headers=self._get_cors_headers(http_msg),
            body=json.dumps(self.context.strategy.current_coin).encode("utf-8"),
        )
        self.context.outbox.put_message(message=http_response)

    
    def _get_cors_headers(self, http_msg: HttpMessage) -> str:
        """
        returns the expected cors headers
        """
        cors_headers = "Access-Control-Allow-Origin: *\n"
        cors_headers += "Access-Control-Allow-Methods: GET,POST\n"
        cors_headers += "Access-Control-Allow-Headers: Content-Type,Accept\n"

        return  f"{cors_headers}{http_msg.headers}"

    def _handle_pre_flight(
        self, http_msg: HttpMessage, http_dialogue: HttpDialogue
    ) -> None:
        """
        Handle a Http request of verb OPTIONS.

        :param http_msg: the http message
        :param http_dialogue: the http dialogue
        """


        http_response = http_dialogue.reply(
            performative=HttpMessage.Performative.RESPONSE,
            target_message=http_msg,
            version=http_msg.version,
            status_code=200,
            status_text="",
            headers=self._get_cors_headers(http_msg=http_msg),
            body=b"",
        )
        self.context.outbox.put_message(message=http_response)

    def _handle_swipe(self, http_msg: HttpMessage, http_dialogue: HttpDialogue) -> None:
        """
        Handle a Http request of verb GET.

        :param http_msg: the http message
        :param http_dialogue: the http dialogue
        """
        strategy = cast(Strategy, self.context.strategy)
        payload = json.loads(http_msg.body)
        address = payload.get("public_address")
        status_text = "Unsuccessful"
        valid = False

        ledgers = self.context.shared_state.get("ledgers")
        native_balances = self.context.shared_state.get("balances")

        direction = payload.get("direction")
        coin_id = payload.get("coin_id")
        ledger_id = payload.get("ledger_id", "ethereum")

        strategy._current_coin = strategy.get_new_coin()


        status_text = "Success!"
            # valid = strategy.is_request_valid(address, request_ledger)
        # if valid:
        #     self.context.logger.info(
        #         f"Address {address} successfully claimed. Preparing TX."
        #     )

        #     native_balance = native_balances.get(request_ledger)

        #     self.context.logger.info(
        #         f"Native balance on {request_ledger} ledger is {native_balance}"
        #     )

        #     if not isinstance(int(native_balance.amount), int):
        #         status_text = "Pending ledger balance"
        #     elif native_balance is None:
        #         status_text = "Invalid ledger"
        #     elif native_balance.amount < strategy.gwei_per_request:
        #         status_text = "Insufficient funds in faucet"
        #     else:
        #         status_text = "Success! Please await transaction confirmation."
        #         self._make_transfer(address, request_ledger)
        # else:
        #     status_text = "Address has already claimed today."
            
        http_response = http_dialogue.reply(
            performative=HttpMessage.Performative.RESPONSE,
            target_message=http_msg,
            version=http_msg.version,
            status_code=201,
            status_text=status_text,
            headers=self._get_cors_headers(http_msg),
            body=json.dumps({"result": status_text}).encode("utf-8"),
        )
        self.context.logger.info("responding with: {}".format(status_text))
        self.context.outbox.put_message(message=http_response)
        # strategy.add_drip_request(address, valid, ledger_id=ledger_id)

    def _handle_invalid(
        self, http_msg: HttpMessage, http_dialogue: HttpDialogue
    ) -> None:
        """
        Handle an invalid http message.

        :param http_msg: the http message
        :param http_dialogue: the http dialogue
        """
        self.context.logger.warning(
            "cannot handle http message of performative={} method={} url={} dialogue={}".format(
                http_msg.performative, http_msg.method, http_msg.url, http_dialogue
            )
        )

    def teardown(self) -> None:
        """Implement the handler teardown."""

    def _make_transfer(self, address, ledger_id):
        self.context.logger.info(f"Preparing a drip tx to {address} on {ledger_id}")
        strategy = cast(Strategy, self.context.strategy)
        terms = strategy.get_drip_terms(address, ledger_id=ledger_id)
        tx_behaviour = cast(TransactionBehaviour, self.context.behaviours.transaction)
        tx_behaviour.waiting.append(terms)


class LedgerApiHandler(Handler):
    """Implement the ledger handler."""

    SUPPORTED_PROTOCOL = LedgerApiMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """Implement the setup for the handler."""

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        """
        ledger_api_msg = cast(LedgerApiMessage, message)

        # recover dialogue
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        ledger_api_dialogue = cast(
            Optional[LedgerApiDialogue], ledger_api_dialogues.update(ledger_api_msg)
        )
        if ledger_api_dialogue is None:
            self._handle_unidentified_dialogue(ledger_api_msg)
            return

        # handle message
        if ledger_api_msg.performative is LedgerApiMessage.Performative.BALANCE:
            self._handle_balance(ledger_api_msg)
        elif (
            ledger_api_msg.performative is LedgerApiMessage.Performative.RAW_TRANSACTION
        ):
            self._handle_raw_transaction(ledger_api_msg, ledger_api_dialogue)
        elif (
            ledger_api_msg.performative
            == LedgerApiMessage.Performative.TRANSACTION_DIGEST
        ):
            self._handle_transaction_digest(ledger_api_msg, ledger_api_dialogue)
        elif (
            ledger_api_msg.performative
            == LedgerApiMessage.Performative.TRANSACTION_RECEIPT
        ):
            self._handle_transaction_receipt(ledger_api_msg, ledger_api_dialogue)
        elif ledger_api_msg.performative == LedgerApiMessage.Performative.ERROR:
            self._handle_error(ledger_api_msg, ledger_api_dialogue)
        else:
            self._handle_invalid(ledger_api_msg, ledger_api_dialogue)

    def teardown(self) -> None:
        """Implement the handler teardown."""

    def _handle_unidentified_dialogue(self, ledger_api_msg: LedgerApiMessage) -> None:
        """
        Handle an unidentified dialogue.

        :param ledger_api_msg: the message
        """
        self.context.logger.info(
            "received invalid ledger_api message={}, unidentified dialogue.".format(
                ledger_api_msg
            )
        )

    def _handle_balance(self, ledger_api_msg: LedgerApiMessage) -> None:
        """
        Handle a message of balance performative.

        :param ledger_api_msg: the ledger api message
        """
        strategy = cast(Strategy, self.context.strategy)
        if ledger_api_msg.balance > 0:
            self.context.logger.info(
                "starting balance on {} ledger={}.".format(
                    strategy.ledger_id,
                    ledger_api_msg.balance,
                )
            )
            strategy._balance = ledger_api_msg.balance
        else:
            self.context.logger.warning(
                f"you have no starting balance on {strategy.ledger_id} ledger! Stopping skill {self.skill_id}. "
            )
            # self.context.is_active = False

    def _handle_transaction_digest(
        self, ledger_api_msg: LedgerApiMessage, ledger_api_dialogue: LedgerApiDialogue
    ) -> None:
        """
        Handle a message of transaction_digest performative.

        :param ledger_api_msg: the ledger api message
        :param ledger_api_dialogue: the ledger api dialogue
        """
        self.context.logger.info(
            "transaction was successfully submitted. Transaction digest={}".format(
                ledger_api_msg.transaction_digest
            )
        )
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        ledger_api_msg, receipt_dialogue = ledger_api_dialogues.create(
            counterparty=ledger_api_msg.sender,
            performative=LedgerApiMessage.Performative.GET_TRANSACTION_RECEIPT,
            transaction_digest=ledger_api_msg.transaction_digest,
        )
        receipt_dialogue.terms = ledger_api_dialogue.terms
        receipt_dialogue.initial_ledger_api_dialogue = (
            ledger_api_dialogue.initial_ledger_api_dialogue
        )
        self.context.logger.info("checking transaction is settled.")
        self.context.outbox.put_message(message=ledger_api_msg)

    def _handle_error(
        self, ledger_api_msg: LedgerApiMessage, ledger_api_dialogue: LedgerApiDialogue
    ) -> None:
        """
        Handle a message of error performative.

        :param ledger_api_msg: the ledger api message
        :param ledger_api_dialogue: the ledger api dialogue
        """
        self.context.logger.info(
            "received ledger_api error message={} in dialogue={}.".format(
                ledger_api_msg, ledger_api_dialogue
            )
        )
        ledger_api_msg_ = cast(
            Optional[LedgerApiMessage], ledger_api_dialogue.last_outgoing_message
        )
        if (
            ledger_api_msg_ is not None
            and ledger_api_msg_.performative
            != LedgerApiMessage.Performative.GET_BALANCE
        ):
            tx_behaviour = cast(
                TransactionBehaviour, self.context.behaviours.transaction
            )
            tx_behaviour.failed_processing(ledger_api_dialogue)

    def _handle_invalid(
        self, ledger_api_msg: LedgerApiMessage, ledger_api_dialogue: LedgerApiDialogue
    ) -> None:
        """
        Handle a message of invalid performative.

        :param ledger_api_msg: the ledger api message
        :param ledger_api_dialogue: the ledger api dialogue
        """
        self.context.logger.warning(
            "cannot handle ledger_api message of performative={} in dialogue={}.".format(
                ledger_api_msg.performative,
                ledger_api_dialogue,
            )
        )

    def _handle_raw_transaction(
        self, ledger_api_msg: LedgerApiMessage, ledger_api_dialogue: LedgerApiDialogue
    ) -> None:
        """Handle a message of raw_transaction performative."""

        self.context.logger.debug("received raw transaction={}".format(ledger_api_msg))
        signing_dialogues = cast(SigningDialogues, self.context.signing_dialogues)

        # we have to do a hack here because api.get_transfer_transaction()
        # adds in data when transfering to SAFE contract.
        # this is a hack to remove that data.
        ledger_api_msg.raw_transaction._body["data"] = "0x"
        ledger_api_dialogue.initial_ledger_id = ledger_api_msg.raw_transaction.ledger_id
        ledger_api_msg.raw_transaction._ledger_id = "ethereum"
        signing_msg, signing_dialogue = signing_dialogues.create(
            counterparty=self.context.decision_maker_address,
            performative=SigningMessage.Performative.SIGN_TRANSACTION,
            raw_transaction=ledger_api_msg.raw_transaction,
            terms=ledger_api_dialogue.terms,
        )
        signing_dialogue = cast(SigningDialogue, signing_dialogue)
        signing_dialogue.associated_ledger_api_dialogue = ledger_api_dialogue
        self.context.decision_maker_message_queue.put_nowait(signing_msg)
        self.context.logger.info(
            "proposing the transaction to the decision maker. Waiting for confirmation ..."
        )

    def _handle_transaction_receipt(
        self, ledger_api_msg: LedgerApiMessage, ledger_api_dialogue: LedgerApiDialogue
    ) -> None:
        """
        Handle a message of balance performative.

        :param ledger_api_msg: the ledger api message
        :param ledger_api_dialogue: the ledger api dialogue
        """

        ledger = self.context.shared_state['ledgers'][ledger_api_dialogue.terms.ledger_id]
        self.context.logger.info(
            f"View the pending transaction on {ledger.explorer_url}/tx/{ledger_api_msg.transaction_receipt.receipt.get('transactionHash')}"
        )

        # ledger_api = EvmLedgerApis.get_api(ledger_api_dialogue.terms.ledger_id)

        # is_settled = TrueLedgerApis.is_transaction_settled(
        #     ledger_api_dialogue.terms.ledger_id,
        #     ledger_api_msg.transaction_receipt.receipt,
        # )
        is_settled = True
        tx_behaviour = cast(TransactionBehaviour, self.context.behaviours.transaction)
        initial_ledger_api_dialogue = cast(
            LedgerApiDialogue, ledger_api_dialogue.initial_ledger_api_dialogue
        )
        if is_settled:
            tx_behaviour.finish_processing(initial_ledger_api_dialogue)
            self.context.logger.info(
                "Transaction {} is settled!".format(
                    ledger_api_msg.transaction_receipt.receipt.get("transactionHash")
                )
            )
        else:
            tx_behaviour.failed_processing(initial_ledger_api_dialogue)
            self.context.logger.info(
                "Transaction {} is not valid or settled! Aborting...".format(
                    ledger_api_msg.transaction_receipt.receipt.get("transactionHash")
                )
            )


class SigningHandler(Handler):
    """Implement the signing handler."""

    SUPPORTED_PROTOCOL = SigningMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """Implement the setup for the handler."""

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        """
        signing_msg = cast(SigningMessage, message)

        # recover dialogue
        signing_dialogues = cast(SigningDialogues, self.context.signing_dialogues)
        signing_dialogue = cast(
            Optional[SigningDialogue], signing_dialogues.update(signing_msg)
        )
        if signing_dialogue is None:
            self._handle_unidentified_dialogue(signing_msg)
            return

        # handle message
        if signing_msg.performative is SigningMessage.Performative.SIGNED_TRANSACTION:
            self._handle_signed_transaction(signing_msg, signing_dialogue)
        elif signing_msg.performative is SigningMessage.Performative.ERROR:
            self._handle_error(signing_msg, signing_dialogue)
        else:
            self._handle_invalid(signing_msg, signing_dialogue)

    def teardown(self) -> None:
        """Implement the handler teardown."""

    def _handle_unidentified_dialogue(self, signing_msg: SigningMessage) -> None:
        """
        Handle an unidentified dialogue.

        :param signing_msg: the message
        """
        self.context.logger.info(
            f"received invalid signing message={signing_msg}, unidentified dialogue."
        )

    def _handle_signed_transaction(
        self, signing_msg: SigningMessage, signing_dialogue: SigningDialogue
    ) -> None:
        """
        Handle an oef search message.

        :param signing_msg: the signing message
        :param signing_dialogue: the dialogue
        """
        self.context.logger.info("transaction signing was successful.")
        ledger_api_dialogue = signing_dialogue.associated_ledger_api_dialogue
        last_ledger_api_msg = ledger_api_dialogue.last_incoming_message
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        if last_ledger_api_msg is None:
            raise ValueError("Could not retrieve last message in ledger api dialogue")

        ledger_api_msg, submission_dialogue = ledger_api_dialogues.create(
            counterparty=last_ledger_api_msg.sender,
            performative=LedgerApiMessage.Performative.SEND_SIGNED_TRANSACTION,
            signed_transaction=signing_msg.signed_transaction,
        )
        ledger_api_msg.signed_transaction._ledger_id = ledger_api_dialogue.initial_ledger_id
        submission_dialogue.terms = ledger_api_dialogue.terms
        submission_dialogue.initial_ledger_api_dialogue = ledger_api_dialogue
        self.context.outbox.put_message(message=ledger_api_msg)
        self.context.logger.info("sending transaction to ledger.")

    def _handle_error(
        self, signing_msg: SigningMessage, signing_dialogue: SigningDialogue
    ) -> None:
        """
        Handle an oef search message.

        :param signing_msg: the signing message
        :param signing_dialogue: the dialogue
        """
        self.context.logger.info(
            f"transaction signing was not successful. Error_code={signing_msg.error_code}"
            + f" signing_dialogue={signing_dialogue}"
        )
        signing_msg_ = cast(
            Optional[SigningMessage], signing_dialogue.last_outgoing_message
        )
        if (
            signing_msg_ is not None
            and signing_msg_.performative
            == SigningMessage.Performative.SIGN_TRANSACTION
        ):
            tx_behaviour = cast(
                TransactionBehaviour, self.context.behaviours.transaction
            )
            ledger_api_dialogue = signing_dialogue.associated_ledger_api_dialogue
            tx_behaviour.failed_processing(ledger_api_dialogue)

    def _handle_invalid(
        self, signing_msg: SigningMessage, signing_dialogue: SigningDialogue
    ) -> None:
        """
        Handle an oef search message.

        :param signing_msg: the signing message
        :param signing_dialogue: the dialogue
        """
        self.context.logger.warning(
            f"cannot handle signing message of performative={signing_msg.performative} in dialogue={signing_dialogue}."
        )



class WebSocketHandler(HttpHandler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = WebsocketsMessage.protocol_id

    @property
    def strategy(self) -> "Strategy":
        """Get the strategy."""
        return cast(Strategy, self.context.strategy)

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        if message.performative == WebsocketsMessage.Performative.CONNECT:
            return self._handle_connect(message)

        dialogue = self.context.websocket_dialogues.get_dialogue(message)

        if message.performative == WebsocketsMessage.Performative.DISCONNECT:
            return self._handle_disconnect(message, dialogue)
        # it is an existing dialogue
        if dialogue is None:
            self.context.logger.error(
                "Could not locate dialogue for message={}".format(message)
            )
            return None
        if message.performative == WebsocketsMessage.Performative.SEND:
            return self._handle_send(message, dialogue)
        self.context.logger.warning(
            "Cannot handle websockets message of performative={}".format(
                message.performative
            )
        )
        return None

    def _handle_disconnect(
        self, message: Message, dialogue: WebsocketsDialogue
    ) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        self.context.logger.info(
            "Handling disconnect message in skill: {}".format(message)
        )
        ws_dialogues_to_connections = {
            v.incomplete_dialogue_label: k for k, v in self.strategy.clients.items()
        }
        if dialogue.incomplete_dialogue_label in ws_dialogues_to_connections:
            del self.strategy.clients[
                ws_dialogues_to_connections[dialogue.incomplete_dialogue_label]
            ]
            self.context.logger.info(f"Total clients: {len(self.strategy.clients)}")
        else:
            self.context.logger.warning(
                f"Could not find dialogue to disconnect: {dialogue.incomplete_dialogue_label}"
            )

    def _handle_send(self, message: Message, dialogue) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        self.context.logger.info(
            "Handling ping message in skill: {}".format(message.data)
        )
        pong_message = dialogue.reply(
            performative=WebsocketsMessage.Performative.SEND,
            target_message=dialogue.last_message,
            data=message.data + " pong",
        )
        self.context.outbox.put_message(message=pong_message)

    @property
    def websocket_dialogues(self) -> "WebsocketsDialogues":
        """Get the http dialogues."""
        return cast(WebsocketsDialogues, self.context.websocket_dialogues)

    def _handle_connect(self, message: Message) -> None:
        """
        Implement the reaction to the connect message.
        """

        dialogue: WebsocketsDialogue = self.websocket_dialogues.get_dialogue(message)

        if dialogue is not None:
            self.context.logger.debug(
                "Already have a dialogue for message={}".format(message)
            )
            return
        # we need to create a new dialogue
        client_reference = message.url
        dialogue = self.websocket_dialogues.update(message)
        response_msg = dialogue.reply(
            performative=WebsocketsMessage.Performative.CONNECTION_ACK,
            success=True,
            target_message=message,
        )
        self.context.logger.info(
            "Handling connect message in skill: {}".format(client_reference)
        )
        self.strategy.clients[client_reference] = dialogue
        self.context.outbox.put_message(message=response_msg)