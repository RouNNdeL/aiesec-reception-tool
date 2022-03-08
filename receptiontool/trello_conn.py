from __future__ import annotations

from typing import List

from trello import TrelloClient, List as TrelloList
import logging

from receptiontool.expaql.formaters import OpportunityApplicationFormatter
from receptiontool.expaql.models import OpportunityApplication


class TrelloConn:
    def __init__(self, api_key: str, token: str, board_id: str, cards_filename: str):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id
        self.cards_filename = cards_filename
        self.list_of_ids = self.load_already_added_ids()

    def add_new_card(self, card_name: str, card_id: int, card_description: str,
                     selected_list: TrelloList) -> None:
        if card_id in self.list_of_ids:
            return

        self.add_card_id_to_list_and_file(card_id)
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

    def add_card_id_to_list_and_file(self, card_id: int) -> None:
        with open(self.cards_filename, "a") as file:
            file.write(f"{card_id}\n")
        self.list_of_ids.append(card_id)

    def load_already_added_ids(self) -> List:
        try:
            with open(self.cards_filename) as file:
                lines = file.read().splitlines()
            return lines
        except FileNotFoundError:
            logging.warning("File with cards ids does not exist, assuming that no cards are in trello")
            return []
