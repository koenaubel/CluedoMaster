from flask import session, request


def add_turn(turn_data):
    if 'turn' not in session:
        session['turn'] = list()
    turn_list = session['turn']
    turn_list.append(turn_data)
    session['turn'] = turn_list
