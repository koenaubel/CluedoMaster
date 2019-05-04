from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from turn import add_turn, update_cards_in_hand, check_solution_cards
import os
import cards as c

app = Flask(__name__)
app.secret_key = b'%%\x14\xb82\xf6\xf9\xb2f\x91L+\xc1\xea\x7fs'


@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        session.clear()
        players = list()
        for player in request.form.getlist('player'):
            if player != "":
                players.append(player)
        if not players:
            flash("First enter the player's names.")
            return redirect(url_for('home'))
        session['players'] = players
        return redirect(url_for('select_cards'))
    return render_template('home.html')


@app.route('/select_cards', methods=('GET', 'POST'))
def select_cards():
    if request.method == 'POST':
        cards_in_hand = request.form.get('cards_in_hand')
        if not cards_in_hand:
            flash("First select the cards you have in your hand.")
            return redirect(url_for('select_cards'))
        cards_in_hand = cards_in_hand.split(",")
        session['found_cards'] = dict()
        update_cards_in_hand(cards_in_hand, session['players'][0])
        check_solution_cards()
        return redirect(url_for('cards'))
    if 'players' not in session:
        return redirect(url_for('home'))
    return render_template('select_cards.html', locations=c.LOCATIONS, suspects=c.SUSPECTS, weapons=c.WEAPONS)


@app.route('/turns', methods=('GET', 'POST'))
def turns():
    if request.method == 'POST':
        solved = add_turn(request.form)
        if solved:
            return redirect(url_for('solved'))
    if 'players' not in session:
        return redirect(url_for('home'))
    if 'cards_in_hand' not in session:
        return redirect(url_for('select_cards'))
    return render_template('turns.html', locations=c.LOCATIONS, suspects=c.SUSPECTS, weapons=c.WEAPONS)


@app.route('/cards', methods=('GET', 'POST'))
def cards():
    if request.method == 'POST':
        solved = add_turn(request.form)
        if solved:
            return redirect(url_for('solved'))
    if 'players' not in session:
        return redirect(url_for('home'))
    if 'cards_in_hand' not in session:
        return redirect(url_for('select_cards'))
    return render_template('cards.html', locations=c.LOCATIONS, suspects=c.SUSPECTS, weapons=c.WEAPONS)


@app.route('/solved')
def solved():
    return render_template('solved.html', locations=c.LOCATIONS, suspects=c.SUSPECTS, weapons=c.WEAPONS)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
