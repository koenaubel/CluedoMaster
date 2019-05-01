from flask import session


def add_turn(turn_data):
    if 'turns' not in session:
        session['turns'] = list()
    turn_list = session['turns']
    turn_list.append(turn_data)
    session['turns'] = turn_list
    session['found_cards'] = dict()

    # Add showed card to cards_in_hand
    if "cardShowedToMe" in turn_data:
        update_cards_in_hand(turn_data['cardShowedToMe'], turn_data['show_player'])

    # Add players that didn't show a card to cards_not_in_hand
    player = next_player(turn_data['turn_player'])
    cards = [turn_data['location_asked'], turn_data['suspect_asked'], turn_data['weapon_asked']]
    while turn_data['show_player'] != player and turn_data['turn_player'] != player:
        update_cards_not_in_hand(cards, player)
        player = next_player(player)

    # Check every turn for cards we can know
    check_all_turns()


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
    if type(cards) is str:
        cards = [cards]
    for card in cards:
        session['cards_in_hand'][card] = player

    # Add all other player (except oneself) to cards_not_in_hand
    other_players = session['players'].copy()
    other_players.pop(0)
    if player in other_players:
        other_players.remove(player)
    for other_player in other_players:
        update_cards_not_in_hand(cards, other_player)


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
        if len(session['cards_not_in_hand'][card]) == len(players) - 1 and card not in session['cards_in_hand']:
            update_solution(card)


def update_solution(card):
    if 'solution' not in session:
        session['solution'] = list()
    session['solution'].append(card)
    session['found_cards'][card] = 'solution'


def check_has_one_card(cards, player):
    number_of_cards_not_in_hand = 0
    for card in cards:
        if card in session['cards_not_in_hand']:
            if player in session['cards_not_in_hand'][card]:
                number_of_cards_not_in_hand += 1
            else:
                can_have_card = card
        else:
            can_have_card = card
    if number_of_cards_not_in_hand == len(cards) - 1:
        return can_have_card


def check_all_turns():
    added_card = True
    found_cards = dict()
    while added_card:
        added_card = False
        for turn in session['turns']:
            player = turn['show_player']
            cards = [turn['location_asked'], turn['suspect_asked'], turn['weapon_asked']]
            card = check_has_one_card(cards, player)
            if card is not None:
                if card not in session['cards_in_hand']:
                    update_cards_in_hand(card, player)
                    session['found_cards'][card] = player
                    added_card = True
