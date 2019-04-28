from flask import session


def add_turn(turn_data):
    if 'turn' not in session:
        session['turn'] = list()
    turn_list = session['turn']
    turn_list.append(turn_data)
    session['turn'] = turn_list


def update_cards_in_hand(cards, player):
    if 'cards_in_hand' not in session:
        session['cards_in_hand'] = dict()
    for card in cards:
        session['cards_in_hand'][card] = player


def update_cards_not_in_hand(cards, player):
    if 'cards_not_in_hand' not in session:
        session['cards_not_in_hand'] = list()
    for card in cards:
        if card not in session['cards_not_in_hand']:
            session['cards_in_hand'][card] = [player]
        else:
            session['cards_in_hand'][card].append(player)
