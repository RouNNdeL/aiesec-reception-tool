from trello import TrelloClient
import requests

class TrelloConn:
    def __init__(self, api_key, token, board_id):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id

    def add_new_card(self, card_name, card_description, list_name=None, client=None):
        if client is None:
            client = TrelloClient(self.api_key, self.token)
        board = client.get_board(self.board_id)
        lists = board.all_lists()
        selected_list = None
        for trello_list in lists:
            # if None return first
            if list_name is None or trello_list.name == list_name:
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

    def card_already_in_trello(self, description):



if __name__ == "__main__":
    print("FINISH")
