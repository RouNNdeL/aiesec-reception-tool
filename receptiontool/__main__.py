#!/usr/bin/env python3

from __future__ import annotations

import atexit
import logging
from gql.transport.requests import log as gql_logger
from receptiontool.trello_conn import TrelloConn

from receptiontool.config import IgvToolConfig
from receptiontool.expaql.api import ExpaQuery

config = IgvToolConfig()
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%I:%M:%S",
    level=config.log_level,
)
gql_logger.setLevel(logging.WARNING)

expaql: ExpaQuery | None = None


def check_for_updates() -> None:
    global expaql

    with open(config.token_file, "r") as f:
        refresh_token = f.read().strip()

    expaql = ExpaQuery(
        config.expa.client_id, config.expa.client_secret, refresh_token
    )

    trello = TrelloConn(config.trello.api_key, config.trello.token, config.trello.board_id)
    trello.add_list_of_cards(applications=expaql.get_applications())


def exit_handler() -> None:
    global expaql

    if expaql is not None:
        with open(config.token_file, "w") as f:
            f.write(expaql.get_refresh_token())


def entrypoint() -> None:
    logging.info("Starting receptiontool")
    atexit.register(exit_handler)
    try:
        check_for_updates()
    except Exception as e:
        logging.fatal(e, exc_info=True)
