from __future__ import annotations

from datetime import timedelta
from typing import Callable, List, Optional

from trello import Board, Card, List as TrelloList, TrelloClient

from receptiontool.expaql.formaters import OpAppFormatter
from receptiontool.expaql.models import OpportunityApplication


class TrelloConn:
    __client: TrelloClient
    __board: Board
    new_card_callback: Optional[Callable[[OpportunityApplication, Card], None]]

    def __init__(self, api_key: str, token: str, board_id: str):
        self.__client = TrelloClient(api_key, token)
        self.__board = self.__client.get_board(board_id)
        self.new_card_callback = None

    def get_list_by_name(self, name: str) -> TrelloList:
        for trello_list in self.__board.all_lists():
            if trello_list.name == name:
                return trello_list

        raise Exception(f"List '{name}' not found in Trello")

    def get_first_list(self) -> TrelloList:
        for trello_list in self.__board.all_lists():
            if not trello_list.closed:
                return trello_list

        raise Exception("No lists in Trello")

    def add_new_card(
        self,
        expa_application: OpportunityApplication,
        trello_list: TrelloList,
    ) -> None:
        card_name = expa_application.person.full_name
        card_description = OpAppFormatter.format_markdown(expa_application)

        card = trello_list.add_card(card_name, card_description)
        card.set_start(expa_application.created_at)
        card.set_due(expa_application.created_at + timedelta(days=1))

        if self.new_card_callback is not None:
            self.new_card_callback(expa_application, card)

    def add_new_cards(
        self, expa_applications: List[OpportunityApplication], trello_list: TrelloList
    ) -> None:
        for expa_application in expa_applications:
            self.add_new_card(expa_application, trello_list)
