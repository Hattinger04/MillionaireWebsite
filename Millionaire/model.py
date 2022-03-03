import random
import os
import sys
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func

Base = declarative_base()
metadata = Base.metadata
engine = create_engine(
    r'sqlite:///C:\Users\s8gre\Documents\Schule\4BHWII\CC\MillionaireWebsite\millionaire.sqlite3')  # Welche Datenbank wird verwendet
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
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
    wrongQuestions = []
    questions = None

    # no db included yet
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
        self.questions = questions
        return questions

    def get_rand_question(self, level, questions):
        questions_level = []
        for i in questions:
            if i.level == level:
                questions_level.append(i)
        return random.choice(questions_level)

    def getAllQuestions(self):
        return self.questions

    def getQuestionById(self, ID):
        try:
            for question in self.questions:
                if question.ID == ID:
                    return question
            return None
        except(IndexError):
            return None

    def addQuestion(self, question):
        info = Millionaire.query.filter_by(id=question.ID)
        if info is not None:
            return False
        self.setWrongQuestion(question.antwort)

        questionDB = Millionaire(id=question.ID, difficulty=question.level, question=question.fragetext, \
                                   correct_answer=question.antwortmoeglichkeit[int(question.antwort)], answer2=question.antwortmoeglichkeit[self.wrongQuestions[0]], \
                                   answer3=question.antwortmoeglichkeit[self.wrongQuestions[1]], answer4=question.antwortmoeglichkeit[self.wrongQuestions[2]], background_information ="")
        session = db_session.session_factory()
        session.begin()
        session.add(questionDB)
        session.commit()
        session.flush()
        session.close()
        return True

    def deleteQuestion(self, ID):
        info = Millionaire.query.filter_by(id=ID)
        if info is None:
            return False
        Millionaire.query.filter_by(id=ID).delete()
        db_session.commit()
        db_session.flush()
        return True

    def changeQuestion(self, ID, question):
        info = Millionaire.query.filter(Millionaire.id == 1)
        if info is None:
            self.addQuestion(question)
            return False
        self.setWrongQuestion(question.antwort)
        Millionaire.query.filter(Millionaire.id == 1).update(dict(id=question.ID, difficulty=question.level, question=question.fragetext, \
                                   correct_answer=question.antwortmoeglichkeit[int(question.antwort)], answer2=question.antwortmoeglichkeit[self.wrongQuestions[0]], \
                                   answer3=question.antwortmoeglichkeit[self.wrongQuestions[1]], answer4=question.antwortmoeglichkeit[self.wrongQuestions[2]], background_information =""))
        db_session.commit()
        db_session.flush()
        return True

    def setWrongQuestion(self, rightQuestion):
        self.wrongQuestions.clear()
        for i in range(4):
            if i != int(rightQuestion):
                self.wrongQuestions.append(i)

