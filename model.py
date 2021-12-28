import random
from enum import Enum
from tkinter import *



class Status(Enum):
    Right = 0,
    Wrong = 1,
    WrongInput = 2,
    Exit = 3


class Question(object):
    fragetext = None
    level = None
    antwortmoeglichkeit = None
    antwort = None

    # ctor + toString anscheinend in folien
    def __init__(self, fragetext, level, antwortmoeglichkeit, antwort):
        if not 0 <= level <= 4:
            print("Level konnte nicht ausgelesen werden!")
            return
        self.level = level
        self.fragetext = fragetext
        self.antwortmoeglichkeit = antwortmoeglichkeit
        self.antwort = antwort

    def __str__(self):
        return str(self.level) + " " + self.fragetext + " " + self.antwortmoeglichkeit.__str__() + " " + str(self.antwort)


class Module(object):

    def read_questions(self, fName):
        print("Auslesen der Dateien")
        questions = []
        file = open(fName, 'r')
        for line in file:
            line = line.replace("\n", "")
            if line[0].isnumeric():
                question = line.split("\t")
                answers = [question[2], question[3], question[4], question[5]]
                random.shuffle(answers)
                end_question = Question(question[1], int(question[0]), answers, answers.index(question[2]))
                questions.append(end_question)
        return questions

    def get_rand_question(self, level, questions):
        questions_level = []
        for i in questions:
            if i.level == level:
                question = i
                questions_level.append(i)
        return random.choice(questions_level)

    def check_answer(self, question, answer):
        if str(answer).startswith("exit"):
            exit()
        elif answer == str(question.antwort):
            print("Right")
            return Status.Right
        elif str(answer).isnumeric():
            print("Wrong")
            return Status.Wrong
        return Status.Wrong

    def main(self):
        print("Datei suchen...")
        questions = self.read_questions("millionaire.txt")
        for i in questions:
            print(i.__str__())
        self.consoleOutput(questions)
        
    def consoleOutput(self, questions):
        user_input = Status.Right
        player_level = -1
        while user_input != Status.Wrong:
            player_level += 1
            if player_level == 5:
                print("Du hast gewonnnen :D ")
                return
            print("-------------------------------")
            print("Your current level is %s" % str(player_level))
            question = self.get_rand_question(player_level, questions)
            print(question.fragetext)
            for i in question.antwortmoeglichkeit:
                print(i + " (" + str(question.antwortmoeglichkeit.index(i)) + ")")
            user_input = self.check_answer(question, input("Your answer: "))



