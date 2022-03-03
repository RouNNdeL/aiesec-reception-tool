from trello import TrelloClient
import requests

api_key = '79845a991d59b3158e3d1a7201e6dad6'
token = '316d8ea02a0e5be37e3de243cd2be19c52ac3e27b7b6f35795cca225f4a14359'
trello_client = TrelloClient(api_key, token)
board_id = '621e033969a2640751cfd39c'
list1_id = '621e0347f6d23431bec705c6'


def add_new_card(card_name, card_description, list_name=None, client=None):
    if client is None:
        client = TrelloClient(api_key, token)
    board = client.get_board(board_id)
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


def get_card_ids(client=None):
    if client is None:
        client = TrelloClient(api_key, token)
    board = client.get_board(board_id)
    lists = board.all_lists()
    cards = []
    for trello_list in lists:
        cards.extend(trello_list.list_cards())
    return cards


if __name__ == "__main__":
    # add_new_card("archived", "dupa", "col2")
    get_card_ids()

    print("FINISH")
