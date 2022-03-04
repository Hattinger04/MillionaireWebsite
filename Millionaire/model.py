import random
import os
import sys
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
import deprecation

Base = declarative_base()
metadata = Base.metadata
engine = create_engine(
    r'sqlite:///C:\Users\s8gre\Documents\Schule\4BHWII\CC\MillionaireWebsite\millionaire.sqlite3')  # Welche Datenbank wird verwendet
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()


class Millionaire(Base):
    __tablename__ = 'millionaire'

    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer)
    question = Column(Text)
    correct_answer = Column(Text)
    answer2 = Column(Text)
    answer3 = Column(Text)
    answer4 = Column(Text)
    background_information = Column(Text)

    def serialize(self):
        return {
            "ID": self.id,
            "level": self.difficulty,
            "fragetext": self.question,
            "antwortmoeglichkeit": [self.correct_answer, self.answer2, self.answer3, self.answer4],
            "antwort": 0
        }


class Question(object):
    ID = None
    fragetext = None
    level = None
    antwortmoeglichkeit = []
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
        return str(self.ID) + " " + str(
            self.level) + " " + self.fragetext + " " + self.antwortmoeglichkeit.__str__() + " " + str(self.antwort)

    def serialize(self):
        return {
            "ID": self.ID,
            "level": self.level,
            "fragetext": self.fragetext,
            "antwortmoeglichkeit": self.antwortmoeglichkeit,
            "antwort": self.antwort
        }


class Module(object):
    wrongQuestions = []
    questions = []

    @deprecation.deprecated(details="Old method - now using db")
    def read_questionsFile(self, fName):
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
        self.questions = questions
        return questions

    def read_db(self):
        questionsDB = Millionaire.query.all()
        for question in questionsDB:
            answers = [question.correct_answer, question.answer2,question.answer3, question.answer4]
            random.shuffle(answers)
            self.questions.append(Question(question.id, question.question, question.difficulty, answers, answers.index(question.correct_answer)))

    def get_rand_question(self, level, questions):
        questions_level = []
        for i in questions:
            if i.level == level:
                questions_level.append(i)
        return random.choice(questions_level)

    def getAllQuestions(self):
        return self.questions

    def getQuestionById(self, ID):
        return Millionaire.query.get(ID)

    def addQuestion(self, question):
        info = self.getQuestionById(question.ID)
        if info:
            return False
        self.setWrongQuestion(question.antwort)
        info = Millionaire(id=question.ID, difficulty=question.level, question=question.fragetext, \
                           correct_answer=question.antwortmoeglichkeit[int(question.antwort)],
                           answer2=question.antwortmoeglichkeit[self.wrongQuestions[0]], \
                           answer3=question.antwortmoeglichkeit[self.wrongQuestions[1]], \
                           answer4=question.antwortmoeglichkeit[self.wrongQuestions[2]])
        db_session.add(info)
        db_session.flush()
        return True

    def deleteQuestion(self, ID):
        info = self.getQuestionById(ID)
        if not info:
            return False
        db_session.delete(info)
        db_session.flush()
        return True

    def changeQuestion(self, ID, question):
        info = self.getQuestionById(ID)
        if not info:
            self.addQuestion(question)
            return False
        self.setWrongQuestion(question.antwort)
        questionDB = Millionaire(id=question.ID, difficulty=question.level, question=question.fragetext, \
                                 correct_answer=question.antwortmoeglichkeit[int(question.antwort)],
                                 answer2=question.antwortmoeglichkeit[self.wrongQuestions[0]], \
                                 answer3=question.antwortmoeglichkeit[self.wrongQuestions[1]], \
                                 answer4=question.antwortmoeglichkeit[self.wrongQuestions[2]])
        info.difficulty = questionDB.difficulty
        info.question = questionDB.question
        info.correct_answer = questionDB.correct_answer
        info.answer2 = questionDB.answer2
        info.answer3 = questionDB.answer3
        info.answer4 = questionDB.answer4
        db_session.add(info)
        db_session.flush()
        return True

    def setWrongQuestion(self, rightQuestion):
        self.wrongQuestions.clear()
        for i in range(4):
            if i != int(rightQuestion):
                self.wrongQuestions.append(i)
