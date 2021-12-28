from flask import Flask
from flask.templating import render_template
from model import Question, Module

app = Flask(__name__)
app.secret_key = '5#y2L"F4Q8zsa7Zb'

@app.route('/')
def startseite():
    return render_template('startseite.html', result = dict)

@app.route('/game', methods = ['GET', 'POST'])
@app.route('/game/<int:answer>', methods = ['GET', 'POST'])
def game(answer=-1):
    data = [
        {
            'frage': 'fragen über fragen...',
            'antwort1': 'antowort1...',
            'antwort2': 'antowort2...',
            'antwort3': 'antowort3...',
            'antwort4': 'antowort4...'
        }
    ]
    return render_template('game.html', data=data, result = dict)

@app.route('/questions')
def questions():
    return render_template('questions.html', result = dict) 


if __name__ == '__main__':
    app.run()
