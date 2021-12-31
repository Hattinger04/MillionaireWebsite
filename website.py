from flask import Flask
from flask.templating import render_template
from model import Question, Module

app = Flask(__name__)
app.secret_key = '5#y2L"F4Q8zsa7Zb'
questions = Module.read_questions("millionaire.txt")
player_level = -1
right_answer = -1

def new_question(level): 
    global right_answer
    question = Module.get_rand_question(level, questions)
    right_answer = question.antwort
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
    return data


@app.route('/')
def startSite():
    global player_level
    player_level = -1
    return render_template('startseite.html', result = dict)

@app.route('/game')
@app.route('/game/<int:answer>', methods = ['GET', 'POST'])
def gameSite(answer=-1):
    global player_level
    player_level += 1
    if(player_level == 5): 
        return render_template('game.html', data="winning", result = dict)
    elif(player_level != 0): 
        if answer != right_answer:
            # return to smth different when not right answer - right now "startseite"
            player_level = -1
            return render_template('startseite.html', result = dict)
        return render_template('game.html', data=new_question(player_level), result = dict)
    else: 
        return render_template('game.html', data=new_question(player_level), result = dict)

@app.route('/questions')
def questionsSite():
    fragen = []
    for q in questions: 
        fragen.append({
            "level": q.level,
            "frage": q.fragetext
        })
    return render_template('questions.html', data=fragen, result = dict) 



if __name__ == '__main__':
    app.run()