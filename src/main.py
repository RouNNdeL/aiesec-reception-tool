#!/usr/bin/env python3

from __future__ import annotations
from os import getenv

from expaql.api import ExpaQuery
from expaql.formaters import OportunityApplicationFormatter
from gql.transport.requests import log as requests_logger

import logging
import atexit

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%I:%M:%S",
    level=logging.INFO,
)
requests_logger.setLevel(logging.WARNING)

expaql: ExpaQuery | None = None


def get_token_file():
    token_file = getenv("REFRESH_TOKEN_FILE")
    if token_file is None:
        token_file = ".token"

    return token_file


def main():
    global expaql

    with open(get_token_file(), "r") as f:
        refresh_token = f.read().strip()

    client_id = getenv("EXPA_OAUTH_CLIENT_ID")
    client_secret = getenv("EXPA_OAUTH_CLIENT_SECRET")

    if client_id is None or client_secret is None:
        raise Exception(
            "Please set EXPA_OUTH_CLIENT_ID and "
            "EXPA_OAUTH_CLIENT_SECRET env variables"
        )

    expaql = ExpaQuery(client_id, client_secret, refresh_token)
    for x in expaql.get_applications():
        formatter = OportunityApplicationFormatter(x)
        print(formatter.format_markdown())


def exit_handler():
    global expaql

    if expaql is not None:
        with open(get_token_file(), "w") as f:
            f.write(expaql.get_refresh_token())


if __name__ == "__main__":
    atexit.register(exit_handler)
    try:
        main()
    except Exception as e:
        logging.fatal(e, exc_info=True)
