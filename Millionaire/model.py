import random
import os
import sys

from flask_restful import Resource


class Question(object):
    id = None
    fragetext = None
    level = None
    antwortmoeglichkeit = None
    antwort = None

    def __init__(self, id, fragetext, level, antwortmoeglichkeit, antwort):
        if not 0 <= level <= 4:
            raise ValueError("Level has no good value.")
        self.id = id
        self.level = level
        self.fragetext = fragetext
        self.antwortmoeglichkeit = antwortmoeglichkeit
        self.antwort = antwort

    def __str__(self):
        return str(id) + " " + str(self.level) + " " + self.fragetext + " " + self.antwortmoeglichkeit.__str__() + " " + str(self.antwort)

    def serialize(self):
        return {
            "id": self.id,
            "level": self.level,
            "fragetext": self.fragetext,
            "antwortmoeglichkeit": self.antwortmoeglichkeit,
            "antwort": self.antwort
        }

class Module(object):
    def read_questions(fName):
        id = 0
        questions = []
        file = open(os.path.join(sys.path[0], fName), 'r')
        for line in file:
            line = line.replace("\n", "")
            if line[0].isnumeric():
                question = line.split("\t")
                answers = [question[2], question[3], question[4], question[5]]
                random.shuffle(answers)
                end_question = Question(id, question[1], int(question[0]), answers, answers.index(question[2]))
                id = id + 1
                questions.append(end_question)
        return questions

    def get_rand_question(level, questions):
        questions_level = []
        for i in questions:
            if i.level == level:
                questions_level.append(i)
        return random.choice(questions_level)

    def getAllQuestions(self):
        pass

    def getQuestionById(self, id):
        pass
    def addQuestion(self, question):
        pass
    def deleteQuestion(self, id):
        pass
    def changeQuestion(self, id, Question):
        pass



