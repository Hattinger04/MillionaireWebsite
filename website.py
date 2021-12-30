from flask import Flask
from flask.templating import render_template
from model import Question, Module

app = Flask(__name__)
app.secret_key = '5#y2L"F4Q8zsa7Zb'
questions = Module.read_questions("millionaire.txt")
player_level = -1

@app.route('/')
def startSite():
    return render_template('startseite.html', result = dict)

@app.route('/game')
@app.route('/game/<int:answer>', methods = ['GET', 'POST'])
def gameSite(answer=-1):
    global player_level
    player_level += 1
    if(player_level != 0): 
        pass
        # get value and check if correct

        # if correct next question

        # else return false

    else: 
        # first Question: 
        question = Module.get_rand_question(0, questions)

        data = [
            {
                'frage': question.fragetext,
                'level': question.level,
                'antwort1': question.antwortmoeglichkeit[0],
                'antwort2': question.antwortmoeglichkeit[1],
                'antwort3': question.antwortmoeglichkeit[2],
                'antwort4': question.antwortmoeglichkeit[3]
            }
           
    ]
    return render_template('game.html', data=data, result = dict)
    

@app.route('/questions')
def questionsSite():
    return render_template('questions.html', result = dict) 


if __name__ == '__main__':
    app.run()
