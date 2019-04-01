from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=('GET','POST'))
def home():
    if request.method == 'POST':
        Player = []
        for i in range(6):
            Player.append(request.form['player' + str(i+1)])
        return redirect(url_for('selectcards'))
    return render_template('home.html')

@app.route('/selectcards', methods=('GET','POST'))
def selectcards():
    if request.method == 'POST':
        print(request.form['ballroom'])
        print(request.form['billiard_room'])
        return redirect(url_for('cards'))
    return render_template('selectcards.html')

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
