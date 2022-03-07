from trello import TrelloClient
import requests


def card_already_in_trello(card_id):
    with open("trello_cards") as file:
        lines = file.readlines()
    if f"{card_id}\n" in lines:
        return True
    else:
        with open('trello_cards', 'a') as file:
            file.write(f'{card_id}\n')
        return False


class TrelloConn:
    def __init__(self, api_key, token, board_id):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id

    def add_new_card(self, info, card_description, list_name=None, client=None):
        card_name = info[0]
        card_id = info[1]
        if card_already_in_trello(card_id):
            return
        if client is None:
            client = TrelloClient(self.api_key, self.token)
        board = client.get_board(self.board_id)
        lists = board.all_lists()
        selected_list = None
        for trello_list in lists:
            # if None return first, unless it is archived
            if (list_name is None and not trello_list.closed) or trello_list.name == list_name:
                selected_list = trello_list
                break
        if selected_list is not None:
            selected_list.add_card(card_name, card_description)
        else:
            print(f"No list found with a given name: {list_name}")

    def get_card_ids(self, client=None):
        if client is None:
            client = TrelloClient(self.api_key, self.token)
        board = client.get_board(self.board_id)
        lists = board.all_lists()
        cards = []
        for trello_list in lists:
            cards.extend(trello_list.list_cards())
        return cards
