from __future__ import annotations

from typing import List

from trello import TrelloClient, List as TrelloList
import logging

from receptiontool.expaql.formaters import OpportunityApplicationFormatter
from receptiontool.expaql.models import OpportunityApplication


def load_already_added_ids() -> list:
    try:
        with open("trello_cards") as file:
            lines = file.read().splitlines()
        return lines
    except FileNotFoundError:
        logging.info("File with cards ids does not exist, assuming that no cards are in trello")
        return []


class TrelloConn:
    def __init__(self, api_key: str, token: str, board_id: str):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id
        self.list_of_ids = load_already_added_ids()

    def add_new_card(self, card_name: str, card_id: int, card_description: str,
                     selected_list: TrelloList) -> None:
        if self.card_already_in_trello(card_id):
            return

        selected_list.add_card(card_name, card_description)

    def add_list_of_cards(self, applications: List[OpportunityApplication], list_name: str | None = None) -> None:
        client = TrelloClient(self.api_key, self.token)
        board = client.get_board(self.board_id)
        lists = board.all_lists()

        selected_list = None
        for trello_list in lists:
            # if None return first, unless it is archived
            if (list_name is None and not trello_list.closed) or trello_list.name == list_name:
                selected_list = trello_list
                break

        if selected_list is None:
            raise Exception(f"No list found with a given name: {list_name}")

        for application in applications:
            formatter = OpportunityApplicationFormatter(application)
            self.add_new_card(application.person.full_name, application.id, formatter.format_markdown(), selected_list)

    def card_already_in_trello(self, card_id: int) -> bool:
        if card_id in self.list_of_ids:
            return True
        else:
            with open("trello_cards", "a") as file:
                file.write(f"{card_id}\n")
            return False
