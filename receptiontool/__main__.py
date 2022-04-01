#!/usr/bin/env python3

from __future__ import annotations

import logging
from typing import List

from gql.transport.requests import log as gql_logger
import requests
from trello.card import Card
from trello.label import Label

from receptiontool.config import IgvToolConfig
from receptiontool.expaql.api import ExpaQuery
from receptiontool.expaql.formaters import OpAppFormatter
from receptiontool.expaql.models import OpportunityApplication
from receptiontool.trello_conn import TrelloConn

config = IgvToolConfig()
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%I:%M:%S",
    level=config.log_level,
)
gql_logger.setLevel(logging.WARNING)


def refresh_token_callback(refres_token: str) -> None:
    logging.debug("Writing new token")
    with open(config.token_file, "w") as f:
        f.write(refres_token)


def new_card_callback(app: OpportunityApplication, trello_card: Card) -> None:
    with open(config.data_file, "a") as f:
        f.write(f"{app.id}\n")

    embed = OpAppFormatter.format_discord_embed(app, trello_card.url)
    data = {"embeds": [embed]}
    res = requests.post(config.discord.webhook_url, json=data)

    if not res.ok:
        logging.fatal(
            f"Unable to send Discord webhook message: HTTP{res.status_code} '{res.text}'"
        )


def trello_label_callback(
    app: OpportunityApplication, board_labels: List[Label]
) -> List[Label]:
    labels = []
    for label in board_labels:
        name = label.name.strip().lower()
        if name == "partner lc" and app.person.home_lc.id in config.expa.partner_lcs:
            labels.append(label)
        elif name == app.slot.title.strip().lower():
            labels.append(label)

    return labels


def check_for_updates() -> None:
    with open(config.token_file, "r") as f:
        refresh_token = f.read().strip()
    with open(config.data_file, "r") as f:
        ignored_apps = {int(it) for it in f.read().splitlines()}

    logging.info(f"Loaded {len(ignored_apps)} ids from the ignored apps file")

    expaql = ExpaQuery(
        config.expa.client_id,
        config.expa.client_secret,
        refresh_token,
        refresh_token_callback,
    )
    trello = TrelloConn(
        config.trello.api_key,
        config.trello.token,
        config.trello.board_id,
    )
    trello.new_card_callback = new_card_callback
    trello.label_callback = trello_label_callback

    new_apps = expaql.get_applications_by_ids(config.expa.opportunities)
    logging.info(f"Fetched {len(new_apps)} from EXPA")

    filtered_apps = [app for app in new_apps if app.id not in ignored_apps]

    if config.trello.list_name is not None:
        trello_list = trello.get_list_by_name(config.trello.list_name)
    else:
        trello_list = trello.get_first_list()

    logging.info(f"Adding {len(filtered_apps)} to Trello")
    trello.add_new_cards(filtered_apps, trello_list)


def entrypoint() -> None:
    logging.info("Starting receptiontool")
    try:
        check_for_updates()
    except Exception as e:
        logging.fatal(e, exc_info=True)
