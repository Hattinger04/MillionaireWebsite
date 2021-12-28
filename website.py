from flask import Flask
from flask.templating import render_template
from model import Question, Module

app = Flask(__name__)


@app.route('/')
def startseite():
    return render_template('startseite.html', result = dict)

@app.route('/game')
@app.route('/game/<int:answer>')
def game(answer=-1):
    return render_template('game.html', result = dict)

@app.route('/questions')
def questions():
    return render_template('questions.html', result = dict) 


if __name__ == '__main__':
    app.run()
