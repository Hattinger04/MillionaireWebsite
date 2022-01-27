from flask import Flask, session, request
from flask.templating import render_template
from flask_restful import Resource, Api
from model import Module, Question

app = Flask(__name__)
app.secret_key = '5#y2L"F4Q8zsa7Zb'
module = Module()
questions = module.read_questions("millionaire.txt")
api = Api(app)

def new_question(level):
    question = module.get_rand_question(level, questions)
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
    return render_template('startseite.html', result = dict)

@app.route('/game')
@app.route('/game/<int:answer>')
def gameSite(answer=-1):
    session["level"] += 1
    if(session["level"] == 5):
        return render_template('game.html', data="winning", result = dict)
    elif(session["level"] != 0):
        if answer != session["answer"]:
            return render_template('startseite.html', result = dict)
        return render_template('game.html', data=new_question(session["level"]), result = dict)
    else:
        return render_template('game.html', data=new_question(session["level"]), result = dict)

@app.route('/questions')
def questionsSite():
    data = []
    for q in questions:
        data.append({
            "ID": q.ID,
            "level": q.level,
            "frage": q.fragetext
        })
    return render_template('questions.html', data=data, result = dict)

# nachfragen wohin?
def getAll(self):
    questions = module.getAllQuestions()
    message = []
    for question in questions:
        message.append(question.serialize())
    return {"Message" : message}

class Service(Resource):
    def get(self, id):
        return module.getQuestionById(id).serialize()
    def put(self, id):
        question = Question(id,request.form["fragetext"], int(request.form["level"]),request.form["antwortmoeglichkeit"],request.form["antwort"])
        status = module.addQuestion(question)
        if status:
            return {"Message": "Neu hinzugefügt"}
        return {"Message": "Überschrieben"}
    def delete(self, id):
        status = module.deleteQuestion(id)
        if status:
            return {"Message": "Frage mit der ID %s gelöscht" % id}
        return {"Message": "Frage mit der ID %s exisitiert nicht!" % id}
    def patch(self, id):
        question = Question(id, request.form["fragetext"], int(request.form["level"]), request.form["antwortmoeglichkeit"], request.form["antwort"])
        status = module.changeQuestion(id, question)
        if status:
            return {"Message": "Frage mit der ID %s gepatched" % id}
        return {"Message": "Frage mit der ID %s wurde neu erstellt" % id}


api.add_resource(Service, "/service/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)