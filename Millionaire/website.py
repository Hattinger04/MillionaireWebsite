from flask import Flask, session
from flask.templating import render_template
from flask_restful import Resource, Api
from model import Module

app = Flask(__name__)
app.secret_key = '5#y2L"F4Q8zsa7Zb'
questions = Module.read_questions('millionaire.txt')

def new_question(level):
    question = Module.get_rand_question(level, questions)
    session["answer"] = question.antwort
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
    session["level"] = -1
    session["answer"] = -1
    return render_template('templates/startseite.html', result = dict)

@app.route('/game')
@app.route('/game/<int:answer>')
def gameSite(answer=-1):
    session["level"] += 1
    if(session["level"] == 5):
        return render_template('templates/game.html', data="winning", result = dict)
    elif(session["level"] != 0):
        if answer != session["answer"]:
            return render_template('templates/startseite.html', result = dict)
        return render_template('templates/game.html', data=new_question(session["level"]), result = dict)
    else:
        return render_template('templates/game.html', data=new_question(session["level"]), result = dict)

@app.route('/questions')
def questionsSite():
    data = []
    for q in questions:
        data.append({
            "level": session["level"],
            "frage": session["question"]
        })
    return render_template('templates/questions.html', data=data, result = dict)


class Service(Resource):
    def get(self, id):
        return Module.getQuestionById(id)
    def put(self, question):
        status = Module.addQuestion(question)
        if status:
            return {"Message": "Neu hinzugefügt"}
        return {"Message": "Überschrieben"}
    def delete(self, id):
        Module.deleteQuestion(id)
        return {"Message": "Frage mit der ID %s gelöscht" % id}
    def patch(self, id):
        Module.changeQuestion(id)
        return {"Message": "Frage mit der ID %s gepatched" % id}
    def getAll(self):
        return Module.getAllQuestions()

if __name__ == '__main__':
    app.run(debug=True)