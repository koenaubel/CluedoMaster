from flask import session


def add_turn(turn_data):
    if 'turn' not in session:
        session['turn'] = list()
    turn_list = session['turn']
    turn_list.append(turn_data)
    session['turn'] = turn_list

    if "cardShowedToMe" in turn_data:
        update_cards_in_hand(turn_data['cardShowedToMe'], turn_data['show_player'])

    player = next_player(turn_data['turn_player'])
    cards = [turn_data['location_asked'], turn_data['suspect_asked'], turn_data['weapon_asked']]
    while turn_data['show_player'] != player and turn_data['turn_player'] != player:
        update_cards_not_in_hand(cards, player)
        player = next_player(player)


def next_player(player):
    if 'players' not in session:
        return None
    players = session['players']
    i = players.index(player) + 1
    if i == len(players):
        i = 0
    return players[i]


def update_cards_in_hand(cards, player):
    if 'cards_in_hand' not in session:
        session['cards_in_hand'] = dict()
    if type(cards) is list:
        for card in cards:
            session['cards_in_hand'][card] = player
    elif type(cards) is str:
        session['cards_in_hand'][cards] = player


def update_cards_not_in_hand(cards, player):
    if 'players' not in session:
        return
    players = session['players']
    if player == players[0]:
        return
    if 'cards_not_in_hand' not in session:
        session['cards_not_in_hand'] = dict()
    for card in cards:
        if card not in session['cards_not_in_hand']:
            session['cards_not_in_hand'][card] = [player]
        else:
            if player not in session['cards_not_in_hand'][card]:
                session['cards_not_in_hand'][card].append(player)
        if len(session['cards_not_in_hand'][card]) == len(players) - 1:
            update_solution(card)


def update_solution(card):
    if 'solution' not in session:
        session['solution'] = list()
    session['solution'].append(card)
