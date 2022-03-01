#!/usr/bin/env python3

from __future__ import annotations
from os import getenv

from expaql.api import ExpaQuery
from expaql.formaters import OportunityApplicationFormatter
from config import IgvToolConfig
from gql.transport.requests import log as gql_logger

import logging
import atexit

config = IgvToolConfig()
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%I:%M:%S",
    level=config.log_level
)
gql_logger.setLevel(logging.WARNING)

expaql: ExpaQuery | None = None

def main():
    global expaql

    with open(config.token_file, "r") as f:
        refresh_token = f.read().strip()

    expaql = ExpaQuery(config.expa_client_id, config.expa_client_secret, refresh_token)
    for x in expaql.get_applications():
        formatter = OportunityApplicationFormatter(x)
        print(formatter.format_markdown())


def exit_handler():
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
