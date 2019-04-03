from flask import Flask, render_template, request, redirect, url_for, session
import os
import cards as c

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/', methods=('GET','POST'))
def home():
    if request.method == 'POST':
        players = list()
        for player in request.form.getlist('player'):
            if player != "":
                players.append(player)
        session['players'] = players
        return redirect(url_for('select_cards'))
    return render_template('home.html')


@app.route('/select_cards', methods=('GET','POST'))
def select_cards():
    if request.method == 'POST':
        return redirect(url_for('cards'))
    return render_template('select_cards.html', locations=c.locations(),suspects=c.suspects(), weapons=c.weapons())


@app.route('/turns')
def turns():
    return render_template('turns.html')


@app.route('/cards')
def cards():
    return render_template('cards.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
