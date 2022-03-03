#!/usr/bin/env python3

from __future__ import annotations

from expaql.api import ExpaQuery
from expaql.formaters import OpportunityApplicationFormatter
from config import IgvToolConfig
from gql.transport.requests import log as gql_logger
from trello_conn import TrelloConn

import logging
import atexit

config = IgvToolConfig()
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%I:%M:%S",
    level=config.log_level,
)
gql_logger.setLevel(logging.WARNING)

expaql: ExpaQuery | None = None


def main() -> None:
    global expaql

    with open(config.token_file, "r") as f:
        refresh_token = f.read().strip()

    expaql = ExpaQuery(
        config.expa_client_id, config.expa_client_secret, refresh_token
    )

    trello = TrelloConn(config.trello_api_key, config.trello_token, config.trello_board_id)
    i = 0
    for x in expaql.get_applications():
        formatter = OpportunityApplicationFormatter(x)
        # print(formatter.format_markdown())
        trello.add_new_card(formatter)
        i += 1


def exit_handler() -> None:
    global expaql

    if expaql is not None:
        with open(config.token_file, "w") as f:
            f.write(expaql.get_refresh_token())


if __name__ == "__main__":
    atexit.register(exit_handler)
    try:
        main()
    except Exception as e:
        logging.fatal(e, exc_info=True)
