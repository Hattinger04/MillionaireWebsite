import random
import os
import sys

class Question(object):
    ID = None
    fragetext = None
    level = None
    antwortmoeglichkeit = None
    antwort = None

    def __init__(self, ID, fragetext, level, antwortmoeglichkeit, antwort):
        if not 0 <= level <= 4:
            raise ValueError("Level has no good value.")
        self.ID = ID
        self.level = level
        self.fragetext = fragetext
        self.antwortmoeglichkeit = antwortmoeglichkeit
        self.antwort = antwort

    def __str__(self):
        return str(self.ID) + " " + str(self.level) + " " + self.fragetext + " " + self.antwortmoeglichkeit.__str__() + " " + str(self.antwort)

    def serialize(self):
        return {
            "ID": self.ID,
            "level": self.level,
            "fragetext": self.fragetext,
            "antwortmoeglichkeit": self.antwortmoeglichkeit,
            "antwort": self.antwort
        }

class Module(object):
    questions = None
    def read_questions(self, fName):
        ID = 0
        questions = []
        file = open(os.path.join(sys.path[0], fName), 'r')
        for line in file:
            line = line.replace("\n", "")
            if line[0].isnumeric():
                question = line.split("\t")
                answers = [question[2], question[3], question[4], question[5]]
                random.shuffle(answers)
                end_question = Question(ID, question[1], int(question[0]), answers, answers.index(question[2]))
                ID = ID + 1
                questions.append(end_question)
                print(end_question)
        self.questions = questions
        return questions

    def get_rand_question(level, questions):
        questions_level = []
        for i in questions:
            if i.level == level:
                questions_level.append(i)
        return random.choice(questions_level)

    def getAllQuestions(self):
        return self.questions
    def getQuestionById(self, ID):
        try:
            if(self.questions[ID] in self.questions):
                return self.questions[ID]
        except(IndexError):
            return None
    def addQuestion(self, question):
        if(question in self.questions):
            return False
        self.questions.append(question)
        return True
    def deleteQuestion(self, ID):
        question = self.getQuestionById(ID)
        if (question not in self.questions):
            return False
        self.questions.remove(question)
        return True
    def changeQuestion(self, ID, question):
        if (self.questions[ID] not in self.questions):
            return False
        self.questions[ID] = question
        return True



