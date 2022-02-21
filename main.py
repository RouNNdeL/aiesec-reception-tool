#!/usr/bin/env python3

from expaql.api import ExpaQuery
from gql.transport.aiohttp import log as requests_logger
import logging

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%I:%M:%S",
    level=logging.INFO,
)
requests_logger.setLevel(logging.WARNING)


def main():
    expaql = ExpaQuery(
        "e17bccea2b3ee0f7350df6b6caa3a5cb5bc1da2e5d4b4c7b9765f3ba5258cab2"
    )
    person = expaql.get_current_person()
    logging.info("Logged in as %s", person)


if __name__ == "__main__":
    main()
